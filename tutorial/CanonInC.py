from musicpy import *

track1 = chord('E4, D4, C4, B3, A3, G3, A3, B3') % (2/4, 2/4)
track2 = chord('C3, G2, A2, E2, F2, G2, F2, G2') % (2/4, 2/4)
piece1 = piece(tracks=[track1, track2], bpm=62)

track3 = chord('G4, G4, E4, E4, C4, C4, C4, D4') % (2/4, 2/4)
track2 = track2
track1 = track1 + 12
piece2 = piece(tracks=[track1, track2, track3], bpm=62)

rhythm1 = [2/4, 1/4, 1/4, 2/4, 1/4, 1/4, 2/4, 1/4, 1/4, 2/4, 1/4, 1/4]
track1 = chord('E5, D5, F4, C5, B4, G4, A4, G4, E4, A4, G4, F4') % (rhythm1, rhythm1)
track2 = chord('G4, G4, F4, D4') % ([2/4, 1/4, 2/4, 1/4], [2/4, 1/4 + 9/4, 2/4, 1/4])
rhythm2 = [1/8] * 16
track3 = chord('C3, G3, C4, E4, B2, D3, G3, B3, A2, E3, A3, C4, E2, E3, G3, B3') % (rhythm2, rhythm2)
track4 = chord('F2, C3, F3, A3, C3, E3, G3, C4, F2, C3, F3, A3, G2, D3, G3, B3') % (rhythm2, rhythm2)
piece3 = piece(tracks=[track1, track2, track3 | track4], bpm=72)

track3 = chord('C3, E3, G3, C4, B2, D3, G3, B3, A2, E3, A3, C4, E2, E3, G3, B3') % (rhythm2, rhythm2)
track4 = track4
melody1 = 'C5, B4, C5, E4, G4, B4, C5, E5, G5, E5, G5, A5, F5, E5, D5, F5, E5, D5, C5, B4, A4, F4, C5, B4, G4, C5, B4'
rhythm1 = [1/8]*4 + [1/4]*4 + [1/8]*14 + [1/4] + [1/8]*4
track1 = chord(melody1) % (rhythm1, rhythm1)
piece4 = piece(tracks=[track1, track3 | track4], bpm=72)

Piece = piece1 | piece2 | piece3 | piece4

play(Piece, name='./output/CanonInC.mid')