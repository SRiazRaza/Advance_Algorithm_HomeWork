import sys
import math
from collections import defaultdict

#from matplotlib.font_manager import _Weight

sys.path.append('../')

PI = 3.141592

"""
TSP class
tsp: TSP = (name: string, dimension: int, etype: string, nodes: defaultdict (list), adjMatrix: list [])
    name = name of the dataset
    dimension = size of the dataset
    etype = dataset type (GEO | EUC_2D)
    nodes = list of nodes of the graph
    adjMatrix = adjacency matrix of the graph nodes
"""


class TSP:

    def __init__(self):
        self.name = ''
        self.dimension = 0
        self.etype = ''
        self.nodes = defaultdict(list)
        self.adjMatrix = []

    """
    add_node (i: int, x: float, y: float): void
        i = index of the node
        x = latitude
        y = longitude
    Add a node to the node list; it does not change the adjacency matrix.
    If the dataset is in GEO format, it converts x and y to radians.
    """
    #Note: No conversion for Euclidean Distance 
    def add_node(self, i: int, x: float, y: float):
        if self.etype == 'GEO':
            degX, degY = int(x), int(y)
            minX, minY = x - degX, y - degY
            x, y = PI * (degX + 5.0 * minX / 3.0) / 180.0, PI * (degY + 5.0 * minY / 3.0) / 180.0
        self.nodes[i] = [x, y]

    """
    get_weight (first: int, sec: int): float
        first = index of the first node
        second = index of the second node
    The weight returns between one knot and another.
    Distinguish if the coordinates are lat, long or Euclidean
    """
 
    def get_weight(self, first: int, sec: int):
        if self.etype == 'GEO':
            RRR = 6378.388
            q1 = math.cos(self.nodes[first][1] - self.nodes[sec][1])
            q2 = math.cos(self.nodes[first][0] - self.nodes[sec][0])
            q3 = math.cos(self.nodes[first][0] + self.nodes[sec][0])
            return int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)
        else:
            return round(math.sqrt(
                (self.nodes[sec][1] - self.nodes[first][1]) ** 2 + (self.nodes[sec][0] - self.nodes[first][0]) ** 2))

    """
    calculateAdjMatrix (): void
    Calculate the adjacency matrix (symmetric matrix on the diagonal).
    Let's assume it is called after inserting nodes for the first time in the TSP.
    """

    def calculateAdjMatrix(self):
        #print(self.dimension + 1)
        for i in range(self.dimension + 1):
            self.adjMatrix.append([0 for i in range(self.dimension + 1)])

        for i in range(1, self.dimension + 1):
            for j in range(1, self.dimension + 1):
                if i == j:
                    # self.adjMatrix[i][j] = 0
                    self.adjMatrix[i][j] = math.inf
                else:
                    self.adjMatrix[i][j] = self.adjMatrix[j][i] = self.get_weight(i, j)

    """
    printAdjMatrix (): void
    Utility function for printing the adjacency matrix.
    """

    def printAdjMatrix(self):
        print('\n')
        print('\n'.join([''.join(['{:4}'.format((item)) for item in row])
                         for row in self.adjMatrix]))

    """
    delete_node (index: ind): void
        index = index of the node to be deleted
    Delete, if it exists, a node from the node list. It also updates the adjacency matrix.
    """

    def delete_node(self, index: int):
        if index in self.nodes.keys():
            self.nodes.pop(index)
            for i in range(1, self.dimension + 1):
                self.adjMatrix[i][index] = self.adjMatrix[index][i] = 0
            self.dimension = self.dimension - 1

    """
    get_min_node (visited: list, index: ind): [int, float, float]
        visited = list of visited nodes in which NOT to search for the minimum
        index = index of the node for which to find the neighbor of minimum weight
    Returns the lowest weight node from index that has not yet been visited by the Nearest Neighbor algorithm    """

    def get_min_node(self, visited, index: int):
        minWeight = float('inf')
        minIndex = -1
        for i in range(1, self.dimension + 1):
            if self.adjMatrix[i][index] < minWeight and self.adjMatrix[i][index] != 0 and i not in visited:
                minIndex = i
                minWeight = self.adjMatrix[index][i]

        return ([minIndex, self.nodes[minIndex][0], self.nodes[minIndex][1]])

    """    
    def get_min_random_node(self, index):
        partial_circle=index

        return weight"""
