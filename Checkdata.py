# 播放所收集到的数据
# 数据存放在 data/song.txt中，          
# 输出的一系列音频存放在 data/midi/中   

from src.Melody import Melody
from src.Converter import Converter
from sys import argv

sourcepath = 'data/song.txt'
destpath = ''
sourceFile = 0
destFile = 0

argc = len(argv)
if argc > 1:
    assert argc == 3        # python Checkdata.py   source.txt  dest.txt
    sourcepath = argv[1]
    destpath = argv[2]
    destFile = open(destpath, 'w')
sourceFile = open(sourcepath, 'r')

index = 0
converter = Converter()

while True:
    notes = sourceFile.readline()
    if not notes:
        break
    
    notes = notes.split()
    if argc == 3:
        notes = [converter.note2index[note] for note in notes]
    else:
        notes = [int(note) for note in notes]
    if len(notes) != 32:
        raise ValueError("Unexpected length of this piece, with length %d" % len(notes))
    melody = Melody(notes, len(notes))
    converter.PrintNotes(melody)
    outputPath = 'data/midi/' + str(index) + '.mid'
    converter.ToMidi(melody, outputPath)
    index += 1 
print("Already Get %d pieces" % index)  
sourceFile.close()
if destFile != 0:
    destFile.close()