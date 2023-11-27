from random import *
from .Melody import Melody

class Seed:
    def __init__(self, len=32, rhythm=None):
        self.melodyseed = []
        self.len = len
        self.rhythm = rhythm
        self.RandomMelody()
        
    def RandomMelody(self):
        for indexOfMelody in range(10):
            notes = []
            for indexOfNote in range(self.len):
                if indexOfNote == 0:    # 不能以延音，休止开始, 参考Converter.index2note
                    notes.append(randint(2, 28))
                else:
                    notes.append(randint(0, 28))
            melody = Melody(notes, self.len)
            self.melodyseed.append(melody)
        