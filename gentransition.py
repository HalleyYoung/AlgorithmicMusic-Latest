import genphrase as gp
import gencontinuationcadential as gcc
import genbasicidea as gbi
import transform as tf
import gencell as gc
from chunk import *

def genTransition():
    chords = [[4,6,8],[4,6,8],[0,2,4],[0,2,4],[4,6,8],[4,6,8],[0,2,4], [0,2,4]]
    phrase = gp.genPhrase(prev_note = 0, chords=chords, authentic_cadence=True)
    for i in range(0,4):
        phrase.cells[i].setKey(7)
    phrase.sub_chunks[0].setKey(7)
    return phrase