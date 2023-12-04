from functools import total_ordering
from .Interval import Interval
from torch import Tensor
from .CNN.CNNModel import CNNModel
import random
from copy import deepcopy

@total_ordering
class Melody:
    def __init__(self, notes: list, length=32):
        self.notes = notes
        self.len = length
        self.score = 0     # 适应度
        assert self.len == len(self.notes)
        
    def GetScore(self, function='basic', model=None): 
        if function == 'basic':
            lambda1 = 0.5
            lambda2 = 1.0
            score1 = self.GetIntervalScore()    
            score2 = self.GetScaleScore()    
            self.score = lambda1 * score1 + lambda2 * score2 
        elif function == 'CNN':
            assert model != None
            notes = Tensor([self.notes])
            pred = model(notes)[0]
            self.score = pred[1]      # 模型预测为负样本的概率

    def GetIntervalScore(self):
        # 对所有相邻音程评分，取平均
        interval = Interval()
        note1 = 0
        note2 = 0
        cnt = 0
        score1 = 0
        index = 0
        while self.notes[index] < 2:
            index += 1
        note1 = self.notes[index]
        
        for i in range(index + 1, self.len):
            if self.notes[i] < 2:
                continue
            note2 = self.notes[i]
            score1 += interval.ScoreTwoNote(note1, note2)
            cnt += 1
            note1 = note2
        score1 = score1 / cnt
        return score1

    def GetScaleScore(self):
        # 旋律中的调内音越多，适应度越好(越低)
        # 统计G大调中的调内音 (G, A, B, C, D, E, F#)
        cnt = 0
        inTonality = 0
        Gmaj = [4, 6, 8, 9, 11, 1, 3]       # mod 12
        for note in self.notes:
            if note > 0 and note < 28:
                cnt += 1
                if (note % 12) in Gmaj:
                    inTonality += 1
        score2 = 1 - inTonality / cnt
        return score2

    
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
                    mutation.notes[index] = 28
                elif mutation.notes[index] < 2:
                    mutation.notes[index] = 2
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
                mutation.notes[index] = 2
            elif mutation.notes[index] > 28:
                mutation.notes[index] = 28
        return mutation
    
    def MutationOctave(self):
        # 随机选取一个音，上移八度或下移八度
        target = random.randint(0, self.len - 1)
        while self.notes[target] < 2:
            target = random.randint(0, self.len - 1)
            
        mutation = deepcopy(self)
        upOrDown = random.randint(0, 1) * 2 - 1     # 1 or -1
        mutation.notes[target] += 12 * upOrDown
        if mutation.notes[target] > 28:
            mutation.notes[target] = 28
        elif mutation.notes[target] < 2:
            mutation.notes[target] = 2
        return mutation
    
    def MutationNote(self):
        # 随机选取一个音，上下五度内移动
        target = random.randint(0, self.len - 1)
        while self.notes[target] < 2:
            target = random.randint(0, self.len - 1)
            
        mutation = deepcopy(self)
        deviation = random.randint(-7, 7)
        mutation.notes[target] += deviation
        if mutation.notes[target] > 28:
            mutation.notes[target] = 28
        elif mutation.notes[target] < 2:
            mutation.notes[target] = 2
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