__author__ = 'halley'
from chunk import *
import genbasicidea as gbi
import transform as tf
import genending

default_chords = [[0,2,4],[0,2,4],[3,5,7],[0,2,4],[0,2,4],[0,2,4],[1,3,5],[4,6,8],[0,2,4],[0,2,4],[3,5,7],[0,2,4],[0,2,4],[3,5,7],[4,6,8],[0,2,4]]
#generate a period
def genPeriod(chords = default_chords, bi11 = None, real_end = False):
    if bi11 == None:
        bi11 = gbi.genBasicIdea(chords=chords[:4])
    bi21 = gbi.genBasicIdea(prev_note = bi11.pits[-1], chords=chords[4:8])
    bi21cells = bi21.cells
    bi21cells[-1] = genending.genEnding(bi21cells[-2].pits[-1], chord=chords[7], authentic=False)
    bi21 = Chunk(sub_chunks = bi21cells)
    bi12 = tf.alterBasicIdea(bi = bi11, prev_note = bi21.pits[-1], chords = chords[8:12])
    bi22 = tf.alterBasicIdea(bi = bi21, prev_note = bi12.pits[-1], chords = chords[12:], cadence='authentic', real_end = real_end)
    return Chunk(sub_chunks=[Chunk(sub_chunks=[bi11,bi21]), Chunk(sub_chunks=[bi12, bi22])])