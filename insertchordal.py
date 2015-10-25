__author__ = 'halley'
from constants import *
import rhythmhelpers as rhy
from chunk import *
import random

voicing_index = {}
voicing_index['b'] = 0
voicing_index['t'] = 1
voicing_index['a'] = 2
voicing_index['s'] = 3

def insertChordal(instr_cells):
    chords = [(0,[0,2,4]), (1, [1,3,5]), (0, [3,5,7]), (0, [4,6,8,3])]
    voicings = [(7,-3,2,7), (10, 1, 3, 5), (10, 0, 5, 7), (11, 1, 3, 6)]
    rhythms = []
    for i in range(0, len(voicings)):
        new_rhy = random.choice([[1.0,1.0], [1.0,0.5,0.25,0.25], [1.5,0.25,0.25], [1.5,0.5], [0.75,0.25,0.5,0.5], [1.0,0.75,0.25]])
        rhythms.append(new_rhy)

    for i in range(0, len(voicings)):
        rhythm = rhythms[i]
        voicing = voicings[i]
        for instr in instrs:
            cell_rhythm = rhythm
            cell_pitches = [voicing[voicing_index[satb[instr]]] for note in rhythm]
            new_cell = Chunk(pits = cell_pitches, durs=cell_rhythm)
            instr_cells[instr].append(new_cell)

