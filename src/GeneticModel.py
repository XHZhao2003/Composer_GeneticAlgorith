from .Seed import Seed
from .Melody import Melody
from numpy.random import multinomial

class GeneticModel:
    # 参数: 初始片段，适应度函数种类，种群最大规模，迭代次数，停止迭代的阈值
    def __init__(self, seed : Seed, func='basic', population=10000, iter=100, threshold=1):
        self.population = seed.melodyseed
        self.scoreFunction = func 
        self.maxPopulation = population
        self.maxIter = iter
        self.prob = [0.7, 0.1, 0.1, 0.1]    # 无变异，八度变异，音符变异，交换变异
        
    def forward(self):
        population = self.population
        for iter in range(self.maxIter):
            # 参考文献中阐述了若干不使用crossover的理由，子代完全基于父代变异
            newPopulation = []
            Score = []              # 父代适应度，归一化
            randomSelection = []    # 多项分布随机出父代个体被选中的次数
            
            for (indiv, index) in population:
                for i in range(randomSelection[index]):
                    mutation = self.mutate(indiv)
                    newPopulation.append(mutation)
            
            for indev in newPopulation: 
                if self.scoreFunction == 'basic':
                    pass    # 更新适应度        
                elif self.scoreFunction == 'something else, CNN/RNN':
                    pass    # 更新适应度
            population = newPopulation     
            
            # 将population按适应度排序
            # if best_individual.score > threshold:
            #       self.population = population
            #       break
        
        self.population = population
    
    
    def mutate(self, melody:Melody):
        randomMutate = multinomial(1, self.prob)
        mutation = melody
        if randomMutate[0] == 1:
            return mutation
        elif randomMutate[1] == 1:
            pass    # 八度变异
        elif randomMutate[2] == 1:
            pass    # 音符变异
        elif randomMutate[3] == 1:
            pass    # 交换相邻音符
        
        return mutation
    
    