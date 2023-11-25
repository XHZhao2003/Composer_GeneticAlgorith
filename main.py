from src.Seed import Seed
from src.Melody import Melody
from src.GeneticModel import GeneticModel
from numpy.random import multinomial
from src.Converter import Converter

# seed = Seed(len=32, rhythm=None)
# model = GeneticModel(seed, func='basic', population=10000, iter=100, threshold=1)
# model.forward()

# Convert best melodies into output midi
tie = [28] * 7
melody_list = [8] + tie + [12] + tie + [15] + tie + [19] + tie
melody = Melody(melody_list)
converter = Converter()
converter.ToMidi(melody, './output/test.mid')