from src.Seed import Seed
from src.Melody import Melody
from src.GeneticModel import GeneticModel
from numpy.random import multinomial
from src.Converter import Converter
from src.Interval import Interval
import numpy as np


seed = Seed(len=32, rhythm=None)
model = GeneticModel(seed, func='basic', maxPopulation=10000, iter=800, threshold=1)
model.forward()
    
# Convert best melodies into output midi
converter = Converter()
for i in range(10):
    name = './output/' + str(i) + '.mid'
    converter.PrintNotes(model.population[i])
    converter.ToMidi(model.population[i], name)
