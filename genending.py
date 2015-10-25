import random
import pitchhelpers as pth
import scale as sc
from chunk import *
import gencell as gc
import music21helpers as mh
import pitchhelpers as pth

#generate an ending for a phrase
def genEnding(prev_note, chord = [0,2,4], authentic = True, elided = False, real_end = False):
    if real_end:
        return Chunk(pits=[pth.getClosestPCDegree(prev_note, 0)], durs=[2.0])
    dur = random.choice([0,1, 2,3,4]) if elided else random.choice([0,3,4])
    durs = []
    pitches = []
    if chord == [0,2,4]:
        if authentic:
            last_note = 0
        else:
            last_note = sc.closestNoteDegreeInChord(note = prev_note, chord=[2,4])
    else:
        last_note = random.choice([4,8])
    if dur == 0:
        durs = [0.5,0.5,1.0]
        if prev_note - pth.getClosestPCDegree(prev_note, last_note) == 0:
            pitches = random.choice([[prev_note - 1, prev_note + 1, prev_note], [prev_note + 1, prev_note - 1, prev_note]])
        elif pth.getClosestPCDegree(prev_note, last_note) - prev_note == 1:
            pitches = [prev_note + 1, prev_note + 2, prev_note + 1]
        elif pth.getClosestPCDegree(prev_note, last_note) - prev_note == -1:
            pitches = [prev_note - 1, prev_note - 2, prev_note - 1]
        else:
            pitches = [sc.closestNoteDegreeInChord(prev_note, chord, False)]
            pitches.append(sc.closestNoteDegreeInChord(pth.getClosestPCDegree(prev_note, last_note), chord, False))
            pitches.append(pth.getClosestPCDegree(prev_note, last_note))
    elif dur == 1:
        durs = [1.0,1.0]
        pitches = [pth.getClosestPCDegree(prev_note, last_note)]
        pitches.append(random.randint(3,7))
    elif dur == 2:
        durs = [1.0, -0.5, 0.5]
        pitches = [pth.getClosestPCDegree(prev_note, last_note)]
        pitches.append(-36)
        pitches.append(random.randint(3,7))
    elif dur == 3:
        durs = [1.0, -1.0]
        pitches = [pth.getClosestPCDegree(prev_note, last_note), -36]
    elif dur == 4:
        durs = [2.0]
        pitches = [pth.getClosestPCDegree(prev_note, last_note)]
    return Chunk(pitches, durs)
"""
cells = []
for i in range(0, 16):
    cells.append(gc.genCell(length = 2.0, chord=[4,6,8]))
    cells.append(genEnding(cells[-1].pits[-1], random.choice([[4,6,8], [0,2,4]]), random.choice([True, False])))

mh.showCells(cells)
"""