# 播放所收集到的数据
# 数据存放在 data/song.txt中，          
# 输出的一系列音频存放在 data/midi/中   

from musicpy import *
from src.Melody import Melody
from src.Converter import Converter

datapath = 'data/song.txt'
index = 0
converter = Converter()

with open(datapath, 'r') as f:
    while True:
        notes = f.readline()
        if not notes:
            break
        notes = notes.split()
        notes = [int(note_) for note_ in notes]
        melody = Melody(notes, len(notes))
        converter.PrintNotes(melody)
        outputPath = 'data/midi/' + str(index) + '.mid'
        converter.ToMidi(melody, outputPath)
        index += 1
        
print("Already Get %d pieces" % index)
        