from collections import defaultdict
import sys
from data_structures.heap import Heap, Node
from data_structures.tsp import TSP

sys.path.append('../')


class Prim:
    """
    Prim's MST algorithm with Heap (First Assignment with little changes)

    Pseudocode
    Prim (G, s)
        for each u in V do
            key [u] <- inf
            parents (u) <- null
        key [s] <- 0
        Q <- V
        while Q! = empty do
            u <- extractMin (Q)
            for each v adjacent to u do
                if v in Q and w (u, v) <key [v] then
                    parents (v) <- u
                    key [v] <- w (u, v)

    prim_mst (G: graph, s: node): (defaultdict (list), defaultdict (list))
        G = graph on which to execute the algorithm
        s = starting node for the algorithm
    Return the key and parent maps
    """

    def prim_mst(self, T: TSP, s):
        """
        key: defaultdict (list) = key map. A value is in the form key [node] = node_weight
        parent: defaultdict (list) = parent map. A value is in the form parent [node] = origin_node
        Q: Heap = heap containing the nodes of the resulting MST
        """
        key = defaultdict(list)
        parent = defaultdict(list)
        Q = Heap()

        """
        Initialization
        * For each node node of G \ {s}, key [node] = Inf. Key [s] = 0
        * For each node node of G, parent [node] = nil
        * Q <- V
        """
        for i in range(1, len(T.adjMatrix[0])):
            key[i] = 0 if s == i else float('inf')
            parent[i] = None
            Q.insert(Node(i, key[i]))

        """
        Calculation of the map of the keys and of the parents
        As long as the heap Q is not empty
            pull out the minimum weight knot. u = (index, weight)
            For each node v with weight w adjacent to u
                If the node is present in Q and the weight in Q is less than the weight of v
                    parent [v] = u
                    key [v] = w
                    update Q with the new node of index v and weight key [v]
        """
        while Q.currentSize != 0:
            u = (Q.extractMin()).toTuple()
            for j in range(1, len(T.adjMatrix[int(u[0])])):
                if Q.search(j) and T.adjMatrix[int(u[0])][j] < key[j]:
                    (identifier, prim_weight) = u
                    parent[j] = (identifier, prim_weight, T.adjMatrix[int(u[0])][j])
                    key[j] = T.adjMatrix[int(u[0])][j]
                    Q.searchAndUpdateWeight(j, key[j])

        return key, parent

    """
    get_weight (key: defaultdict (list)): int
        key = MST node map. For each node node, key [node] = node_weight
    Returns the sum of the weights of the MST
    """
    def get_weight(self, key):
        sum = 0
        for (_, v) in key.items():
            if v!= float('inf'):
                sum += v
        return sum
