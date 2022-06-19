#!/user/bin/env python3

import sys
from collections import defaultdict
sys.path.append('../')
"""
    MaxHeap (binary)
    -----------------------------------------
"""

"""
Node class
node: Node = (index: int, weight: int)
    index = number of the vertex
    weight = weight of the vertex
"""
class Node : 

    def __init__(self, index, weight):
        self.index = index
        self.weight = weight
    
    # Utility function that, starting from a node object, returns it in the form of a tuple (index, weight)
    def toTuple(self):
        return (self.index, self.weight)


"""
MaxHeap class
maxheap: MaxHeap = (list: Node [], mapList: defaultdict (list), currentSize: int)
    list = list of nodes of the graph
    mapList = map that associates the vertex index to its position in the list
    currentSize = Heap size
"""
class MaxHeap:

    def __init__(self):
        self.list = [Node(0, float('-inf'))] # dummy node to have arrays starting from 1
        self.mapList = defaultdict(list)
        self.currentSize = 0
    
    """
    parent (index: int): Node
        index = index of the current node
    Returns the parent of the node with index index
    """
    def parent(self, index):
        return self.list[index//2]

    """
    right (index: int): Node
        index = index of the current node
    Returns the right child of the node with index index
    """
    def right(self, index):
        return self.list[(index * 2) + 1]
    
    """
left (index: int): Node
        index = index of the current node
    Returns the left child of the node with index index
    """
    def left(self, index):
        return self.list[(index * 2)]

    """
heapifyUp (index: int): void
        index = index of the node to heapify from
    Runs the heapify procedure of the heap from bottom to top
    In doing so, it also updates the location map
    Returns the location where the node was added
    """
    def heapifyUp(self, index):
        constInd = index
        while index // 2 > 0:
            if self.list[index].weight > self.list[index // 2].weight:
                self.mapList[self.list[(index)].index] = index // 2
                self.mapList[self.list[index // 2].index] = index
                constInd = index // 2
                self.list[index], self.list[index // 2] = self.list[index // 2], self.list[index]
            index //= 2
        return constInd
    
    """
    search (index: int): boolean
        index = index of the node to search for
    Returns True if the index node index exists on the heap, otherwise it returns false
    """
    def search(self, index):
        if index in self.mapList.keys():
            return True
        return False
    
    """
searchAndUpdateWeight (index: int, newWeight: int): void
        index = index of the node to be updated
        newWeight = new weight of the node
    Update the heap with the new node value

    Operation is as follows:
    extrapolates the position in the list of the Node with index index
    updates the weight of that node to inf
    executes heapifyUp from the searched node to make it go to the top of the heap
    update the weight of the node (now) on top of the heap
    executes heapifyDown to guarantee ownership of the heap
    """
    def searchAndUpdateWeight(self, index, newWeight):
        i = self.mapList[index]
        self.list[i].weight = float('inf')
        self.heapifyUp(i)
        self.list[1].weight = newWeight
        self.heapifyDown(1)
    

    """
increaseKey (index: int, newWeight: int): void
        index = index of the node to be updated
        newWeight = new weight of the node
    Update the heap with the new node value

    Operation is as follows:
    extrapolates the position in the list of the Node with index index
    updates the weight of that node to inf
    executes heapifyUp from the searched node to update the weight on top of the heap
    """
    def increaseKey(self, index, newWeight):
        i = self.mapList[index]
        if(self.list[i].weight < newWeight):
            self.list[i].weight = newWeight
            self.heapifyUp(i)

    """
    insert (node: Node): void
        node = node to insert
    It inserts the new node into the heap and runs heapifyUp to secure ownership of the heap
    It also updates the location map with the location returned by heapifyUp
    """
    def insert(self, node):
        self.list.append(node)
        self.currentSize += 1
        pos = self.heapifyUp(self.currentSize)
        self.mapList[node.index] = pos
    
    """
    heapifyDown (index: int): void
        index = index of the node to heapify from
    Runs the heapify procedure of the heap from top to bottom
    In doing so, it also updates the location map
    """
    def heapifyDown(self, index):
        while (index * 2) <= self.currentSize :
            maxChild = self.maxChild(index)
            if self.list[index].weight < self.list[maxChild].weight: 
                self.mapList[self.list[maxChild].index] = index
                self.mapList[self.list[index].index] = maxChild
                self.list[index], self.list[maxChild] = self.list[maxChild], self.list[index]
            index = maxChild

    """
    maxChild (index: int): int
        index = index of the node to return the youngest child of
    Returns the index of the child node of the index node with less weight
    """
    def maxChild(self, index):
        if (index * 2)+1 > self.currentSize:
            return index * 2
        else:
            if self.list[index*2].weight > self.list[(index*2)+1].weight:
                return index * 2 
            else:
                return (index * 2) + 1
 
    """
    extractMax (): Node
    Returns the maximum weight node of the heap which, since this is a maxHeap, coincides with the first element
    """
    def extractMax(self):
        if len(self.list) == 1:
            return None
        maxEl = self.list[1]
        del self.mapList[maxEl.index]
        self.list[1] = self.list[self.currentSize]
        self.mapList[self.list[self.currentSize].index] = 1
        # *self.list, _ = self.list
        del self.list[self.currentSize]
        self.currentSize -= 1
        self.heapifyDown(1)
        return maxEl

    """
    extractChecker (extracted: int): boolean
    Utility function for testing the extraction of the maximum element from the heap
    """
    def extractChecker(self, extracted):
        for a in self.list:
            if(extracted < a.weight):
                return False
        return True

    """
    print (): void
    Utility function to print the heap
    """
    def print(self):
        for i in range(1, (self.currentSize//2)+1):
            
            print(" PARENT: "+ str(self.list[i].index) + "(w." + str(self.list[i].weight)+") LEFT CHILD: "+ str(self.list[2*i].index) + "(w." +
                                str(self.list[2 * i].weight) + ")", end="")
            if 2*i+1 <= self.currentSize : 
                print(" RIGHT CHILD: " + str(self.list[2*i+1].index) + "(w." + str(self.list[2 * i + 1].weight) + ")")
            else:
                print("")