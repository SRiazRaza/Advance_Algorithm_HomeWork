from algorithms.prim import Prim
from data_structures.tsp import TSP


class TwoApproximation:
    def algorithm(self, graph: TSP):
        starting_node = 1
        prim = Prim()
        key, mst = prim.prim_mst(graph, starting_node)

        # Convert the MST result to a tree-like structure

        # Prepare the tree-like structure
        # Complexity: teta(n)
        tree = {}
        for i in range(1, len(graph.adjMatrix)):
            tree[i] = []

        # Complexity: O(n log(n))
        for index in mst:
            if mst[index] != None:
                (parent, _, weight) = mst[index]
                tree[parent].insert(self._insert(tree[parent], mst[index]), (index, weight))

        # Visit the MST in preorder
        preorder_result = []
        self._preorder_visit(graph, tree, (starting_node, 0), preorder_result)

        # Add the root to create a cycle
        preorder_result.append(starting_node)

        # Sum all the weights
        summation = 0
        for i in range(len(preorder_result) - 1):
            summation += graph.adjMatrix[preorder_result[i]][preorder_result[i + 1]]

        return int(summation)

    # Complexity: teta(n)
    def _preorder_visit(self, graph: TSP, tree, v, path):
        (identifier, weight) = v
        path.append(identifier)
        for (u, w) in tree[identifier]:
            self._preorder_visit(graph, tree, (u, w), path)

    # Complexity: O(log(n))
    def _insert(self, array, x, low=0, high=None):
        (p, _, w) = x

        if high is None:
            high = len(array)
        while low < high:
            mid = (low + high) // 2
            (c_i, w_i) = array[mid]
            if w < w_i:
                high = mid
            else:
                low = mid + 1
        return low
