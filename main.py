from src.Seed import Seed
from src.GeneticModel import GeneticModel
from numpy.random import multinomial

seed = Seed(len=32, rhythm=None)
model = GeneticModel(seed, func='basic', population=10000, iter=100, threshold=1)
model.forward()

# Convert best melodies into output midi
