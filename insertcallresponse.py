__author__ = 'halley'
import gencell as gc
from constants import *
import random
from chunk import *

#insert call response
def insertCallResponse(instr_cells, main_passage, group1, group2):
    main_cells = main_passage.cells
    main1 = [[] for instr in group1]
    main2 = [[] for instr in group2]
    empty = [gc.genBlankCell(2.0) for i in main_cells]
    for i in range(0, len(main_cells)):
        if i % 2 == 0:
            for j in range(0, len(main1)):
                main1[j].append(main_cells[i])
            which_to_sound = random.randint(0, len(main2) - 1)
            for j in range(0, len(main2)):
                if j != which_to_sound:
                    main2[j].append(gc.genBlankCell(2.0))
                else:
                    if main_cells[i].chord == None or main_cells[i].chord == []:
                        main2[j].append(gc.genBlankCell(2.0))
                    else:
                        main2[j].append(Chunk(pits = [random.choice(main_cells[i].chord)], durs=[2.0], key=main_cells[i].key))
        else:
            for j in range(0, len(main2)):
                main2[j].append(main_cells[i])
            which_to_sound = random.randint(0, len(main1) - 1)
            for j in range(0, len(main1)):
                if j != which_to_sound:
                    main1[j].append(gc.genBlankCell(2.0))
                else:
                    if main_cells[i].chord == None or main_cells[i].chord == []:
                        main1[j].append(gc.genBlankCell(2.0))
                    else:
                        main1[j].append(Chunk(pits = [random.choice(main_cells[i].chord)], durs=[2.0], key=main_cells[i].key))
    for i in range(0, len(group1)):
        instr_cells[group1[i]].extend(main1[i])
    for i in range(0, len(group2)):
        instr_cells[group2[i]].extend(main2[i])
    for instr in instrs:
        if instr not in group1 and instr not in group2:
            instr_cells[instr].extend(empty)
    return main_cells