# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 20:11:47 2015

@author: halley
"""
import functionalhelpers as fh
import rhythmhelpers as rhy

def getMaxDepth(chunk):
    if chunk.sub_chunks == None or chunk.sub_chunks == []:
        return 0
    else:
        return 1 + getMaxDepth(chunk.sub_chunks[0])

def getMinDepth(chunk):
    if chunk.sub_chunks == None:
        return 0
    else:
        return 1 + min([getMinDepth(i) for i in chunk.sub_chunks])

def getCells(chunk):
    if chunk.depth == 0:
        return [chunk]
    else:
        return fh.concat([getCells(i) for i in chunk.sub_chunks])





#A chunk of music
class Chunk():
    def setKey(self, key):
        self.key = key
        if self.sub_chunks != None:
            for sub_chunk in self.sub_chunks:
                sub_chunk.setKey(key)
            for i in range(0, len(self.cells)):
                self.cells[i].key = key
    def resetBeatPitsAndDurs(self):
        self.beat_durs = []
        new_note = True
        for note in self.durs:
            if new_note:
                self.beat_durs.append([note])
                if (note % 1) != 0:
                    new_note = False
            else:
                self.beat_durs[-1].append(note)
                if sum(self.beat_durs[-1]) % 1 == 0:
                    new_note = True
        self.beat_pits = fh.mapStructure(self.beat_durs, self.pits)

    def appendPitsDurs(self, pits, durs):
        self.pits += pits
        self.durs += durs

        self.resetBeatPitsAndDurs()

    def setPitsDurs(self, pits, durs):
        self.pits = pits
        self.durs = durs

        self.resetBeatPitsAndDurs()

    def __init__(self, pits = [], durs = [], ctype = -1, chord = [], sub_chunks = None, key = 0):
        self.sub_chunks = sub_chunks

        self.chord = chord
        #find depth
        self.depth = getMaxDepth(self)

        #get cells
        self.cells = getCells(self)

        self.key = key
        self.setKey(key)

        #find pits/durs
        if pits == [] and self.depth > 0:
            pits = fh.concat([i.pits for i in self.cells])
            durs = fh.concat([i.durs for i in self.cells])
        self.pits = pits
        self.durs = durs

        #get ctype - basically only useful for cells
        self.ctype = ctype

        #get beat rhythms and pitches
        self.beat_durs = []
        self.beat_pits = []
        self.resetBeatPitsAndDurs()
    def mapAllPits(self, f):
        if self.depth == 0:
            self.setPitsDurs(self, f(self.pits), self.durs)
        else:
            for sub_chunk in self.sub_chunks:
                sub_chunk.mapAllPits(f)

