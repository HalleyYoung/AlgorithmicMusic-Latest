__author__ = 'halley'
import harmony as hm
import gencell as gc
import random
import transpose
import preferences as pref
from chunk import *
import probabilityhelpers as ph
import functionalhelpers as fh
import transform as tf




#generate a 2-cell motif
def genMotif(prev_note = random.choice([0,2,4,7]), chords = [[0,2,4],[0,2,4]], cell1 = None):
    #generate first cell
    start_chord = chords[0]
    if cell1 == None:
        cell1 = gc.genCell(2.0, prev_note, first_note = None, chord=start_chord, durs=[], cell_type=None)
    #now generate second cell from first cell
    end_chord = chords[1]
    if random.uniform(0, 1) < 0.8 and len(set(cell1.durs)) > 1 and 0.33333333 not in cell1.durs:
        return [cell1, tf.transformCell(cell1, cell1, end_chord)]
    else:
        if end_chord == None:
            end_chord = hm.getHighestProbChord(start_chord, None)
        cell2 = gc.genCell(2.0, cell1.pits[-1], None, end_chord, [], None)
        return [cell1, cell2]
