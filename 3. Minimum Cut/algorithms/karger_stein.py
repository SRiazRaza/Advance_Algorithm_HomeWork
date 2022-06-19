from data_structures.karger_graph import KargerGraph
import math
import numpy.random as rnd
from copy import deepcopy
import gc
import time
import sys

sys.path.append('../')


class KargerStein:
    def __init__(self, G: KargerGraph):
        self.G = G
    
    """
    Input: cumulative weight vector C

    Allows you to randomly choose a certain value r and returns,
    through binary search, the position of that value in the
    cumulative weight vector C.
    """
    def random_select(self, C):
        random = rnd.uniform(low=0, high=C[len(C) - 1], size=(1,))
        r = round(random[0])

        found = False
        start = 1
        end = len(C)
        mid = 0

        while start < end and found == False:
            mid = (start + end) // 2

            if C[mid - 1] <= r and r < C[mid]:
                found = True
            elif C[mid] <= r:
                start = mid + 1
            elif C[mid] > r:
                end = mid

        return mid

    """
    Input: W: weighted adjacency matrix
          D: vector of the weighted degrees of the vertices

    It allows to choose one side of the graph G in linear time with respect to
    number of vertices of the graph. To determine the vertices, this procedure
    use the random_select method.
    """
    def edge_select(self, D, W):
        C_D = []
        for i in range(1, len(D) + 1):
            acc = 0
            for j in range(1, i):
                acc += D[j]
            C_D.append(acc)

        u = self.random_select(C_D)

        C_W = []
        for i in range(1, len(D) + 1):
            acc = 0
            for j in range(1, i):
                acc += W[u][j]
            C_W.append(acc)

        v = self.random_select(C_W)

        return (u, v)

    """
    Input: W: weighted adjacency matrix
            D: vector of the weighted degrees of the vertices
            u, v: vertices
            n: number of vertices in graph G

    Make the contraction of the chosen side.
    """
    def contract_edge(self, D, W, u, v, n: int):
        D[u] = D[u] + D[v] - 2 * W[u][v]
        D[v] = 0
        n = n - 1
        W[u][v] = W[v][u] = 0

        for w in range(1, self.G.n_vertices + 1):
            if w != u and w != v:
                W[u][w] += W[v][w]
                W[w][u] += W[w][v]
                W[v][w] = W[w][v] = 0

        return n

    """
    Input: W: weighted adjacency matrix
            D: vector of the weighted degrees of the vertices
            k: number of vertices to contract

    Defines the full contraction operation, updating
    all data structures.
    """
    def contract(self, D, W, k: int):
        n = 0
        for d in D:
            if d != 0:
                n += 1

        n_i = 0
        for i in range(0, n - k):
            (u, v) = self.edge_select(D, W)
            n_i = self.contract_edge(D, W, u, v, n)
        return D, W, n_i

    """
    Input: W: weighted adjacency matrix
            D: vector of the weighted degrees of the vertices
            n: number of vertices in graph G

    Corresponds to the full_contraction method of the Karger algorithm,
    but obtaining an advantage from the point of view
    computational and the possibility of being applied for weighted graphs.
    """
    def recursive_contract(self, D, W, n: int):
        if n <= 6:
            D_prime, W_prime, _ = self.contract(D, W, 2)

            u, v = 0, 0
            for i in range(len(D_prime)):
                if u == 0 and D_prime[i] != 0:
                    u = i
                elif u != 0 and v == 0 and D_prime[i] != 0:
                    v = i

            # Return the weight of the single arc (u, v) in G_prime
            return W_prime[u][v]

        t = math.ceil(n / math.sqrt(2) + 1)

        w = []
        for i in range(1, 3):
            D_i, W_i, n_i = self.contract(D, W, t)
            w.append(self.recursive_contract(D_i, W_i, n_i))

        return min(w[0], w[1])

    """
Input: threshold_in_seconds: value in seconds to indicate the threshold
                                    beyond which the execution of the algorithm
                                    is interrupted

    This recursive procedure calls enough recursive_contract
    of times in order to guarantee correctness in high probability.
    """
    def algorithm(self, threshold_in_seconds=math.inf):
        #Calculate vector D
        self.G.calculate_weighted_degrees_vertices()

        W = self.G.W
        D = self.G.D

        is_threshold_activated = False
        discovery_time = 0
        minimum = math.inf
        k_min = 0
        k = round((math.log(self.G.n_vertices, 2)) ** 2)

        starting_total_time = starting_discovery_time = time.perf_counter_ns()
        gc.disable()

        #Reps for high probability
        # The code bieng reused from main.py
        for i in range(0, k):
            if time.perf_counter_ns() > (starting_total_time + (threshold_in_seconds * 1000000000)):
                is_threshold_activated = True
                break

            t = self.recursive_contract(deepcopy(D), deepcopy(W), deepcopy(self.G.n_vertices))

            if t < minimum:
                discovery_time = time.perf_counter_ns() - starting_discovery_time
                minimum = t
                k_min = (i + 1)

        gc.enable()
        total_time = time.perf_counter_ns() - starting_total_time

        return minimum, k, k_min, discovery_time, total_time, is_threshold_activated

    """
    Input: threshold_in_seconds: value in seconds to indicate the threshold
                                    beyond which the execution of the algorithm
                                    is interrupted

    This method is used to make algorithm measurements.
    """
    # The altered code from main.py (asympotic part) 
    def measurements(self, threshold_in_seconds=math.inf):
        min_cut, k, k_min, discovery_time, total_time, is_threshold_activated = self.algorithm(threshold_in_seconds)

        if total_time < 1000000000:
            num_calls = 1000000000 // total_time

            starting_repetitions_total_time = time.perf_counter_ns()
            repetitions_discovery_time = 0
            for j in range(0, num_calls):
                min_cut, k, k_min, discovery_time, total_time, is_threshold_activated = self.algorithm(threshold_in_seconds)
                repetitions_discovery_time += discovery_time
            repetitions_total_time = time.perf_counter_ns() - starting_repetitions_total_time

            return min_cut, k, k_min, (repetitions_discovery_time / num_calls), (repetitions_total_time / num_calls), num_calls, is_threshold_activated
        else:
            return min_cut, k, k_min, discovery_time, total_time, 1, is_threshold_activated