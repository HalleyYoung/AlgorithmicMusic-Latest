
__author__ = 'halley'
import music21helpers as mh

class Node:
    def __init__(self, pit):
        self.pit = pit
        self.left = None
        self.right = None

nums = range(60,73)

def sortedListToBST(list):
    if list == []:
        return None
    mid = len(list)/2
    new_node = Node(list[mid])
    new_node.left = sortedListToBST(list[:mid])
    new_node.right = sortedListToBST(list[(mid + 1):])
    return new_node

a = sortedListToBST(nums)


def inOrder(pits, durs, node):
    if node == None:
        return
    inOrder(pits, durs, node.left)
    pits.append(node.pit)
    durs.append(1.0)
    inOrder(pits, durs, node.right)
    return pits, durs

def preOrder(pits, durs, node):
    if node == None:
        return
    pits.append(node.pit)
    durs.append(0.5)
    preOrder(pits, durs, node.left)
    preOrder(pits, durs, node.right)
    return pits, durs

def postOrder(pits, durs, node):
    if node == None:
        return
    postOrder(pits, durs, node.left)
    postOrder(pits, durs, node.right)
    pits.append(node.pit)
    durs.append(0.25)
    return pits, durs

pitches = []
durs = []
ps,ds = inOrder([], [], a)
pitches.extend(ps)
durs.extend(ds)
ps,ds = preOrder([], [], a)
pitches.extend(ps)
durs.extend(ds)
ps,ds = postOrder([], [], a)
pitches.extend(ps)
durs.extend(ds)


mh.showLists(pitches, durs)