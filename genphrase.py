__author__ = 'halley'
import random
import genbasicidea as gb
import transform as tf
import gencell as gc
import rhythmhelpers as rhy
import music21helpers as mh
import genending
import preferences as pref
import scale as sc
from music21 import *
import harmony as hm
from chunk import *

#generate a four bar phrase
def genPhrase(prev_note = random.randint(0,4), chords = [[0,2,4],[0,2,4],[4,6,8], [0,2,4],[0,2,4],[3,5,7],[4,6,8],[0,2,4]], basicIdea = None, authentic_cadence = False):
    phrase_cells = []
    if basicIdea == None:
        basicIdea = gb.genBasicIdea(prev_note=prev_note, chords = chords[:4], motif1 = None)
    phrase_cells = basicIdea.cells
    #choose first or second motif of basic idea to transform for third motif
    which_motif_to_transform = random.choice([phrase_cells[:2], phrase_cells[2:]])
    third_motif = tf.transformMotif(which_motif_to_transform, phrase_cells[-1], chords[4:6])
    motif4cell1 = (gc.genCell(2.0, third_motif[-1].pits[-1], first_note=None, chord=chords[6], durs = rhy.getDefiningRhythm(phrase_cells + third_motif)))
    motif4cell2 = genending.genEnding(motif4cell1.pits[-1], chords[-1], authentic_cadence)
    second_half = Chunk(sub_chunks = third_motif + [motif4cell1] + [motif4cell2], ctype='half')
    return Chunk(sub_chunks = [basicIdea, second_half], ctype = 'phrase')
"""
melody_cells = []
for i in range(0, 4):
    melody_cells.extend(genPhrase().cells)

harmony_pits = []
harmony_durs = []
for cell in melody_cells:
    if not pref.goodCell(cell):
        print('False')
    if cell.chord != [] and cell.chord != None:
        harmony_pits.append(tuple(cell.chord))
        harmony_durs.append(2.0)
    else:
        harmony_pits.append(0)
        harmony_durs.append(-2.0)
harmony_pits = sc.degreesToNotes(degrees=harmony_pits, octave=4)
harmony_part = mh.listsToPart(harmony_pits, harmony_durs)


melody_part = stream.Part()
for cell in melody_cells:
    pits = sc.degreesToNotes(cell.pits)
    durs = cell.durs
    if len(pits) != len(durs):
        print('oy!')
    for i in range(0, len(pits)):
        n = note.Note(pits[i])
        if durs[i] > 0:
            n.quarterLength = durs[i]
        else:
            n.isRest = True
            n.quarterLength = abs(durs[i])
        melody_part.append(n)


s = stream.Stream()
s.insert(0, melody_part)
s.insert(0, harmony_part)
s.show()
"""
