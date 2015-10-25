__author__ = 'halley'
import probabilityhelpers as ph
import random
import scale as sc
from chunk import *
import pitchhelpers as pth
import accompaniment as accomp

#generate a counterpoint
def genCounter(main_passage, prev_note = 0):
    new_cells = []
    for main_cell in main_passage.cells: #loop through main cells
        if main_cell.chord == None or main_cell.chord == []:
            new_pits = []
            for pit in main_cell.pits:
                new_pits.append(pth.getClosestPCDegree(prev_note, pit, low = -5, high = 14))
                prev_note = new_pits[-1]
            new_cells.append(Chunk(pits = new_pits, durs = main_cell.durs, key=main_cell.key))
        else:
            durs = []
            pits = []

            #use random number to choose what durs
            ran = random.uniform(0,1)
            if ran < 0.2:
                durs = [1.0,1.0]
            elif ran < 0.5:
                durs = [1.5,0.5]
            else:
                durs = [2.0]

            for i in range(0, len(durs)):
                pits.append(sc.closestNoteDegreeInChord(prev_note, main_cell.chord, same=False, low = -3, high = 14))
                prev_note = pits[-1]
            new_cells.append(Chunk(pits=pits, durs=durs, key = main_cell.key, chord=main_cell.chord))
    return new_cells

def genCounterAndAlberti(main_passage, prev_note = 0):
    new_cells = []
    for main_cell in main_passage.cells: #loop through main cells
        if main_cell.chord == None or main_cell.chord == []:
            new_pits = []
            for pit in main_cell.pits:
                new_pits.append(pth.getClosestPCDegree(prev_note, pit, low = -5, high = 14))
                prev_note = new_pits[-1]
            new_cells.append(Chunk(pits = new_pits, durs = main_cell.durs, key=main_cell.key))
        else:
            durs = []
            pits = []

            #use random number to choose what durs
            ran = random.uniform(0,1)
            if ran < 0.2:
                durs = [1.0,1.0]
            elif ran < 0.2:
                durs = [1.5,0.5]
            elif ran < 0.6:
                durs = [2.0]
            else:
                durs = [0.5,0.5,0.5,0.5]
            if durs != [0.5,0.5,0.5,0.5]:
                for i in range(0, len(durs)):
                    pits.append(sc.closestNoteDegreeInChord(prev_note, main_cell.chord, same=False, low = -3, high = 14))
                    prev_note = pits[-1]
                else:
                    pits.extend(accomp.getAlbertiEighths(main_cell.chord, main_cell.pits, main_cell.durs))
            new_cells.append(Chunk(pits=pits, durs=durs, key = main_cell.key, chord=main_cell.chord))
    return new_cells
