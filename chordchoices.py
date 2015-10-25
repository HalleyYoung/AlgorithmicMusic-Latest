__author__ = 'halley'
import random
from constants import *
import music21helpers as mh

#pick a chord progression that fits the given last chord
def chooseChords(num_chords, first_chord = [0,2,4], end_chords = [[0,2,4]]):
    chords = [first_chord]
    for i in range(1, num_chords - len(end_chords) - 1):
        next_chord = random.choice(chord_movements[chords[-1][0]])
        chords.append([next_chord + j for j in [0,2,4]])
    penultimate_chord_choices = chord_movements[chords[-1][0]]
    penultimate_chord_choices = filter(lambda i: end_chords[0][0] in chord_movements[i], penultimate_chord_choices)
    penultimate_choice = random.choice(penultimate_chord_choices)
    chords.append([penultimate_choice + j for j in [0,2,4]])
    chords.extend(end_chords)
    return chords


chords = chooseChords(num_chords = 8, end_chords = [[4,6,8],[0,2,4]])
print(chords)
pits = [tuple(i) for i in chords]
durs = [2.0 for i in chords]

part =  mh.listsDegreesToPart(pits, durs)

part.show()