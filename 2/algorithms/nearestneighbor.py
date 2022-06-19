from data_structures.tsp import TSP
import copy as cp

class NearestNeighbor:
    def algorithm(self, graph: TSP):
        
        """
        startingGraph: TSP = graph from which the nodes are gradually extracted
        finalPath: list = list containing the path as it is found
        visited: list = visit the visited nodes
        totalWeight: float = total weight of the tsp graph
        """
        startingGraph = cp.deepcopy(graph)
        finalPath, visited = [], []
        totalWeight = 0

        """Initialization
        * Take the first node
            * Add it to finalPath
            * Add its index to visited
        * Delete the node from the starting set
        """
        startingNode = startingGraph.nodes[1]
        finalPath.append([1, startingNode[0], startingNode[1]])
        visited.append(1)
        startingGraph.delete_node(1)
        
        """
        Search for nodes
        * Let (V1, ..., Vk) be the current path:
            * Take the vertex Vk + 1 not present and with minimum distance from Vk
            * Insert Vk + 1 after Vk
            * Update the weight value
            * Delete the node Vk + 1 from the starting set
        """
        while startingGraph.dimension != 0:
            lastEl = finalPath[-1][0]
            
            visited.append(lastEl)
            minimumNode = graph.get_min_node(visited, lastEl)
            finalPath.append([minimumNode[0], minimumNode[1], minimumNode[2]])

            totalWeight += graph.adjMatrix[lastEl][finalPath[-1][0]]
            startingGraph.delete_node(minimumNode[0])

            #print(finalPath[-1][0])
        
       
        # Add the start node to close the graph
        totalWeight += graph.adjMatrix[finalPath[-1][0]][1]
        finalPath.append([1, startingNode[0], startingNode[1]])

        return totalWeight
        