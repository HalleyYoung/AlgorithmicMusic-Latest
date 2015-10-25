__author__ = 'halley'
from chunk import *
import pitchhelpers as pth
import harmony as hm
import gencell as gc
import scale as sc

def genBass(main_passage, low = -4, high = 7):
    prev_note = 4
    main_cells = main_passage.cells
    bass_cells = []
    for main_cell in main_cells:
        if main_cell.chord == [] or main_cell.chord == None:
            bass_cells.append(gc.genBlankCell(2.0))
            prev_note = 4
        else:
            main_pits = main_cell.beat_pits
            pits = []
            pits.append(pth.getClosestPCDegree(prev_note, main_pits[0][0], low = low, high = high))


            if len(main_pits) == 2:
                if hm.inChord(main_pits[1][0], main_cell.chord):
                    pits.append(sc.closestNoteDegreeInChord(note=pits[-1], chord=main_cell.chord, same=False, low = low, high = high))
                    durs = [1.0,1.0]
                    bass_cells.append(Chunk(pits = pits, durs=durs, chord=main_cell.chord, key = main_cell.key))
                else:
                    durs = [2.0]
                    bass_cells.append(Chunk(pits = pits, durs = durs, chord=main_cell.chord, key = main_cell.key))
            else: #if it's a 1.5, 0.5 or 1.5, 0.25,0.25
                durs = [2.0]
                bass_cells.append(Chunk(pits = pits, durs = durs, chord=main_cell.chord, key = main_cell.key))
            prev_note = pits[-1]
    return bass_cells
