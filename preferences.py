__author__ = 'halley'
import harmony as hm
import functionalhelpers as fh

#check whether the cells are a good combination
def goodCells(cells):
    if not all([len(i.pits) == len(i.durs) for i in cells]):
        return False
    pits = fh.concat([j.pits for j in cells])
    #no leaping from non-tone chord
    if not hm.inChord(cells[0].pits[-1], cells[0].chord) and abs(cells[0].pits[-1] - cells[1].pits[0]) > 1:
        return False
    pit_diffs = [abs(pits[i] - pits[i - 1]) for i in range(1, len(pits))]
    #no three in a row
    for i in range(2, len(pits)):
        if abs(pits[i] - pits[i - 1]) == 6:
            return False
        if pits[i] == pits[i - 1] and pits[i - 2] == pits[i]:
            return False
        if (pits[i] % 7) == 3 and (pits[i - 1] % 7) == 6 or  (pits[i] % 7) == 6 and (pits[i - 1] % 7) == 3:
            return False
    #no jumps bigger than 4
    if max(pit_diffs) > 4:
        return False
    #no notes lower than -3
    if min(pits) < -3:
        return False
    if max(pits) > 20:
        return False
    for i in range(1, len(cells)):
        if (cells[i - 1].pits[-1] % 7) == 3 and cells[i].chord == [0,2,4] and (cells[i].pits[0] % 7) != 2:
            return False
        if (cells[i - 1].pits[-1] % 7) == 6 and cells[i].chord == [0,2,4] and (cells[i].pits[0] % 7) != 0:
            return False
    if len(cells) > 1:
        if max(pits) - min(pits) < 4:
            return False
    return True

#test if a single cell = good
def goodCell(cell):
    if len(cell.durs) != len(cell.pits):
        return False
    if len(cell.durs) == 1:
        return True
    pits = cell.pits
    durs = cell.durs
    pit_diffs = [abs(pits[i] - pits[i - 1]) for i in range(1, len(pits))]
    #no three in a row
    for i in range(2, len(pits)):
        if pits[i] == pits[i - 1] and pits[i - 2] == pits[i]:
            return False
    for i in range(1, len(pits)):
        if durs[i] == 0.25 and durs[i - 1] == 0.25 and pits[i] == pits[i - 1]:
            return False
    #no jumps bigger than 4
    if max(pit_diffs) > 4:
        return False
    #no notes lower than -3
    if min(pits) < -3:
        return False
    if max(pits) > 20:
        return False
    return True