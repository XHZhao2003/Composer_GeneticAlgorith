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
        self.note2index = {
            '0':    0,  # 休止
            '-':    1,   # 延音
            'F3':   2,
            'F#3':  3,
            'G3':   4 ,
            'G#3':  5,
            'A3':   6,
            'A#3':  7,
            'B3':   8,
            'C4':   9,
            'C#4':  10,
            'D4':   11,
            'D#4':  12,
            'E4':   13,
            'F4':   14,
            'F#4':  15,
            'G4':   16,
            'G#4':  17,
            'A4':   18,
            'A#4':  19,
            'B4':   20,
            'C5':   21,
            'C#5':  22,
            'D5':   23,
            'D#5':  24,
            'E5':   25,
            'F5':   26,
            'F#5':  27,
            'G5':   28
        }
        self.beatUnit = 1/8
        
    # 接受一个Melody对象，转换并生成midi文件
    def ToMidi(self, melody: Melody, name, bpm=80):
        notes = melody.notes
        length = melody.len
        midiNote = []
        duration = []
        interval = []
        
        startTime = 0
        tempNote = 0
        tempNoteEnd = 0         # 当前音符是否结束，判断例如 C4 - 0 - 中 Duaration=2 Interval=4
        tempDuration = self.beatUnit
        tempInterval = self.beatUnit
        index = 0
        
        # 处理休止符开头的情形
        while index < len(notes) and notes[index] < 2:
            startTime += self.beatUnit
            index += 1
            
        while index < len(notes):
            curNote = notes[index]
            if curNote == 0:
                tempInterval += self.beatUnit
                tempNoteEnd = 1
            elif curNote == 1:
                tempInterval += self.beatUnit
                if tempNoteEnd == 0:
                    tempDuration += self.beatUnit
            elif curNote > 1 and curNote < 29:
                if tempNote > 0:
                    midiNote.append(self.index2note[tempNote])
                    duration.append(tempDuration)
                    interval.append(tempInterval)
                tempNote = curNote
                tempNoteEnd = 0
                tempDuration = self.beatUnit
                tempInterval = self.beatUnit
            else:
                raise ValueError("Unexpected note %d" % curNote)
            index += 1
        midiNote.append(self.index2note[tempNote])
        duration.append(tempDuration)
        interval.append(tempInterval)

        midiNote = ','.join(midiNote)
        
        track1 = chord(midiNote) % (duration, interval)
        play(track1, bpm=bpm, name=name, start_time=startTime)                    

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