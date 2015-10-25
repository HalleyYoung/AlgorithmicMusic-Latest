# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 08:57:44 2015

@author: halley
"""
import scale as sc
import gencell as gc
from chunk import *
import random
import probabilityhelpers as ph
import music21helpers as mh
import rhythmhelpers as rhy
import harmony as hm
from constants import *
import copy


#scalewise run of pitches
def scalewiseRunSameRhythmSameDir(cell1, prog, prev_note = 0, up_down = random.choice([-1,1])):
    if cell1.durs == [2.0]:
        return [copy.deepcopy(cell1)]
    if cell1.ctype != SCALEWISE:
        return []
    direc = 1 if cell1.pits[-1] > cell1.pits[-2] else -1
    new_pitches = [prev_note + direc]
    for i in range(1, len(cell1.pits)):
        new_pitches.append(new_pitches[-1] + direc)
    return [Chunk(new_pitches, cell1.durs, cell1.ctype)]

#scalewise run, change rhythm
def scalewiseRunDiffRhythmSameDir(cell1, prog, prev_note = 0, up_down = random.choice([-1,1])):
    if cell1.durs == [2.0]:
        return [copy.deepcopy(cell1)]
    if cell1.ctype != SCALEWISE:
        return []
    direc = 1 if cell1.pits[-1] > cell1.pits[-2] else -1
    new_pitches = [prev_note + direc]
    new_rhythm = rhy.randomHalfRhythm()
    for i in range(1, len(new_rhythm)):
        new_pitches.append(new_pitches[-1] + direc)
    return [Chunk(new_pitches, new_rhythm, cell1.ctype)]


#scalewise run, change rhythm and direction
def scalewiseRunDiffRhythmSwitchDir(cell1, prog, prev_note = 0, up_down = random.choice([-1,1])):
    if cell1.durs == [2.0]:
        return [copy.deepcopy(cell1)]
    if cell1.ctype != SCALEWISE:
        return []
    direc = -1 if cell1.pits[-1] > cell1.pits[-2] else 1
    new_pitches = [prev_note + direc]
    new_rhythm = rhy.randomHalfRhythm()
    for i in range(1, len(new_rhythm)):
        new_pitches.append(new_pitches[-1] + direc)
    return [Chunk(new_pitches, new_rhythm, cell1.ctype)]

#retrograde
def retrograde(cell1, prog, prev_note = 0, up_down = random.choice([-1,1])):
    return [Chunk(cell1.pits[::-1], cell1.durs[::-1], cell1.ctype)]

# retrograde change last pitch
def retrogradeChangeLastPitch(cell1, prog, prev_note = 0, up_down = random.choice([-1,1])):
    new_pitches = cell1.pits[::-1][:-1]
    if len(new_pitches) == 0:
        return []
    if new_pitches[-1] % 7 in [i % 7 for i in prog]:
        mnew1 = new_pitches + [gc.getNthChordNote(new_pitches[-1], prog, up_down, 1)]
        mnew2 = new_pitches + [gc.getNthChordNote(new_pitches[-1], prog, up_down, 2)]
        return [Chunk(mnew1, cell1.durs[::-1], cell1.ctype), Chunk(mnew2, cell1.durs[::-1], cell1.ctype)]
    else:
        if cell1.pits[0] == new_pitches[-1] + 1:
            return [Chunk(new_pitches + [new_pitches[-1] - 1], cell1.durs[::-1], cell1.ctype)]
        else:
            return [Chunk(new_pitches + [new_pitches[-1]  + 1], cell1.durs[::-1], cell1.ctype)]

#retrograde only pitches
def retrogradePitches(cell1, prog, prev_note = 0, up_down = random.choice([-1,1])):
    return [Chunk(cell1.pits[::-1], cell1.durs, cell1.ctype)]

#same type, different durs
def sameCtypeDifferentDur(cell1, prog, prev_note = 0, up_down = random.choice([-1,1])):
    return [gc.genCell(length=2.0, prev_note=prev_note, first_note = None, chord = prog, durs = [], cell_type = cell1.ctype) for i in range(0,2)]

#same type, same durs
def sameCtypeSameRhythmDifferentChunk(cell1, prog, prev_note = 0, up_down = random.choice([-1,1])):
    return [gc.genCell(length=2.0, prev_note=prev_note, first_note = None, chord = prog, durs = cell1.durs, cell_type = cell1.ctype) for i in range(0,2)]


#keep same chunk, or just change what chord
def identity(chunk, chord = [], prev_note = 0, up_down = random.choice([-1,1])):
    if chords == []:
        return [chunk]
    else:
        if chunk.depth == 0:
            if chunk.ctype == SCALEWISE:
                return [copy.deepcopy(chunk)]
            else:
                above = []
                below = []
                for pit in chunk.pits:
                    above.append(hm.getClosestAbove(pit, chord))
                    below.append(hm.getClosestBelow(pit, chord))
                return [Chunk(sub_chunks=None, pits=above, durs=chunk.durs, ctype = chunk.ctype), Chunk(sub_chunks=None, pits = below, durs = chunk.durs, ctype=chunk.ctype)]


def inversion(chunk, chords, prev_note = 0, up_down = random.choice([-1,1])):
    if chunk.depth == 0:
        chords = chords
        new_notes = [chunk.pits[0]]
        for i in range(1, len(chunk.pits)):
            new_notes.append(new_notes[-1] - chunk.pits[i] + chunk.pits[i - 1])

        return [Chunk(new_notes, chunk.durs, chunk.ctype)]
    elif chunk.depth == 1:
        subs = chunk.sub_chunks
        new_subs = []
        for j in range(0, len(subs)):
            new_durs = subs[j].durs
            if j == 0:
                first_note = subs[0].pits[0]
            else:
                first_note = new_subs[-1].pits[-1] + subs[j].pits[0] - subs[j - 1].pits[-1]
            new_pits = [first_note]
            for i in range(1, len(subs[j].pits)):
                new_pits.append(new_pits[-1] - subs[j].pits[i] + subs[j].pits[i - 1])
            new_subs.append(hm.transposeToChord(Chunk(new_pits, new_durs, chunk.ctype), chords[j])[random.choice([0,1])])
        return [Chunk(new_subs)]
    else:
        return []

def partialTranspose(chunk, chords, prev_note = 0, up_down = random.choice([-1,1])):
    new_chunks = []
    if chunk.depth == 0:
        pits = chunk.pits
        #transpose every beat
        for amount in ([-2,2,-1,1]):
            for i in range(0, len(chunk.beat_durs)):
                new_pits = fh.concat(chunk.beat_pits[:i]) + [pit + amount for pit in chunk.beat_pits[i]] + fh.concat(chunk.beat_pits[i+1:])
                new_chunks.append(Chunk(new_pits, chunk.durs, chunk.ctype))
        #transpose every two notes
            for i in range(0, len(pits) - 1):
                new_pits = pits[:i] + [pits[i] + amount, pits[i + 1] + amount] + pits[i+1:]
                new_chunks.append(Chunk(new_pits, chunk.durs, chunk.ctype))
    return new_chunks


def partialRetrograde(chunk, chord, prev_note = 0, up_down = random.choice([-1,1])):
    new_chunks = []
    if chunk.depth == 0:
        if chunk.durs == [2.0]:
            return [copy.deepcopy(chunk)]
        #retrograde beginning, keep rhythm const
        new_pits = chunk.beat_pits[0][::-1] + fh.concat(chunk.beat_pits[1:])
        new_chunks.append(Chunk(new_pits, chunk.durs, chunk.ctype))
        #retrograde beginning, change rhythm
        new_durs = chunk.beat_durs[0][::-1] + fh.concat(chunk.beat_durs[1:])
        new_chunks.append(Chunk(new_pits, new_durs, chunk.ctype))

        #retrograde end, keep rhythm const
        new_pits = fh.concat(chunk.beat_pits[:-1]) + chunk.beat_pits[-1][::-1]
        new_chunks.append(Chunk(new_pits, new_durs, chunk.ctype))
        #retrograde end, change rhythm
        new_durs = fh.concat(chunk.beat_durs[:-1]) + chunk.beat_durs[-1][::-1]
        new_chunks.append(Chunk(new_pits, new_durs, chunk.ctype))

        #switch order of beats
        new_pits = fh.concat(reversed(chunk.beat_pits))
        new_durs = fh.concat(reversed(chunk.beat_durs))
        new_chunks.append(Chunk(new_pits, new_durs))

    return new_chunks

def subRhythm(chunk, chord, prev_note = 0, up_down = random.choice([-1,1])):
    new_rhythm = rhy.alterRhythm(chunk.durs, 0.3)
    return gc.genCell(length=sum(new_rhythm),prev_note=prev_note, first_note = None, chord=chord, durs=new_rhythm, cell_type=chunk.ctype)