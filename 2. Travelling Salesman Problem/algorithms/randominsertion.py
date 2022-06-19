from functools import partial
import graphlib
from itertools import cycle
from data_structures.tsp import TSP
import copy as cp
import random

class RandomInsertion :
    
    def algorithm(self,g:TSP):
        partial_circle=[]
        weight= 0
        graph = cp.deepcopy(g)
        partial_circle.append(1) 
        nodes = [i for i in range(2, graph.dimension+1)] # 0 has already been selected
        #print("1.",nodes)
        minimum = float('inf')
        for i in range(1,graph.dimension+1):
            if graph.adjMatrix[1][i]:
                if graph.adjMatrix[1][i] < minimum:
                    minimum = graph.adjMatrix[1][i]
                    j = i
                    #print(graph.adjMatrix[1][i],minimum,j)

        partial_circle.append(j)
        nodes.remove(j)
        #print("2",nodes)

        while len(partial_circle) < graph.dimension+1:
            # Selection
            k = random.choice(nodes)
            #print("Random: ",k)
            nodes.remove(k)
            #print("Nodes: ",nodes)
            # Insertion
            minimum =  float('inf')
            
            for idx in range(len(partial_circle)-1):

                i, j = partial_circle[idx], partial_circle[idx+1] # edge {i, j}
                wik, wkj, wij = graph.adjMatrix[i][k], graph.adjMatrix[k][j], graph.adjMatrix[i][j]
                w = wik + wkj - wij

                if w < minimum:
                    minimum = w
                    idx_of_k = idx+1 # the location where k must be inserted

            partial_circle.insert(idx_of_k, k)
            #print("Partial Circle: ",partial_circle)
        
        for el in range(len(partial_circle)-1): 
            weight += graph.adjMatrix[partial_circle[el]][partial_circle[el+1]]

        partial_circle.append(partial_circle[0]) #adding starting point at the end to create a cycle
        weight += graph.adjMatrix[partial_circle[-2]][partial_circle[-1]] #adding starting
        # point at the end to create a cycle
        
        #cycle_ = sorted(set(partial_circle))
        #assert len(cycle_) == len(partial_circle) - 1, "What you found is not a hamiltonian cycle"
        #assert cycle_ == list(range(1, graph.dimension+1)), "What you found does not touch all nodes"
        return weight

