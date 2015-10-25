
__author__ = 'halley'


class Node:
    def __init__(self, pit):
        self.pit = pit
        self.left = None
        self.right = None

nums = range(48,61)

def sortedListToBST(list):
    if list == []:
        return None
    mid = len(list)/2
    new_node = Node(list[mid])
    new_node.left = sortedListToBST(list[:mid])
    new_node.right = sortedListToBST(list[(mid + 1):])
    return new_node

a = sortedListToBST(nums, )