from chunk import *
import probabilityhelpers as ph
import rhythmhelpers as rhy
import random
from constants import *
import music21helpers as mh
import scale as sc
import preferences as pref

p_cell_dict = {}
p_cell_dict[SCALEWISE] = 0.2
p_cell_dict[USUAL] = 0.3
p_cell_dict[CHORDAL] = 0.5


#generate scalewise cells
def genScalewiseCell(length, prev_note = 0, first_note = None, chord = [], durs = []):
    if durs == []:
        rhythm = rhy.randomDuration(length)
    else:
        rhythm = durs
    direction = 1
    if first_note != None:
        pitches = [first_note]
    elif prev_note % 7 == 6 and chord == [0,2,4]:
        pitches = [prev_note + 1]
    elif prev_note % 7 == 3 and chord == [0,2,4]:
        pitches = [prev_note - 1]
    else:
        if chord == []:
            pitches = [prev_note + random.choice([1,-1])]
        else:
            pitches = [sc.closestNoteDegreeInChord(prev_note, chord, True, 0)]
    for i in range(1, len(rhythm)):
        if pitches[-1] % 7 == 6 and chord == [0,2,4]:
            pitches.append(pitches[-1] + 1)
        elif pitches[-1] % 7 == 3 and chord == [0,2,4]:
            pitches.append(pitches[-1] - 1)
        else:
            direction = direction if random.uniform(0,1) < 0.7 else direction * -1
            if pitches[i - 1] > 14:
                direction = -1
            elif pitches[i - 1] < 0:
                direction = 1
            pitches.append(pitches[i - 1] + direction)
    return_val = Chunk(pits=pitches, durs=rhythm, ctype=SCALEWISE, chord=chord)
    if pref.goodCell(return_val):
        return return_val
    else:
        return genScalewiseCell(length, prev_note, first_note, chord, durs)

#get random next degree
def randomNextDegree(prev_note, up_down):
    if prev_note <= 0:
        up_down = 1
    direction = up_down if random.uniform(0,1) < 0.63 else up_down * -1
    new_note = prev_note + 1*direction
    return new_note

#gen next chord note up or down a certain amount
def getNthChordNote(prev_note, cord, up_down, how_many):
    n = 0
    if n == 0:
        prev_note = sc.closestNoteDegreeInChord(prev_note, cord, True, up_down)
    elif prev_note <= 0:
        up_down == 1
    while n < how_many:
        prev_note += up_down
        if prev_note % 7 in [i % 7 for i in cord]:
            n += 1
    return prev_note


#get a random chord note
def randomChordNote(prev_note, cord, per_up = '0.5', sixteenth = False):
    """if sixteenth:
        how_many = 1
    else:
        how_many = ph.probDictToChoice({0:0.1, 1:0.9})"""
    how_many = 1
    upOrDown = 1 if random.uniform(0,1) < per_up else -1
    if prev_note <= -3:
        how_many = 2
    if prev_note <= 0:
        upOrDown = 1
    if prev_note > 10:
        upOrDown = -1
    return getNthChordNote(prev_note, cord, upOrDown, how_many)

#generate chordal cells
def genChordalCell(length, prev_note = 0, first_note = None, cord = [], durs = []):
    pitches = []
    def strToNum(string):
        return [int(i) for i in string.split()]
    if cord == []:
        cord = strToNum(ph.probDictToChoice({'0 2 4':0.5, '4 6 8':0.3, '3 5 7':0.2}))
    if durs == []:
        durs = rhy.randomDuration(length)
    if first_note != None:
        pitches = [first_note]
    elif prev_note % 7 == 6 and cord == [0,2,4]:
        pitches = [prev_note + 1]
    elif prev_note % 7 == 3 and cord == [0,2,4]:
        pitches = [prev_note - 1]
    else:
        pitches = [sc.closestNoteDegreeInChord(prev_note, cord, 1, False)]
    for i in range(1, len(durs)):
        pitches.append(randomChordNote(prev_note, cord, durs[i] == 0.25))
        if not (pitches[-1] % 7 in [ j % 7 for j in cord]):
            print(' prevnote ' + str(prev_note) + ' new ' + str(pitches[-1]) + ' chord ' + str(cord))
        prev_note = pitches[-1]
    """return_val = Chunk(pits=pitches, durs=durs, ctype=CHORDAL, chord=cord)
    if pref.goodCell(return_val):
        return return_val
    else:
        return genChordalCell(length, prev_note, first_note, cord, durs)"""
    return Chunk(pits=pitches, durs=durs, ctype=CHORDAL, chord=cord)

#generate usual cells
def genUsualCell(length, prev_note = 0, first_note = None, cord = [], durs = []):
    pitches = []
    def strToNum(string):
        return [int(i) for i in string.split()]
    if cord == []:
        cord = strToNum(ph.probDictToChoice({'0 2 4':0.5, '4 6 8':0.3, '3 5 7':0.2}))
    if durs == []:
        durs = rhy.randomDuration(length)
    if first_note != None:
        pitches = [first_note]
    elif prev_note % 7 == 6 and cord == [0,2,4]:
        pitches = [prev_note + 1]
    elif prev_note % 7 == 3 and cord == [0,2,4]:
        pitches = [prev_note - 1]
    else:
        pitches = [sc.closestNoteDegreeInChord(prev_note, cord, 1, False)]
    tot_durs = [sum(durs[:i]) for i in range(0, len(durs))]
    for i in range(1, len(durs)):
        if tot_durs[i] % 1.0 == 0:
            if prev_note not in cord:
                pitches.append(sc.closestNoteDegreeInChord(prev_note, cord, True))
            else:
                pitches.append(randomChordNote(prev_note, cord))
        elif random.uniform(0,1) < 0.5:
            if prev_note not in cord:
                pitches.append(sc.closestNoteDegreeInChord(prev_note, cord, True))
            else:
                pitches.append(randomChordNote(prev_note, cord))
        else:
            pitches.append(randomNextDegree(prev_note, 1))
        prev_note = pitches[-1]
    return_val = Chunk(pitches, durs, USUAL, cord, None)
    if pref.goodCell(return_val) or random.uniform(0,1) < 0.05:
        return return_val
    else:
        return genUsualCell(length, prev_note, first_note, cord, durs)


#get any type of cell
def genCell(length, prev_note = 0, first_note = None, chord = [], durs = [], cell_type = None):
    if cell_type == None:
        cell_type = ph.probDictToChoice(p_cell_dict)
    if cell_type == SCALEWISE:
        return genScalewiseCell(length, prev_note, first_note, chord, durs)
    elif cell_type == CHORDAL:
        return genChordalCell(length, prev_note, first_note, chord, durs)
    else:
        return genUsualCell(length, prev_note, first_note, chord, durs)

#create a resting cell
def genBlankCell(length):
    return Chunk(pits = [0], durs = [-1*length])
