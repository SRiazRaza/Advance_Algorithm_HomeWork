from collections import defaultdict

import sys
sys.path.append('../')


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)  # Adjacency list
        self.V = set()
        self.E = []

    def add_vertex(self, value: int):
        self.V.add(value)

    # Called just after addVertex
    def add_edge(self, u: int, v: int, w: int):
        self.E.append((u, v, w))
        self.graph[u].append((v, w))
        self.graph[v].append((u, w))

    def remove_edge(self, u: int, v: int, w: int):
        self.E.remove((u, v, w))
        self.graph[u].remove((v, w))
        self.graph[v].remove((u, w))

    def weightBetween(self, firstNode, secondNode):
        minWeight = float('inf')

        for index in range(0, len(self.E)):
            if (self.E[index][0] == firstNode and self.E[index][1] == secondNode) or (
                    self.E[index][1] == firstNode and self.E[index][0] == secondNode):
                minWeight = self.E[index][2]
                break
        return minWeight

    def get_weight(self, first_node, second_node):
        # print('First node: {}'.format(str(first_node)))
        # print('Second node: {}'.format(str(second_node)))
        weight = float('inf')

        for i in range(0, len(self.graph[first_node])):
            # print('Candidate edge: {}'.format(str(self.graph[first_node][i])))
            (u, w) = self.graph[first_node][i]
            if second_node == u:
                weight = w

        # print('Weight: {}\n'.format(weight))
        return weight
