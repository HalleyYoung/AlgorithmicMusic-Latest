import transform as tf
import gencell as gc

#transform first cell twice
def transformFirstCellTwice(transform_motif, prev_cell = gc.genBlankCell(2.0), chords = [[0,2,4],[0,2,4]]):
    cell1 = tf.transformCell(transform_motif[0], prev_cell, chords[0])
    cell2 = tf.transformCell(transform_motif[0], cell1, chords[1])
    return [cell1, cell2]

#transform second cell twice
def transformSecondCellTwice(transform_motif, prev_cell = gc.genBlankCell(2.0), chords = [[0,2,4],[0,2,4]]):
    cell1 = tf.transformCell(transform_motif[1], prev_cell, chords[0])
    cell2 = tf.transformCell(transform_motif[1], cell1, chords[1])
    return [cell1, cell2]


 #switch to exact
def transformFirstChangeSecond(transform_motif, prev_cell = gc.genBlankCell(2.0), chords = [[0,2,4],[0,2,4]]):
    cell1 = tf.transformCell(transform_motif[0], prev_cell, chords[0])
    cell2 = gc.genCell(length=2.0, prev_note=cell1.pits[-1], chord=chords[1])
    return [cell1, cell2]

#switch first and second cell
def switchFirstSecond(transform_motif, prev_cell = gc.genBlankCell(2.0), chords = [[0,2,4],[0,2,4]]):
    cell1 = tf.transformCell(transform_motif[1], prev_cell, chords[0])
    cell2 = tf.transformCell(transform_motif[0], cell1, chords[1])
    return [cell1, cell2]

#transform first cell and then second cell of prev_cell
def transformFirstSecond(transform_motif, prev_cell = gc.genBlankCell(2.0), chords = [[0,2,4],[0,2,4]]):
    cell1 = tf.transformCell(transform_motif[0], prev_cell, chords[0])
    cell2 = tf.transformCell(transform_motif[1], cell1, chords[1])
    return [cell1, cell2]
"""
    take first motif, transform twice
    take second motif, transform twice
    take exact first motif and change second to something totally different
    switch first and second motif
    transform first and second motif
"""
