from .Seed import Seed
from .Melody import Melody
import numpy as np
from numpy.random import multinomial

class GeneticModel:
    # 参数: 初始片段，适应度函数种类，种群最大规模，迭代次数，停止迭代的阈值
    def __init__(self, seed : Seed, func='basic', maxPopulation=10000, iter=100, threshold=1):
        self.population = seed.melodyseed
        self.scoreFunction = func 
        self.maxPopulation = maxPopulation
        self.maxIter = iter
        self.prob = [0.95, 0.01, 0.03, 0.01]    # 无变异，八度变异，音符变异，交换变异
        
    def forward(self):
        for indiv in self.population:
            indiv.GetScore()
            
        population = self.population
        for iter in range(self.maxIter):
            mutation_cnt = [0, 0, 0, 0]
            # 参考文献中阐述了若干不使用crossover的理由，子代完全基于父代变异
            newPopulation = []
            
            # 多项分布随机出父代个体被选中的次数
            Score = []
            for indiv in population:
                Score.append(1.0 / indiv.score)
            Score = np.array(Score)
            scoreSum = np.sum(Score)
            Score = Score / scoreSum
            randomSelection = multinomial(self.maxPopulation, Score)
            
            # 基于变异产生子代
            for index, indiv in enumerate(population):
                # 这一个体产生各种变异的数量
                mutationNumbers = multinomial(randomSelection[index], self.prob)
                for mutationType, mutationNumber in enumerate(mutationNumbers):
                    mutation_cnt[mutationType] += mutationNumber
                    for _ in range(mutationNumber):        # 每种变异产生mutationNumber个
                        mutation = indiv.GetMutation(mutationType)
                        newPopulation.append(mutation)
            
            # newPopulation = list(newPopulation)
            for indiv in newPopulation: 
                indiv.GetScore()
            newPopulation.sort()
            population = newPopulation     
            
            print("第%d代遗传: 最小适应度 %f, 产生变异%d, %d, %d, %d次" % 
                  (iter + 1, population[0].score, mutation_cnt[0], mutation_cnt[1], mutation_cnt[2], mutation_cnt[3]))
        population = list(set(population))
        population.sort()
        self.population = population
    
    
    
    