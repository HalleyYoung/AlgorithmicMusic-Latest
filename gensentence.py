__author__ = 'halley'
import genphrase as gp
import gencontinuationcadential as gcc
import genbasicidea as gbi
import transform as tf
from chunk import *

def genSentence(bi1 = None):
    if bi1 == None:
        bi1 = gbi.genBasicIdea()
    bi2 = tf.alterBasicIdea(bi1, chords=[[0,2,4],[3,5,7],[4,6,8],[4,6,8]], prev_note=bi1.pits[-1])
    if bi2.pits[-1] > 10:
        for i in range(0, len(bi2.cells)):
            bi2.cells[i].pits = [j - 7 for j in bi2.cells[i].pits]
    continuation_cadential = gcc.genContinuationCadential(prev_note = bi2.pits[-1])
    return Chunk(sub_chunks = [bi1,bi2, continuation_cadential])