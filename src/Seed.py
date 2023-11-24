from random import *
from .Melody import Melody

class Seed:
    def __init__(self, len=32, rhythm=None):
        self.index2note = {
            0: 'rest',
            1: 'F3',
            2: 'F#3',
            3: 'G3',
            4: 'G#3',
            5: 'A3',
            6: 'A#3',
            7: 'B3',
            8: 'C4',
            9: 'C#4',
            10: 'D4',
            11: 'D#4',
            12: 'E4',
            13: 'F4',
            14: 'F#4',
            15: 'G4',
            16: 'G#4',
            17: 'A4',
            18: 'A#4',
            19: 'B4',
            20: 'C5',
            21: 'C#5',
            22: 'D5',
            23: 'D#5',
            24: 'E5',
            25: 'F5',
            26: 'F#5',
            27: 'G5',
            28: 'tie'   # 延音
        }
        self.melodyseed = []
        self.len = len
        self.rhythm = rhythm
        self.RandomMelody()
        
    def RandomMelody(self):
        for indexOfMelody in range(10):
            notes = []
            for indexOfNote in range(self.len):
                if indexOfNote == 0:    # 不能以延音开始
                    notes.append(randint(0, 27))
                else:
                    notes.append(randint(0, 28))
            melody = Melody(notes, self.len)
            self.melodyseed.append(melody)
        