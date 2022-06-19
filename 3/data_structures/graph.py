from collections import defaultdict
import math

import sys
sys.path.append('../')


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)  # Adjacency list
        self.totalVertex = 0
        self.totalEdges = 0
        self.V = set()
        self.E = []
        self.datasetName = ""

    def add_vertex(self, value: int):
        self.V.add(value)
      

    # Assumption: Called just after addVertex
    def add_edge(self, u: int, v: int, w: int):
        self.E.append((u, v, w))
        self.graph[u].append((v, w))
        self.graph[v].append((u, w))

    def remove_edge(self, u: int, v: int, w: int):
        if (u,v,w) in self.E:
            self.E.remove((u, v, w))
        self.graph[u].remove((v, w))
        self.graph[v].remove((u, w))
    
    def remove_node(self, v: int): 
        for t in self.graph:
            for (u, w) in self.graph[t]:
                if u == v:
                    self.graph[t].remove((u,w))

        if v in self.graph.keys():
            del self.graph[v]

        if v in self.V:
            self.V.remove(v)
        
        for a,b,c in self.E:
            if a == v or b == v:
                self.E.remove((a,b,c))

    def weightBetween(self, firstNode, secondNode):
        minWeight = float('inf')

        for index in range(0, len(self.E)):
            if (self.E[index][0] == firstNode and self.E[index][1] == secondNode) or (self.E[index][1] == firstNode and self.E[index][0] == secondNode):
                minWeight = self.E[index][2]
                break
        return minWeight

    def totalWeightCost(self, firstNode, secondNode):
        minWeight = 0

        for index in range(0, len(self.E)):
            if (self.E[index][0] == firstNode and self.E[index][1] == secondNode) or (self.E[index][1] == firstNode and self.E[index][0] == secondNode):
                minWeight += self.E[index][2]
        return minWeight
