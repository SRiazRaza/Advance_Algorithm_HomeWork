import sys

sys.path.append('../')


class KargerGraph:
    def __init__(self, n_vertices, n_edges):
        self.n_edges = n_edges
        self.n_vertices = n_vertices
        self.W = []                     # Adjacency matrix
        self.D = []                     # Weighted degree of vertices

        for i in range(self.n_vertices + 1):
            self.W.append([0 for _ in range(self.n_vertices + 1)])

    def add_edge(self, u: int, v: int, w: int):
        self.W[u][v] = self.W[v][u] = w

    def remove_edge(self, u: int, v: int):
        self.W[u][v] = self.W[v][u] = 0

    def calculate_weighted_degrees_vertices(self):
        if len(self.D) == 0:
            self.D.append(0)
            for i in range(1, self.n_vertices + 1):
                acc = 0
                for j in range(1, self.n_vertices + 1):
                    acc += self.W[i][j]
                self.D.append(acc)
