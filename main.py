from src.Seed import Seed
from src.Melody import Melody
from src.GeneticModel import GeneticModel
from numpy.random import multinomial
from src.Converter import Converter
from src.Interval import Interval

for experiment in range(30, 51):
    print("Experiment %d -----------------------------" % experiment)
    seed = Seed(len=32, rhythm=None)
    #model = GeneticModel(seed, func='basic', maxPopulation=15000, iter=300)
    model = GeneticModel(seed, func='model', maxPopulation=15000, iter=300)
    model.forward()
    
    # Convert best melodies into output midi
    converter = Converter()
    for i in range(10):
        name = './output/' + str(experiment) + '-' + str(i) + '.mid'
        converter.PrintNotes(model.population[i])
        converter.ToMidi(model.population[i], name)
