__author__ = 'halley'
import gencell as gc
from constants import *
from chunk import *
import copy
import random

#create neighbor tones passage that begins and ends with note and lasts beat_length long
def getNeighborTones(beat_length, note):
    which_type = random.uniform(0,1)
    if beat_length == 2.0:
        if which_type < 0.2:
            return ([note, note + 1, note], [1.5,0.25,0.25])
        elif which_type < 0.4:
            return ([note, note - 1, note], [1.5,0.25,0.25])
        elif which_type < 0.6:
            return ([note, note + 1, note - 1, note], [0.5,0.5,0.5,0.5])
        elif which_type < 0.8:
            return ([note, note - 1, note + 1, note], [0.5,0.5,0.5,0.5])
        elif which_type < 0.9:
            return ([note, note + 1, note], [1,0.5,0.5])
        else:
            return ([note, note - 1, note], [1,0.5,0.5])
    elif beat_length == 1.0:
        if which_type < 0.25:
            return ([note, note + 1, note], [0.5, 0.25,0.25])
        elif which_type < 0.5:
            return ([note, note - 1, note], [0.5,0.25,0.25])
        elif which_type < 0.7:
            return ([note, note + 1, note - 1, note], [0.25,0.25,0.25,0.25])
        elif which_type < 0.9:
            return ([note, note - 1, note + 1, note], [0.25,0.25,0.25,0.25])
        else:
            return ([note + 3, note + 2, note + 1, note], [0.25,0.25,0.25,0.25])
    else:
        print('error: getNeighborTones called with beat_length != 1.0 or 2.0')

#tutti passage, with melody, bass, and accompaniment
def insertTutti(instr_cells, passage, tutti_cells):
    for instr in instrs:
        if instr not in tutti_cells:
            for cell in passage.cells:
                instr_cells[instr].append(gc.genBlankCell(2.0))
        else:
            if instr in tutti_bass:
                for main_cell in passage.cells:
                    if main_cell.chord == None or main_cell.chord == []:
                        pits = [0]
                        durs = [-2.0]
                    else:
                        pits = [main_cell.chord[0]]
                        durs = [2.0]
                    instr_cells[instr].append(Chunk(pits=pits, durs=durs, chord=main_cell.chord, key=main_cell.key))
            elif instr in tutti_accomp:
                for main_cell in passage.cells:
                    pits = []
                    durs = []
                    for i in range(0, len(main_cell.beat_durs)):
                        beat = main_cell.beat_durs[i]
                        if (beat == [1.0] or beat == [2.0]) and random.uniform(0,1) < 0.2:
                            new_pits, new_durs = getNeighborTones(beat[0], main_cell.beat_pits[i][0])
                            pits.extend(new_pits)
                            durs.extend(new_durs)
                        else:
                            pits.append(0)
                            durs.append(sum(beat)*-1)
                    instr_cells[instr].append(Chunk(pits=pits, durs=durs, chord=main_cell.chord, key=main_cell.key))
            else: #if instr is main melody
                for main_cell in passage.cells:
                    instr_cells[instr].append(copy.deepcopy(main_cell))