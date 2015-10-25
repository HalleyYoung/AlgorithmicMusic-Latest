from constants import *
import random
import genphrase as gp
import scale as sc
from collections import OrderedDict
import insertchordal as ic
from music21 import *
import inserttutti as it
import inserteveryone as ie
import insertcallresponse as icr
import transform as tf
import genperiod as gper
import gencontinuationcadential as gcc
import gensentence as gs

instr_cells = dict([(instr,[]) for instr in instrs])

ic.insertChordal(instr_cells)
period1phrase1 = (gp.genPhrase(authentic_cadence=False))
it.insertTutti(instr_cells, period1phrase1, group_inv[random.choice(tuttis)])

period1phrase2 = (gp.genPhrase(basicIdea=period1phrase1.sub_chunks[0], authentic_cadence=True))
ie.insertEveryone(instr_cells, period1phrase2, {'bassRhythm':'True'})

period2 = (gper.genPeriod())
ie.insertEveryone(instr_cells, period2.sub_chunks[0], {'quarters':True})
ie.insertEveryone(instr_cells, period2.sub_chunks[1], {'albertiEighths':True})


switcher1 = gp.genPhrase(authentic_cadence=False)
switcher1.setKey(7)
random.shuffle(groups)
icr.insertCallResponse(instr_cells, switcher1, group_inv[groups[0]], group_inv[groups[1]])
continuation1 = (gcc.genContinuationCadential())
continuation1.setKey(7)
it.insertTutti(instr_cells, continuation1, group_inv[groups[2]])
phrase2 = gp.genPhrase(authentic_cadence=True)
phrase2.setKey(7)
ie.insertEveryone(instr_cells, phrase2, {'albertiEighths':True})


ie.insertEveryone(instr_cells, period2.sub_chunks[0], {'albertiEighths':True})
ie.insertEveryone(instr_cells, period2.sub_chunks[1], {'quarters':True})
'''period3 = genPeriod(basic_idea = transformBasicIdea(main_passages))
insertEveryone(instr_cells, period3, {'sixteenths':'effect', 'bassRhythm':True})"""
'''

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

s = stream.Stream()
for part in parts.values():
    s.insert(0, part)

s.show()