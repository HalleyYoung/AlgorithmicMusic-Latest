__author__ = 'halley'
import music21helpers as mh
import random

pits = []
durs = []

nums = range(48,61)
for i in range(0,12):
    nums.append(random.choice(range(48,61)))
random.shuffle(nums)

pits.extend(nums)
durs.extend([0.125 for i in nums])

def merge(x1, x2):
    #print('x1 = ' + str(x1) + ' x2 = ' + str(x2))
    new_list = []
    i = 0
    j = 0
    if x1 == None or x1 == []:
        return x2
    elif x2 == None or x2 == []:
        return x1
    while (i < len(x1) and j < len(x2)):
        if x1[i] < x2[j]:
            new_list.append(x1[i])
            pits.append(x1[i])
            i += 1
            durs.append(0.5)
        else:
            new_list.append(x2[j])
            pits.append(x2[j])
            j += 1
            durs.append(0.25)
    if i < len(x1):
        new_list.extend(x1[i:])
        pits.extend(x1[:i])
        durs.extend([0.5 for k in x1[:i]])
    elif j < len(x2):
        new_list.extend(x2[j:])
        pits.extend(x2[j:])
        durs.extend([0.5 for k in x2[:i]])
    return new_list

def mergeSort(list):
    if len(list) == 1:
        return list
    if len(list) >= 2:
        half_point = len(list)/2
        first_half = mergeSort(list[:half_point])
        second_half = mergeSort(list[half_point:])
        #pits.extend(first_half)
        #pits.extend(second_half)
        return merge(first_half, second_half)


a = mergeSort(nums)

pits.extend(a)
durs.extend([0.125 for i in a])

mh.showLists(pits, durs)