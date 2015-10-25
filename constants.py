# -*- coding: utf-8 -*-
"""
Created on Thu May 14 17:05:37 2015

@author: halley
"""
from noteconstants import *
from collections import OrderedDict

chord_movements =  {0:[0,1,2,3,4,5,6], 1:[3,4,0,1], 2:[3,2], 3:[4,0,3], 4:[0,3,5,4], 5:[3,1,4,5], 6:[0,2,6]}

SCALEWISE = 1
USUAL = 2
REP_PATTERN = 3
CHORDAL = 4

MIDI = 0
PITCH_CLASS = 1
NAME = 2

#fifths dict
fifths = {}
fifths[0] = 0
for i in range(1,7):
    fifths[i] = (fifths[i - 1] + 7) % 12
for i in range(-1,-7,-1):
    fifths[i] = (fifths[i + 1] - 7) % 12

#scales dict
scales = {}
scales["major"] = [0,2,4,5,7,9,11]
scales["nminor"] = [0,2,3,5,7,8,10]
scales["hminor"] = [0,2,3,5,7,8,11]
scales["wholetone"] = [0,2,4,6,8,10]
scales["pmajor"] = [0,2,4,7,9]
scales["pminor"] = [0,3,5,7,10]
scales["chromatic"] = range(0,11)
scales["C major"] = scales["major"]
scales["G major"] = [i + 7 for i in scales["major"]]

#modes dict
modes = {}
modes ["dorian"] = 1
modes["phrygian"] = 2
modes["lydian"] = 3
modes["mixolydian"] = 4
modes["aeolian"] = 5
modes["locrian"] = 6

#modes should also be scales
s = scales["major"]
for mode, deg in modes.items():
    scales[mode] = s[deg:] + map(lambda i: i + 12, s[:deg])


#intervals dict
intervals = {}
intervals["perfect"] = {"P1": 0, "P5": 7}
intervals["imperfect"] = {"min3" : 3, "maj3":4, "min6" : 8, "maj6" : 9}
intervals["dissonant"] = {"min2": 1, "maj2" : 2, "P4": 5}
intervals["majorscale"] = {"I": 0, "II" : 2, "III": 4, "iv":5, "V" : 7, "VI" : 9, "VII" : 11}
intervals["bad"] = {"tritone": 6, "aug4" : 6, "min7" : 10, "maj7" : 11}
intervals["min2"] = 1
intervals["maj2"] = 2
intervals["min3"] = 3
intervals["maj3"] = 4
intervals["p4"] = 5
intervals["aug4"] = 6
intervals["tritone"] = 6
intervals["p5"] = 7
intervals["min6"] = 8
intervals["maj6"] = 9
intervals["min7"] = 10
intervals["maj7"] = 11
intervals["major"] = dict([(x, intervals[x]) for x in "maj2", "maj3", "maj6", "maj7"])
intervals["minor"] = dict([(x, intervals[x]) for x in "min2", "min3", "min6", "min7"])

#chords dict
chords = {}
chord_types = {}
chord_types["major"] = [C, E, G]
#chords["augmented"] = [0,4,8]
chord_types["dom7"] = [0,4,7,10]
#chords["major7"] = [0,4,7,11]
#chords["sus2"] = [0,2,7]
#chords["sus4"] = [0,5,7]
#chords["german6"] = [-4,0,3,6]
#chords["french6"] = [-4,0,2,6]
#chords["italian6"] = [-4, 0, 6]


chord_types["minor"] = [0, 3, 7]
chord_types["dim"] = [0,3,6]
#chords["half_dim7"] = [-1,2,5,9]
#chords["dim7"] = [-1,2,5,8]
major_chord_types = ["major", 'dom7']#["major", "augmented", "dom7", "major7", 'sus2', 'sus4', 'german6', 'french6', 'italian6']

minor_chord_types = ['minor', 'dim']#, 'half_dim7', 'dim7']

def scaleVal( interval, scale = scales["major"]):
    return scale[interval%7] + 12*(interval/7)

