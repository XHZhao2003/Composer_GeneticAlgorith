from .Melody import Melody
from musicpy import *

class Converter:
    def __init__(self):
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
        self.beatUnit = 1/8

    def ToMidi(self, melody: Melody, name, bpm=80):
        notes = melody.notes
        length = melody.len
        midiNote = []
        duration = []
        interval = []
        
        tempDuration = self.beatUnit
        tempInterval = self.beatUnit
        
        for index, note in enumerate(notes):
            if index == 0:
                midiNote.append(self.index2note[note])
                tempDuration = self.beatUnit
            else:
                if note == 28:
                    tempDuration += self.beatUnit
                    tempInterval += self.beatUnit
                elif note < 28 and note > 0:
                    duration.append(tempDuration)
                    interval.append(tempInterval)
                    tempDuration = self.beatUnit
                    tempInterval = self.beatUnit
                    midiNote.append(self.index2note[note])
                elif note == 0:
                    tempInterval += self.beatUnit
                else:
                    raise ValueError("Unexpected note %d" % note)
        duration.append(tempDuration)
        interval.append(tempInterval)
        midiNote = ','.join(midiNote)
        
        track1 = chord(midiNote) % (duration, interval)
        play(track1, bpm=bpm, name=name)                    
