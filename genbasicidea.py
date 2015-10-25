__author__ = 'halley'
import random
import genmotif as gm
import transform as tf
import functionalhelpers as fh
from chunk import *

#generate a basic idea
def genBasicIdea(prev_note = random.choice([0,2,4,7]), chords = [[0,2,4], [4,6,8], [0,2,4], [0,2,4]], motif1 = None, cell1 = None):
    if motif1 == None:
        motif1 = gm.genMotif(prev_note = prev_note, chords = chords[:2], cell1 = cell1)
    motif1_durs = fh.concat([i.durs for i in motif1])
    if 2.0 in motif1_durs or motif1_durs == [1.0,1.0,1.0,1.0]:
        motif2 = gm.genMotif(prev_note=motif1[1].pits[-1], chords = chords[2:])
        return Chunk(sub_chunks = motif1 + motif2, ctype='bi')
    else:
        motif2 = tf.transformMotif(transform_motif=motif1, prev_cell=motif1[0], chords=chords[2:])
        return Chunk(sub_chunks = motif1 + motif2, ctype='bi')

