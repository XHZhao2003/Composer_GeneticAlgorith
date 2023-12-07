from functools import total_ordering
from .Interval import Interval
from torch import Tensor
from .CNN.CNNModel import CNNModel
import random
from copy import deepcopy
import numpy as np

@total_ordering
class Melody:
    def __init__(self, notes: list, length=32):
        self.notes = notes
        self.len = length
        self.score = 0     # 适应度
        assert self.len == len(self.notes)
        
    def GetScore(self, function='basic1', model=None): 
        if function == 'basic1':# 原文献方法
            alpha = 1.0
            beta = 0.5
            gamma = 0.8
            f1, f2 = self.GetIntervalScore(zeta=[1.0, 1.0, 1.0, 1.0], eta=[1.0, 1.0, 1.0, 1.0])    
            bl = self.GetBadNote()    
            self.score = alpha * f1 + beta * f2 + gamma * bl
        elif function == 'basic2': # 自制方法
            self.score = 0.2 * self.FeatureScore(0.5, self.GetSelfSimilarity) + 0.2 * self.FeatureScore(0.5, self.GetLinearity) + 0.2 * self.FeatureScore(0.5, self.GetTonality) + 0.2 * self.FeatureScore(0.5, self.GetPitchDistribution)
        elif function == 'CNN':
            assert model != None
            notes = Tensor([self.notes])
            pred = model(notes)[0]
            self.score = pred[1]      # 模型预测为负样本的概率

    def GetIntervalScore(self, zeta=[1.0, 1.0, 1.0, 1.0], eta=[1.0, 1.0, 1.0, 1.0]):
        # 对所有相邻音程评分，按照小节为单位求平均和方差,据此算出适应度函数f1和f2
        interval = Interval()
        note1 = 0
        note2 = 0
        interval_xi, a, b2 = [], [], []

        for i in range(0, self.len, 8):
            for j in range(i, i+7):
                if (self.notes[j] < 2) or (self.notes[j+1] < 2):
                    continue
                note1, note2 = self.notes[j], self.notes[j+1]
                interval_xi.append(interval.ScoreTwoNote(note1, note2))
            a.append(np.mean(interval_xi))
            b2.append(np.var(interval_xi))
        
        u = [1.0, 1.0, 1.0, 1.0]
        sigma2 = [0, 0.2, 0.2, 0]
        f1, f2 = 0.0, 0.0

        for i in range(len(a)):
            f1 += zeta[i] * abs(u[i] - a[i])
            f2 += eta[i] * abs(sigma2[i] - b2[i])
        return f1, f2

    def GetBadNote(self):
        # 统计调外音的个数
        # 统计G大调中的调外音 (G, A, B, C, D, E, F#)
        outTonality = 0
        Gmaj = [4, 6, 8, 9, 11, 1, 3]       # mod 12
        for note in self.notes:
            if note > 1:
                if (note % 12) not in Gmaj:
                    outTonality += 1
        return outTonality
    
    def GetSelfSimilarity(self):
        # 计算自相似度————相同的音程出现的越频繁，自相似度越高
        cnt = 0
        intervalSum = 0
        for i in range(self.len):
            if self.notes[i] < 2 or self.notes[i+1] < 2:
                continue
            cnt += 1
            intervalSum += abs(self.notes[i+1] - self.notes[i])
        return max(1, 2*intervalSum/cnt/self.len)
    
    def GetLinearity(self):
        # 计算线性度————线性度越低，音调起伏越大
        alpha, beta, kappa = 15, -1, 2
        S = 0.0
        for i in range(1, self.len-1):
            if self.notes[i] < 2 or self.notes[i+1] < 2 or self.notes[i-1] < 2:
                continue
            S += abs(beta*self.notes[i-1] + kappa*self.notes[i] + beta*self.notes[i+1])
        return S^2/(S^2+alpha)
    
    def GetTonality(self):
        # 计算调性一致性————若音符属于一个调性的比例越高，则调性一致性越大。
        keyPrevalence = []
        for i in range(12):
            key = [
                (9 + i) % 12,
                (11 + i) %12,
                (1 + i) %12,
                (2 + i) %12,
                (4 + i) %12,
                (6 + i) %12,
                (8 + i) %12
            ]
            Ki = 0
            for note in self.notes:
                if note < 2:
                    continue
                if note % 12 in key:
                    Ki += 1
            keyPrevalence.append(Ki/self.len)
        return max(keyPrevalence) - (1 - max(keyPrevalence))/(self.len-1)

    def GetPitchDistribution(self):
        # 计算音高分布位置————越高表示音乐整体的音高越高。
        P = [0]*12
        for note in self.notes:
            if note < 2:
                continue
            P[note % 12] += 1
        return (self.len - max(P))/11/self.len*12
    
    def FeatureScore(self, t, eI):
        # 将特征值转化为得分
        if t < 0.5:
            return -1/(1 - t)^2*(eI - t)^2 + 1
        else:
            return -1/(0 - t)^2*(eI - t)^2 + 1

    def GetMutation(self, mutationType=0):
        mutation = deepcopy(self)
        # 变异位置
        target = random.randint(0, mutation.len - 1)
        while mutation.notes[target] < 2:
            # 无法改变休止，延音
            target = random.randint(0, mutation.len - 1)

        if mutationType == 0:           # 无变异
            return mutation
        
        elif mutationType == 1:         # 八度变异
            upOrDown = random.randint(0, 1)
            upperBound = min(28, mutation.notes[target] + 12)
            lowerBound = max(2, mutation.notes[target] - 12)
            if upOrDown == 0:
                mutation.notes[target] = upperBound
            else:
                mutation.notes[target] = lowerBound
            return mutation
            
        elif mutationType == 2:         # 音符变异
            # 0.03的概率变成延音
            res = random.random()
            if res < 0.03 and target > 0:
                mutation.notes[target] = 1
            else:
                # 在上下五度之间随机变异
                deviation = random.randint(-7, 7)
                mutation.notes[target] += deviation
                if mutation.notes[target] > 28:
                    mutation.notes[target] = 28
                elif mutation.notes[target] < 2:
                    mutation.notes[target] = 2
            return mutation
                    
        elif mutationType == 3:         # 交换音符变异
            target2 = random.randint(0, mutation.len - 1)
            # 这里实际上有可能出现一段旋律只有一个音的情况，直接允许自身交换，也就是没有变异
            while mutation.notes[target2] < 2:
                target2 = random.randint(0, mutation.len - 1)
            note1 = mutation.notes[target]
            note2 = mutation.notes[target2]
            mutation.notes[target] = note2
            mutation.notes[target2] = note1
            return mutation                
    
    def __lt__(self, other):
        return self.score < other.score
    
    def __hash__(self):
        hashcode = 0
        for i in range(self.len):
            hashcode += ((self.notes[i] + i**2) ** 3)
        return hashcode
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()