__author__ = 'halley'
from inspect import getmembers, isfunction
import celltransforms as ct
import random
import preferences as pref
import harmony as hm
import transpose
import functionalhelpers as fh
import motiftransforms as mt
import gencell as gc
import rhythmhelpers as rhy
from chunk import *
import genending

transform_cell_function_names = ['scalewiseRunSameRhythmSameDir', 'scalewiseRunDiffRhythmSwitchDir','retrogradeChangeLastPitch',
                                 'inversion', 'retrogradePitches', 'sameCtypeDifferentDur', 'identity', 'partialTranspose', 'partialRetrograde']

#the list of functions
transform_cell_functions = dict([(o[0], o[1]) for o in getmembers(ct) if isfunction(o[1])])

transform_motif_function_names = ['transformFirstCellTwice', 'transformSecondCellTwice', 'transformFirstChangeSecond', 'switchFirstSecond',
                                  'transformFirstSecond']

transform_motif_functions = dict([(o[0], o[1]) for o in getmembers(mt) if isfunction(o[1])])

#transform a motif
def transformMotif(transform_motif, prev_cell = gc.genBlankCell(2.0), chords = [[0,2,4],[0,2,4]]):
    whichFunction = transform_motif_functions[random.choice(transform_motif_function_names)]
    return whichFunction(transform_motif, prev_cell, chords)

#transform a cell
def transformCell(transformed_cell, prev_cell = gc.genBlankCell(2.0), chord = [0,2,4]):
    random.shuffle(transform_cell_function_names)
    function_index = 0
    while True:
        function_index += 1
        if function_index >= len(transform_cell_function_names):
            return gc.genCell(length=2.0, chord=chord, durs=rhy.alterRhythm(transformed_cell.durs))
        else:
            attempting_cells = transform_cell_functions[transform_cell_function_names[function_index]](transformed_cell, chord, prev_cell.pits[-1], random.choice([-1,1]))
            random.shuffle(attempting_cells)
            if not hm.inChord(prev_cell.pits[-1], prev_cell.chord):
                attempting_cells = filter(lambda i: abs(i.pits[0] - prev_cell.pits[-1]) < 2, attempting_cells)
            for attempting_cell in attempting_cells:
                attempting_cell.chord = chord
                if hm.chunkInChord(attempting_cell, chord) and pref.goodCells([prev_cell, attempting_cell]):
                    return attempting_cell
            transposed_attempting_cells = fh.concat([transpose.transposeToNewStart(prev_cell, new_cell) for new_cell in attempting_cells])
            if not hm.inChord(prev_cell.pits[-1], prev_cell.chord):
                transposed_attempting_cells = filter(lambda i: abs(i.pits[0] - prev_cell.pits[-1]) < 2, transposed_attempting_cells)
            for transposed_attempting_cell in transposed_attempting_cells:
                transposed_attempting_cell.chord = chord
                if hm.chunkInChord(transposed_attempting_cell, chord) and pref.goodCells([prev_cell, transposed_attempting_cell]):
                    return transposed_attempting_cell

def alterBasicIdea(bi, prev_note = random.choice([0,2,4,7]), chords = [[0,2,4],[0,2,4],[1,3,5],[0,2,4]], cadence = 'None', real_end = False):
    motif1 = transformMotif(transform_motif=bi.cells[:2], prev_cell= Chunk(pits=[prev_note], durs=[-2.0]), chords=chords[:2])
    if cadence == 'None':
        motif2 = transformMotif(transform_motif=bi.cells[2:], prev_cell = Chunk(pits=[motif1[-1].pits[-1]], durs=[-2.0]), chords=chords[2:])
    else:
        cell21 = transformCell(transformed_cell=bi.cells[2], prev_cell=Chunk(pits=[motif1[-1].pits[-1]], durs = [-2.0]), chord=chords[2])
        cell22 = genending.genEnding(cell21.pits[-1], chord=chords[-1], authentic=cadence == 'authentic', real_end = real_end)
        motif2 = [cell21] + [cell22]
    return Chunk(sub_chunks=motif1 + motif2)
