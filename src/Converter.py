from .Melody import Melody
from musicpy import *

class Converter:
    def __init__(self):
        self.index2note = {
            0: '0',  # 休止
            1: '-',   # 延音
            2: 'F3',
            3: 'F#3',
            4: 'G3',
            5: 'G#3',
            6: 'A3',
            7: 'A#3',
            8: 'B3',
            9: 'C4',
            10: 'C#4',
            11: 'D4',
            12: 'D#4',
            13: 'E4',
            14: 'F4',
            15: 'F#4',
            16: 'G4',
            17: 'G#4',
            18: 'A4',
            19: 'A#4',
            20: 'B4',
            21: 'C5',
            22: 'C#5',
            23: 'D5',
            24: 'D#5',
            25: 'E5',
            26: 'F5',
            27: 'F#5',
            28: 'G5',
        }
        self.beatUnit = 1/8
        
    # 接受一个Melody对象，转换并生成midi文件
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
                if note == 0:   # 休止
                    tempInterval += self.beatUnit
                elif note == 1:   # 延音
                    tempDuration += self.beatUnit
                    tempInterval += self.beatUnit
                elif note > 1 and note < 29:
                    duration.append(tempDuration)
                    interval.append(tempInterval)
                    tempDuration = self.beatUnit
                    tempInterval = self.beatUnit
                    midiNote.append(self.index2note[note])
                else:
                    raise ValueError("Unexpected note %d" % note)
        duration.append(tempDuration)
        interval.append(tempInterval)
        midiNote = ','.join(midiNote)
        
        track1 = chord(midiNote) % (duration, interval)
        play(track1, bpm=bpm, name=name)                    

    def PrintNotes(self, melody: Melody):
        notes = []
        temp = ''
        for note in melody.notes:
            if note > -1 and note < 29:
                temp = self.index2note[note]
            else:
                raise ValueError("Unexpected note %d" % note)
            notes.append(temp)
        notes = ' '.join(notes)
        print(notes)