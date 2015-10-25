__author__ = 'halley'
from chunk import *
import random

def transposeToNewStart(old_cell, new_cell):
    transpose_locations = [0,1,-1,-2,2,3,3,4,-4,5,-5]
    new_cells = []
    for transpose_location in transpose_locations:
        new_pits = [i + transpose_location for i in new_cell.pits]
        new_cells.append(Chunk(new_pits, new_cell.durs, new_cell.ctype))
    return new_cells