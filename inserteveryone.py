__author__ = 'halley'
from constants import *
import copy
import gencell as gc
import harmony as hm
import scale as sc
from chunk import *
import pitchhelpers as pth
import genbass as gb
import accompaniment as accomp
import random

def insertEveryone(instr_cells, main_passage, tags):
    bass = satb_inv['b']
    random.shuffle(bass)
    tenor = satb_inv['t']
    random.shuffle(tenor)
    bass_part = gb.genBass(main_passage)
    for i in range(0, len(bass_part)):
        bass_part[i].key = main_passage.cells[0].key
    if 'quarters' in tags:
        tenor_part = accomp.genQuarters(main_passage)
        for i in range(0, len(tenor_part)):
            tenor_part[i].key = main_passage.cells[i].key
    elif 'albertiEighths' in tags:
        tenor_part = accomp.genAlbertiEighths(main_passage)
    else:
        tenor_part = [gc.genBlankCell(2.0) for cell in main_passage.cells]
    blank_part = [gc.genBlankCell(2.0) for cell in main_passage.cells]
    for instr in instrs:
        if satb[instr] == 's' or satb[instr] == 'a':
            instr_cells[instr].extend(copy.deepcopy(main_passage.cells))
        elif satb[instr] == 't':
            if True:
                instr_cells[instr].extend(copy.deepcopy(tenor_part))
            else:
                instr_cells[instr].extend(copy.deepcopy(blank_part))
        else: #satb[instr] == 'b'
            if instr in bass[:2]:
                instr_cells[instr].extend(copy.deepcopy(bass_part))
            else:
                instr_cells[instr].extend(copy.deepcopy(blank_part))

