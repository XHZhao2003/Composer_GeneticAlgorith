from functools import total_ordering
from .Interval import Interval
import random
from copy import deepcopy
import numpy as np
from scipy.spatial import distance

@total_ordering
class Melody:
    def __init__(self, notes: list, length=32):
        self.notes = notes
        self.len = length
        self.score = 0     
        assert self.len == len(self.notes)
        
    def GetScore(self): 
        self.score = 0
        # IntervalMean, IntervalVariance, Rhythm, Tonality, SelfSimilarity
        alpha = [0.5, 0.2, 0.1, 2, 2]
        fit1, fit2 = self.GetIntervalScore(zeta=[1.0, 1.0, 1.0, 1.0], eta=[1.0, 1.0, 1.0, 1.0])
        fit3 = self.GetRhythmSimilarity()
        fit4 = 1 - self.GetTonality()
        fitness = [fit1, fit2, fit3, fit4]

        # feature = [self.GetSelfSimilarity(), self.GetLinearity(), self.GetTonality(),self.GetPitchDistribution()]
        # featureScore = [0.05, 0.5, 1.0, 0.9]
        feature = self.GetSelfSimilarity()
        featureReference = 2.0
        fitness.append(self.FeatureScore(featureReference, feature))
        for i in range(len(alpha)):
            self.score += alpha[i] * fitness[i]

    def GetIntervalScore(self, zeta=[1.0, 1.0, 1.0, 1.0], eta=[1.0, 1.0, 1.0, 1.0]):
        # 对所有相邻音程评分，按照小节为单位求平均和方差,据此算出适应度函数f1和f2
        interval = Interval()
        note1 = 0
        note2 = 0
        interval_xi, mean, variation = [], [], []

        for start in range(0, self.len, 8):
            index1 = start
            index2 = start + 1
            interval_xi = []
            while index1 < start + 8 and index2 < start + 8:
                if self.notes[index1] < 2:
                    index1 += 1
                    index2 += 1
                    continue
                if self.notes[index2] < 2:
                    index2 += 1
                    continue
                note1, note2 = self.notes[index1], self.notes[index2]
                interval_xi.append(interval.ScoreTwoNote(note1, note2))
                index1 += 1
                index2 += 1
            mean.append(np.mean(interval_xi))
            variation.append(np.var(interval_xi))
        referenceMean = [1.0, 1.0, 1.0, 1.0]
        referenceVariation = [0, 0.2, 0.2, 0]
        f1, f2 = 0.0, 0.0

        for i in range(4):
            f1 += zeta[i] * abs(referenceMean[i] - mean[i])
            f2 += eta[i] * abs(referenceVariation[i] - variation[i])
        return f1, f2
    
    def GetSelfSimilarity(self):
        # 计算自相似度————相同的音程出现的越频繁，自相似度越高
        cnt = [0] * 13      # 纯一度-纯八度
        intervalSum = 0
        notes = []
        for note in self.notes:
            if note >= 2 and note <= 28:
                notes.append(note)
        for i in range(len(notes) -1):
            intervalSum += 1
            interval = int(abs(notes[i + 1] - notes[i]))
            if interval < 12:
                cnt[interval] += 1
        score = 0
        for x in cnt:
            if x > 0:
                score += 1
        score = intervalSum / score
        return score
        
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
            hit = 0
            for note in self.notes:
                if note < 2:
                    continue
                if note % 12 in key:
                    hit += 1
            keyPrevalence.append(hit / self.len)
        return max(keyPrevalence) - (1 - max(keyPrevalence))/(self.len-1)

    def GetRhythmSimilarity(self):
        # 计算四小节的节奏相似度,越大越不相似————利用Minkowski Distance
        rhythmSimilarity = 0.0
        rhythm = []
        hand = 0
        for i in range(0, self.len, 8):
            rhythm.append([])
            for j in range(i, i + 8):
                if self.notes[j] > 1:
                    rhythm[hand].append(2)
                else:
                    rhythm[hand].append(self.notes[j])
            hand += 1
        for i in range(4):
            for j in range(i + 1, 4):
                rhythmSimilarity += distance.minkowski(rhythm[i], rhythm[j], 2)
        return rhythmSimilarity
       
    def FeatureScore(self, t, eI):
        # 将特征值转化为得分
        return 1 / (1e-3 + (eI - t) ** 2)

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