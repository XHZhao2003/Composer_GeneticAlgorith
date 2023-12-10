from functools import total_ordering
from .Interval import Interval
from torch import Tensor
from .CNN.CNNModel import CNNModel
import random
from copy import deepcopy
import numpy as np
from scipy.spatial import distance

@total_ordering
class Melody:
    def __init__(self, notes: list, length=32):
        self.notes = notes
        self.len = length
        self.score = 0     # 适应度
        assert self.len == len(self.notes)
        
    def GetScore(self, function='basic1'): 
        if function == 'basic1':# 原文献方法
            alpha = 1.5
            beta = 1.0
            gamma = 0.5
            f1, f2 = self.GetIntervalScore(zeta=[1.0, 1.0, 1.0, 1.0], eta=[1.0, 1.0, 1.0, 1.0])    
            bl = self.GetBadNote()    
            self.score = alpha * f1 + beta * f2 + gamma * bl
        elif function == 'basic2': # 自制方法
            self.score = 0
            alpha = [1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
            feature = [self.GetSelfSimilarity(), self.GetLinearity(), self.GetTonality(),self.GetPitchDistribution()]
            featureScore = [0.05, 0.5, 1.0, 0.9]
            f1, f2 = self.GetIntervalScore(zeta=[1.0, 1.0, 1.0, 1.0], eta=[1.0, 1.0, 1.0, 1.0])
            fitness = [f1, f2, self.GetRhythmSimilarity()]
            for i in range(len(feature)):
                fitness.append(self.FeatureScore(featureScore[i], feature[i]))
            for i in range(len(alpha)):
                self.score += alpha[i] * fitness[i]

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
        for i in range(self.len-1):
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
        return S**2/(S**2+alpha)
    
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
    
    def GetRhythmSimilarity(self):
        # 计算四小节的节奏相似度,越大越不相似————利用Minkowski Distance
        rhythmSimilarity = 0.0
        rhythm = []
        hand = 0
        for i in range(0, self.len, 8):
            rhythm.append([])
            for j in range(i, i+8):
                if self.notes[j] > 1:
                    rhythm[hand].append(2)
                else:
                    rhythm[hand].append(self.notes[j])
            hand += 1
        for i in range(4):
            for j in range(i+1, 4):
                rhythmSimilarity += distance.minkowski(rhythm[i], rhythm[j], 2)
        return rhythmSimilarity

                
    def FeatureScore(self, t, eI):
        # 将特征值转化为得分
        if t < 0.5:
            return -1/((1 - t)**2)*((eI - t)**2) + 1
        else:
            return -1/((0 - t)**2)*((eI - t)**2) + 1

    def Mutation(self, mutationType:int):
        mutation = 0
        if mutationType == 0:
            mutation = deepcopy(self)
        elif mutationType == 1:
            mutation = self.MutationTransposition()
        elif mutationType == 2:
            mutation = self.MutationInversion()
        elif mutationType == 3:
            mutation = self.MutationOctave()
        elif mutationType == 4:
            mutation = self.MutationNote()
        elif mutationType == 5:
            mutation = self.MutationExtension()
        elif mutationType == 6:
            mutation = self.MutationRest()
        else:
            raise ValueError("Unexpected mutation type %d" % mutationType)
        return mutation
        
    def MutationTransposition(self):
        # 移调变换，随机选取一小节，将所有音在上下三度内移动
        indexOfStart = random.randint(0, 3) * 8
        while indexOfStart < 31 and self.notes[indexOfStart] < 2:
            indexOfStart += 1
        indexOfEnd = indexOfStart + 7   
        if indexOfEnd > 31:
            indexOfEnd = 31     
        
        mutation = deepcopy(self)
        deviation = random.randint(-4, 4)
        for index in range(indexOfStart, indexOfEnd + 1):
            if mutation.notes[index] > 1:
                mutation.notes[index] += deviation
                if mutation.notes[index] > 28:
                    mutation.notes[index] = random.randint(2, 28)
                elif mutation.notes[index] < 2:
                    mutation.notes[index] = random.randint(2, 28)
        return mutation
    
    def MutationInversion(self):
        # 倒影变换，随机选取一小节，以首音为基准倒影
        indexOfStart = random.randint(0, 3) * 8
        while indexOfStart < 31 and self.notes[indexOfStart] < 2:
            indexOfStart += 1
        indexOfEnd = indexOfStart + 7   
        if indexOfEnd > 31:
            indexOfEnd = 31     
            
        mutation = deepcopy(self)
        base = mutation.notes[indexOfStart]
        for index in range(indexOfStart, indexOfEnd + 1):
            if mutation.notes[index] < 2:
                continue
            deviation = mutation.notes[index] - base
            mutation.notes[index] -= (2 * deviation)
            if mutation.notes[index] < 2:
                mutation.notes[index] = random.randint(2, 28)
            elif mutation.notes[index] > 28:
                mutation.notes[index] = random.randint(2, 28)
        return mutation
    
    def MutationOctave(self):
        # 随机选取一个音，上移八度或下移八度
        target = random.randint(0, self.len - 1)
        while self.notes[target] < 2:
            target = random.randint(0, self.len - 1)
            
        mutation = deepcopy(self)
        upOrDown = (random.randint(0, 1) * 2) - 1     # 1 or -1
        mutation.notes[target] += (12 * upOrDown)
        if mutation.notes[target] > 28:
            mutation.notes[target] = random.randint(2, 28)
        elif mutation.notes[target] < 2:
            mutation.notes[target] = random.randint(2, 28)
        return mutation
    
    def MutationNote(self):
        # 随机选取一个音，上下四度内移动
        target = random.randint(0, self.len - 1)
        while self.notes[target] < 2:
            target = random.randint(0, self.len - 1)
            
        mutation = deepcopy(self)
        deviation = random.randint(-5, 5)
        mutation.notes[target] += deviation
        if mutation.notes[target] > 28:
            mutation.notes[target] = random.randint(2, 28)
        elif mutation.notes[target] < 2:
            mutation.notes[target] = random.randint(2, 28)
        return mutation
    
    def MutationRest(self):
        # 随机选取一个音变为休止
        target = random.randint(0, self.len - 1)
        while self.notes[target] < 2:
            target = random.randint(0, self.len - 1)

        mutation = deepcopy(self)
        mutation.notes[target] = 0
        return mutation
    
    def MutationExtension(self):
        # 随机选取一个音变为延音
        target = random.randint(0, self.len - 1)
        while self.notes[target] < 2:
            target = random.randint(0, self.len - 1)
        mutation = deepcopy(self)
        mutation.notes[target] = 1
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