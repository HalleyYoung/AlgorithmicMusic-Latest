from constants import *
import random
import genphrase as gp
import scale as sc
from collections import OrderedDict
from music21 import *
import transform as tf
import genperiod as gper
import gensentence as gs
import gentransition as gt
import accompaniment as acc
import gencell as gc
import counterpoint as counter
import genbass as gb
from chunk import *

#define instruments
instr_cells = OrderedDict()
instr_cells['Flute'] = []
instr_cells['Piano 1'] = []
instr_cells['Piano 2'] = []
instrs = ['Flute', 'Piano 1', 'Piano 2']
octaves = {'Flute':5, 'Piano 1':5, 'Piano 2':4}

#generate content

period1phrase1 = (gp.genPhrase(authentic_cadence=False))
instr_cells['Flute'].extend([gc.genBlankCell(2.0) for cell in period1phrase1.cells])
instr_cells['Piano 1'].extend(period1phrase1.cells)
instr_cells['Piano 2'].extend(acc.genAlbertiEighths(period1phrase1))

period1phrase2 = (gp.genPhrase(basicIdea=period1phrase1.sub_chunks[0], authentic_cadence=True))
instr_cells['Flute'].extend(period1phrase2.cells)
instr_cells['Piano 1'].extend(acc.genAlbertiEighths(period1phrase2))
instr_cells['Piano 2'].extend(acc.genQuarters(period1phrase2))

period2 = (gper.genPeriod())
period2phrase1 = period2.sub_chunks[0]
instr_cells['Flute'].extend(counter.genCounter(period2phrase1))
instr_cells['Piano 1'].extend(period2phrase1.cells)
instr_cells['Piano 2'].extend(acc.genAlbertiEighths(period2phrase1))

period2phrase2 = period2.sub_chunks[1]
instr_cells['Flute'].extend(period2phrase2.cells)
instr_cells['Piano 1'].extend(counter.genCounter(period2phrase2))
instr_cells['Piano 2'].extend(acc.genQuarters(period2phrase2))

#call response
switcher = gp.genPhrase(authentic_cadence=False)
switcher.setKey(7)
scells = switcher.cells
chords = [i.chord for i in scells]
for i in range(0, len(switcher.cells)):
    if chords[i] == None or chords[i] == []:
        instr_cells['Flute'].append(scells[i])
        instr_cells['Piano 1'].append(scells[i])
    else:
        if i % 2 == 0:
            instr_cells['Flute'].append(scells[i])
            instr_cells['Piano 1'].append(Chunk(pits = [sc.closestNoteDegreeInChord(instr_cells['Piano 1'][-1].pits[-1], scells[i].chord, low = -3, high = 16)], durs = [2.0]))
            instr_cells['Piano 1'][-1].setKey(7)
        else: #if odd
            instr_cells['Flute'].append(Chunk(pits = [sc.closestNoteDegreeInChord(instr_cells['Flute'][-1].pits[-1], scells[i].chord, low = -3, high = 16)], durs = [2.0]))
            instr_cells['Flute'][-1].setKey(7)
            instr_cells['Piano 1'].append(scells[i])
instr_cells['Piano 2'].extend(gb.genBass(switcher))

sentence1 = gs.genSentence()
sentence1.setKey(7)
instr_cells['Flute'].extend(sentence1.cells)
instr_cells['Piano 1'].extend(counter.genCounter(sentence1, instr_cells['Piano 1'][-1].pits[-1]))
instr_cells['Piano 2'].extend(gb.genBass(sentence1))


transition_phrase = gt.genTransition()
instr_cells['Flute'].extend([gc.genBlankCell(2.0) for cell in transition_phrase.cells])
instr_cells['Piano 1'].extend(transition_phrase.cells)
instr_cells['Piano 2'].extend(acc.genAlbertiEighths(transition_phrase, leading_eighths = False))


period3 = gper.genPeriod(bi11 = tf.alterBasicIdea(period1phrase2.sub_chunks[0]), real_end=True)
period3phrase1 = period3.sub_chunks[0]
instr_cells['Flute'].extend(period3phrase1.cells)
instr_cells['Piano 1'].extend(counter.genCounter(period3phrase1))
instr_cells['Piano 2'].extend(gb.genBass(period3phrase1))

period3phrase2 = period3.sub_chunks[1]
instr_cells['Flute'].extend(period3phrase2.cells)
instr_cells['Piano 1'].extend(counter.genCounter(period3phrase2))
instr_cells['Piano 2'].extend(acc.genAlbertiEighths(period3phrase2, leading_eighths = False))


#create parts from instr_cells
parts = OrderedDict()
for instr in instrs:
    parts[instr] = stream.Part()
    parts[instr].insert(0, instrument.fromString(instr))
    for cell in instr_cells[instr]:
        pits = sc.degreesToNotes(degrees=cell.pits, octave=octaves[instr], scale = [i + cell.key for i in [0,2,4,5,7,9,11]])
        durs = cell.durs
        for i in range(0, len(pits)):
            if durs[i] > 0:
                n = note.Note(pits[i])
                n.quarterLength = durs[i]
            else:
                n = note.Rest()
                n.isRest = True
                n.quarterLength = abs(durs[i])
            parts[instr].append(n)

#insert into stream
s = stream.Stream()
for part in parts.values():
    s.insert(0, part)

#show result
s.show()

#parts.values()[1].show()