#define all chords for all chord types and scale degrees
major_triads = ["I", "II", "III", "IV", "V", "VI", "VII"]
minor_triads = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
for i in range(0, len(major_triads)):
    for chord_type in major_chord_types:
        chords[str(major_triads[i]) + " " + chord_type] = map(lambda j: j + scaleVal(i), chord_types[chord_type])
    for chord_type in minor_chord_types:
        chords[str(minor_triads[i]) + " " + chord_type] = map(lambda j: j + scaleVal(i), chord_types[chord_type])

chord_groupings = {}
chord_groupings['predominant'] = []
chord_groupings['dominant'] = []


"""
sevenths = [''.join([i, '7']) for i in triads]
for i in range(0, len(sevenths)):
    chords[sevenths[i]] = map(scaleVal, [i,i+2,i+4]) + [scaleVal(i+6) - 1]
"""
#cadences dict
#somehow get inversions - perfect authentic not inverted, imperfect inverted
cadences = {}
cadences["perfect-authentic"] = [[4, 0] ]
cadences["imperfect-authentic"] = [[4,0] , [6,0]]
cadences["half"] = [[0,4], [1,4], [3,4], [5,4]]
cadences["deceptive"] = [[4,3]]
cadences["plagal"] = [[3,0]]

def romanNumeral(chord, major):
    if chord == [0,2,4]:
        if major:
            return "I"
        else:
            return 'i'
    elif chord == [1,3,5]:
        return 'II'
    elif chord == [2,4,6]:
        if major:
            return 'iii'
        else:
            return 'III'
    elif chord == [3,5,0]:
        if major:
            return 'IV'
        else:
            return 'iv'
    elif chord == [4,6,1]:
        if major:
            return 'V'
        else:
            return 'v'
    elif chord == [5,0,2]:
        if major:
            return 'vi'
        else:
            return 'VI'
    elif chord == [6,1,3]:
        if major:
            return 'viio'
        else:
            return 'VII'
    else:
        return "?"
"""
cadences["perfect-authentic"] = [["V", "I"]]
cadences["imperfect-authentic"] = [["V", "I"] , ["vii","I"]]
cadences["half"] = [["I", "V"], ["ii", "V"], ["IV", "V"], ["vi", "V"]]
cadences["deceptive"] = [["V", "vi"]]
cadences["plagal"] = [["IV","I"]]
"""

satb = OrderedDict([('Oboe','s'), ('Flute 1','a'), ('Bassoon','b'), ('Trumpet 1 in C', 'a'), ('Trumpet 2 in C', 't'), ('Trombone', 'b'), ('Violin 1','s'), ('Viola','t'), ('Violoncello','b')])
satb_inv = {'s':[], 'a':[], 't':[], 'b':[]}
for instr, role  in satb.items():
    satb_inv[role].append(instr)

instrs = satb.keys()

group = {'Oboe':'winds', 'Flute 1':'winds', 'Bassoon':'winds', 'Trumpet 1 in C': 'brass', 'Trumpet 2 in C': 'brass', 'Trombone': 'brass', 'Violin 1':'strings', 'Viola':'strings', 'Violoncello':'strings'}
group_inv = {'winds':[], 'strings':[], 'brass':[]}
for instr, role in group.items():
    group_inv[role].append(instr)

groups = group_inv.keys()

tuttis = ['winds', 'strings']
sixteenths = ['Flute 1', 'Oboe', 'Violin 1', 'Viola']
solos = ['Flute 1', 'Oboe', 'Violin 1']

octaves = {'Oboe':5, 'Flute 1':5, 'Flute 2':5, 'Bassoon':3, 'Trumpet 1 in C':5, 'Trumpet 2 in C':5, 'Trombone':3, 'Violin 1':5, 'Violin 2':5, 'Viola':5, 'Violoncello':3}

tutti_bass = ['Bassoon', 'Violoncello']
tutti_accomp = ['Oboe', 'Viola']
