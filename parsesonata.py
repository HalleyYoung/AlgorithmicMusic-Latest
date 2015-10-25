__author__ = 'halley'
from music21 import  *
import music21helpers as mh

s = converter.parse('/users/halley/desktop/score.xml')
parts = []
for part in s.parts:
    parts.append(part)

measures = []
pits = []
durs = []
for part in parts:
    measures.append([])
    pits.append([])
    durs.append([])
    for measure in part.measures(0,1000):
        measures[-1].append(measure)
    for measure in measures[-1]:
        if type(measure) == stream.Measure:
            elements = measure.elements
            for element in elements:
                if type(element) == stream.Voice:
                    new_elems = element.elements
                    for elem in new_elems:
                        if type(elem) == note.Note:
                            pits[-1].append(elem.midi)
                            durs[-1].append(elem.quarterLength)
                        elif type(elem) == note.Rest:
                            pits[-1].append(-36)
                            durs[-1].append(elem.quarterLength * -1)
                elif type(element) == note.Note:
                    pits[-1].append(element.midi)
                    durs[-1].append(element.quarterLength)
                elif type(element) == note.Rest:
                    pits[-1].append(-36)
                    durs[-1].append(element.quarterLength * -1)
                if type(element) == chord.Chord:
                    pits[-1].append(tuple([i.midi for i in element.pitches]))
                    durs[-1].append(element.quarterLength)


s = stream.Stream()
for i in range(0, len(pits)):
    s.insert(0, mh.listsToPart(pits[i], durs[i]))

s.show()
