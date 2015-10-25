__author__ = 'halley'

import gencell as gc
import music21helpers as mh
import harmony as hm
from music21 import *

part1_cells = []
part2_cells = []

beginning_chords = [[0,2,4],[0,2,4],[4,6,8],[0,2,4]] #beginning chords

prev_note = 4
for i in range(0, len(beginning_chords)):
    part1_cells.append(gc.genCell(length = 2.0, chord=beginning_chords[i]))
    part2_cells.append(gc.genBlankCell(2.0))

for i in range(0,10):
    prev_part = part1_cells[-4:]
    for j in range(0, len(prev_part)):
        new_cell = gc.genCell(prev_note = part1_cells[-1].pits[-1], length = 2.0, chord=prev_part[j].chord)
        while not (hm.chunkMatches(new_cell, prev_part[j])):
            new_cell = gc.genCell(prev_note = part1_cells[-1].pits[-1], length = 2.0, chord=prev_part[j].chord)
        part1_cells.append(new_cell)
        part2_cells.append(prev_part[j])
        print('i = ' + str(i) + ' j = ' + str(j))

part1 = mh.cellsToPart(part1_cells)
part2 = mh.cellsToPart(part2_cells, octave=3)

s = stream.Stream()
s.insert(0,part1)
s.insert(0, part2)

s.show()