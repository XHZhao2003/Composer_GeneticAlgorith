from musicpy import *

# musicpy中最简单的数据结构是note
G4_sharp = note('G#', 4)                            # 定义了G#4音符
G4_sharp = note('G#', 4, duration=1)                # 定义了更长的音符，时值长一小节，不指定时值默认是一拍，这里改成了4拍
                                                    # musicpy中的一小节默认是4/4拍下的
G4_sharp = N('G#4', duration=1)                     # 另一种写法
play(G4_sharp, name='./output/note.mid', bpm=80)    # 输出一个midi文件，只包含一个音符

# musicpy中最主要的数据结构是chord
Cmaj = chord('C4, E4, G4')                          # 定义一个大三和弦
Cmaj = get_chord('C4', 'maj')                      # 指定根音与和弦名称定义大三和弦
Cmaj = get_chord('C4', 'maj') % (1, 0)              # (1, 0) 表示三和弦中的每个音符时值都是1，三个音符时间上的间隔是0
Cmaj_scale = get_chord('C4', 'maj') % (1/4, 1/4)    # 时值间隔都是1/4，效果是依次演奏                       
play(Cmaj, bpm=80, name='./output/Cmaj.mid')
play(Cmaj_scale, bpm=80, name='./output/Cmaj_scale.mid')


Cmaj = get_chord('C4', 'maj') % (1, 0)
Dmaj = get_chord('D4', 'maj') % (1, 0)
Emaj = get_chord('E4', 'maj') % (1, 0)
Fmaj = get_chord('F4', 'maj') % (1, 0)
Gmaj = get_chord('G4', 'maj') % (1, 0)
Amaj = get_chord('A4', 'maj') % (1, 0)
Bmaj = get_chord('B4', 'maj') % (1, 0)

# 卡农
track0 = chord('F#5, E5, D5, C#5, B4, A4, B4, C#5') % (1, 1)

track_1 = chord('D3, A3, D4, F#4') % (1/4, 1/4)
track_2 = chord('A2, E3, A3, C#4') % (1/4, 1/4)
track_3 = chord('B2, F#3, B4, D4') % (1/4, 1/4)
track_4 = chord('F#2, C#3, F#3, A3') % (1/4, 1/4)
track_5 = chord('G2, D3, G3, B3') % (1/4, 1/4)
track_6 = chord('D2, A2, D3, F#3') % (1/4, 1/4)
track_7 = chord('G2, D3, G4, B4') % (1/4, 1/4)
track_8 = chord('A2, E3, A3, C#4') % (1/4, 1/4)
# 连接旋律
track1 = track_1 | track_2 | track_3 | track_4 | track_5 | track_6 | track_7 | track_8

# 作为乐曲的的数据结构
canon = piece([track0, track1], bpm=120, start_times=[0, 0], 
              instruments=['Acoustic Grand Piano', 'Acoustic Grand Piano'])
play(canon, name='./output/canon.mid')


