__author__ = 'halley'
import random
import gencell as gc
from constants import *
from chunk import *
import genending

#gen continuationcadential phrase
def genContinuationCadential(prev_note = random.choice([2,4,7]), end_chords = [[0,2,4], [3,5,7], [4,6,8], [0,2,4]]):
    cords = [[0,2,4], [1,3,5],[4,6,8], [-2,0,2],[1,3,5],[0,2,4]]
    cells = []
    for i in range(0, 3):
        for j in range(0,2):
            cell_type = CHORDAL if random.uniform(0,1) < 0.5 else SCALEWISE
            chord = cords[i*2 + j]
            cell = gc.genCell(prev_note = prev_note, length=2.0, chord=chord, durs=[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25], cell_type=cell_type)
            for k in range(0,4):
                if (cell.pits[0] == cell.pits[2] and cell.pits[1] == cell.pits[3] or cell.pits[4] == cell.pits[6] and cell.pits[5] == cell.pits[7]):
                    cell = gc.genCell(prev_note = prev_note, length=2.0, chord=chord, durs=[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25], cell_type=cell_type)
            cells.append(cell)
            prev_note = cells[-1].pits[-1]

    end_chord_durs = [[0.75,0.25,0.75,0.25],[0.75,0.25,0.75,0.25],[0.5,0.5,0.5,0.5],[1.0]]
    for i in range(0, len(end_chords) - 1):
        cells.append(gc.genCell(prev_note = prev_note, length=2.0, chord=end_chords[i], durs=end_chord_durs[i], cell_type=CHORDAL))
        prev_note = cells[-1].pits[-1]
        if prev_note > 14:
                prev_note -= 3
    cells.append(genending.genEnding(prev_note, chord=[0,2,4], authentic=True))
    return Chunk(sub_chunks=cells)
