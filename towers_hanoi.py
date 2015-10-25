__author__ = 'halley'
import music21helpers as mh


class Peg:
    def __init__(self, pits, durs, name):
        self.peg = []
        self.pits = pits
        self.durs = durs

pits = []
durs = []

def hanoi(n, source, target, helper1, helper2):
    if n == 1:
        target.peg.append(source.peg.pop())
        pits.extend(target.pits)
        durs.extend([i * n for i in target.durs])
    elif n == 2:
        helper1.peg.append(source.peg.pop())
        pits.extend(helper1.pits)
        durs.extend([i * n for i in helper1.durs])

        target.peg.append(source.peg.pop())
        pits.extend(target.pits)
        durs.extend([i * n for i in target.durs])

        target.peg.append(helper2.peg.pop())
        pits.extend(target.pits)
        durs.extend([i * n for i in target.durs])
    else:
        hanoi(n - 2, source, helper1, target, helper2)

        helper2.peg.append(source.peg.pop())
        pits.extend(helper2.pits)
        durs.extend([i * n for i in helper2.durs])


        target.peg.append(source.peg.pop())
        pits.extend(target.pits)
        durs.extend([i * n for i in target.durs])

        target.peg.append(helper2.peg.pop())
        pits.extend(helper2.pits)
        durs.extend([i * n for i in helper2.durs])

        hanoi(n - 2, helper1, target, source, helper2)

A = Peg([2,0,2,0], [0.25,0.25,0.25,0.25], 'A')
B = Peg([1,1], [0.25,0.25], 'B')
C = Peg([3,5,4], [0.25,0.25,0.5], 'C')
D = Peg([4,5,6,2], [0.375,0.125,0.375,0.125], 'D')

A.peg = [7, 6,5,4,3,2,1]

hanoi(7, A, B, C, D)

mh.showListsDegrees(pits, durs)