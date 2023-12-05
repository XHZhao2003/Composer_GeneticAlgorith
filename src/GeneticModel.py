from .Seed import Seed
from .Melody import Melody
import torch
import numpy as np
from numpy.random import multinomial
from torch import Tensor, nn
from tqdm import tqdm

class GeneticModel:
    # 参数: 初始片段，适应度函数种类，种群最大规模，迭代次数，停止迭代的阈值
    def __init__(self, seed : Seed, func='basic', maxPopulation=10000, iter=100):
        self.population = seed.melodyseed
        self.scoreFunction = func 
        self.maxPopulation = maxPopulation
        self.maxIter = iter
        self.function = func
        self.model = None
        self.prob = [0.99, 0.003, 0.003, 0.001, 0.001, 0.001, 0.001]    # 无变异，移调，倒影，八度，音符，延长，休止

        if self.function == "model":
            self.model = torch.load("src/CNN/model.pt")
            self.prob = [0.8, 0.01, 0.01, 0.01, 0.15, 0.01, 0.01]        
        
    def forward(self):
        for indiv in self.population:
            indiv.score = 1
            
        population = self.population
        for iter in tqdm(range(self.maxIter), ncols=80, total=self.maxIter):
            # 参考文献中阐述了若干不使用crossover的理由，子代完全基于父代变异
            newPopulation = []
            
            # 多项分布随机出父代个体被选中的次数
            Score = []
            for indiv in population:
                Score.append(1.0 / (indiv.score + 1e-3))
            Score = np.array(Score)
            scoreSum = np.sum(Score)
            Score = Score / scoreSum
            randomSelection = multinomial(self.maxPopulation, Score)
            
            # 基于变异产生子代
            for index, indiv in enumerate(population):
                # 这一个体产生各种变异的数量
                mutationNumbers = multinomial(randomSelection[index], self.prob)
                for mutationType, mutationNumber in enumerate(mutationNumbers):
                    for _ in range(mutationNumber):        # 每种变异产生mutationNumber个
                        mutation = indiv.Mutation(mutationType)
                        newPopulation.append(mutation)
            
            # newPopulation = list(newPopulation)
            if self.function == 'basic':
                for indiv in newPopulation: 
                    indiv.GetScore()
            elif self.function == 'model':
                # 求所有个体的评分
                for indiv in newPopulation: 
                    indiv.GetScore()
                self.model.TestMode()
                notesList = Tensor([[indiv.notes] for indiv in newPopulation])
                logits = self.model(notesList)
                softmax = nn.Softmax(dim=1)
                scores = softmax(logits)
                for index, indiv in enumerate(newPopulation):
                    indiv.score += scores[index][1].item()
                
            newPopulation.sort()
            population = newPopulation     
            
            tqdm.write("%d-th Generation: best score: %f" % (iter + 1, population[0].score))
        population = list(set(population))
        population.sort()
        self.population = population
    
    
    
    