"""
=================================================
    Advanced Algorithm - HomeWork1 (2022)
  Master's in Computer Science - University of Padua
    Implementation of Kruskal Naive
==================================================
    <Code Structure>
    
    Class MergeSort:
        funct algorithm
        funct _merge

    class KruskalNaive:
        funct kruskal_naive
        funct _is_acyclic
        funct is_there_a_path
        funct dfs

    class MST:
        funct kruskal_naive
        funct get_mst_weight
    
    class Graph:
        funct __init__
        funct add_vertex
        funct add edge
        funct remove_vertex
        funct weightBetween
    
    funct load_all_dataset
    funct populate_each_Graph_from_Dataset
    funct execute_each_graph_in_dataset
    funct main


    Note: lamda functions weren't used here because of bug found when a random link was missing after each iteration
          resulting into an error of listIndex out of Range
=================================================
     Pseudo-codice Kruskal Naive
    
     Time Complexity: O(m * n)
    
     Kruskal-Naive(G)
         A = empty_set
         sort edges if G by cost
         for each edge e in nondecreasing order of cost
             if A U {e} is acyclic
                 A = A U {e}
         return A

================================================
"""

import sys
from collections import defaultdict
from os import walk, path
import time
import multiprocessing
import math
import gc

class MergeSort:

    def algorithm(self, array, left, right):
        if left < right:
            m = (left + (right - 1)) // 2

            self.algorithm(array, left, m)
            self.algorithm(array, m + 1, right)
            self._merge(array, left, m, right)

    def _merge(self, arr, left, m, right):
        n1 = m - left + 1
        n2 = right - m

        L = [0] * n1
        R = [0] * n2

        for i in range(0, n1):
            L[i] = arr[left + i]

        for j in range(0, n2):
            R[j] = arr[m + 1 + j]

        i = 0
        j = 0
        k = left

        while i < n1 and j < n2:
            (_, _, w1) = L[i]
            (_, _, w2) = R[j]

            if int(w1) <= int(w2):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1

            k += 1

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

class KruskalNaive:

    def kruskal_naive(self, G):

        # Link that will contain Minimum Spanning Tree
        A = Graph()

        # Add all vertices of graph G to graph A
        #
        # Time complexity: O(n)
        for i in range(len(G.V)):
            A.add_vertex(i + 1)

        # Sort the sides by their weight, in ascending order 
        # Can also use lambda fun but we are facing an error
        # Time complexity: O(m * log(m)))
        merge_sort = MergeSort()
        merge_sort.algorithm(G.E, 0, len(G.E) - 1)

        # Time complexity: O(m * n)
        for (u, v, w) in G.E:
            if self._is_acyclic(A, (u, v, w)):
                A.add_edge(u, v, w)

            # Stop when there is n - 1 arcs
            if len(A.E) == (len(G.V) - 1):
                break

        return A

    # Check if the input graph is acyclic or not
    #
    # Time complexity:: O(m)
    def _is_acyclic(self, A, e):
        (u, v, w) = e

        # Check if arc is not a self-loop
        if u != v:

            # If  one of the two arc nodes is not present in the graph,There won't be a loop,
            # If both nodes are present in the graph, then check if the graph is acyclic
            if A.graph[u] == [] or A.graph[v] == []:
                return True
            else:
                return not self.is_there_a_path(A, u, v)
        else:
            return False

    # Call modified DFS
    #
    # Time complexity:: O(m)
    def is_there_a_path(self, G, source_node, destination_node):

        # Set all vertices as unvisited
        visited = [False] * (len(G.V) + 1)

        return self.dfs(G, source_node, destination_node, visited)

    # Check if there is a path from source_node to destination_node
    #
    # Time complexity:: O(m)
    def dfs(self, G, current_node, destination_node, visited):
        if destination_node == current_node:
            return True

        visited[current_node] = True

        for e in G.graph[current_node]:
            (u, w) = e
            if not visited[u] and self.dfs(G, u, destination_node, visited):
                return True

        return False


class MST:
    #Main Program to call Kruskal core function and get_mst_weight function
    #Just a calling function
    def kruskal_naive(self, G):
        algorithm = KruskalNaive()
        return algorithm.kruskal_naive(G)

    def get_mst_weight(self, E): # Finding weight for MST
        summation = 0
        for (u, v, w) in E:
            summation += int(w)

        return summation

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)  # Adjacency list
        self.V = set()
        self.E = []
          
    def add_vertex(self, value: int):
        self.V.add(value)

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
            if (self.E[index][0] == firstNode and self.E[index][1] == secondNode) or (self.E[index][1] == firstNode and self.E[index][0] == secondNode):
                minWeight = self.E[index][2]
                break
        return minWeight

def load_all_dataset(dirpath):
    print("Loading dataset files...", end="")
    sys.stdout.flush()

    graphs = []
    filenames = []

    for root, dirs, files in walk(dirpath):  # load filenames
        for filename in files:
            filenames.append(filename)
    filenames.sort() 

    for file in filenames:  # load files
        g = populate_each_Graph_from_Dataset(dirpath + '/' + file) #Reading and Popolulating each dataset and appending
        graphs.append(g)

    print("DONE")
    sys.stdout.flush()

    return graphs

def populate_each_Graph_from_Dataset(filepath):
    
    file = open(filepath, 'r')
    g = Graph()
    formatted_file = file.read().split('\n')
    n_vertices, n_edges = int(formatted_file[0].split(
        ' ')[0]), int(formatted_file[0].split(' ')[1])

    for i in range(n_edges):
        row = formatted_file[i+1].split(' ')
        g.add_vertex(int(row[0]))
        g.add_vertex(int(row[1]))
        g.add_edge(int(row[0]), int(row[1]), int(row[2]))
        #print(int(row[0]), int(row[1]), int(row[2])) # For error checking

    file.close()

    return g

def execute_each_graph_in_dataset(outputfile, graph, filenumber, fileResultLock):

    executionTimes = 1

    localStartTime = time.perf_counter_ns() #counter for bench marking in ns
    gc.disable() # Garbage Collector disabled

    #==============================
    #Main part of program (Executing Kruskel)
    mst = MST()
    final_graph = mst.kruskal_naive(graph)
    kw = mst.get_mst_weight(final_graph.E)
    #======================================
 
    gc.enable() # Garbage Collector Enabled
    localEndTime = time.perf_counter_ns()-localStartTime

    # If the running time < 1 second, run it n times
    # such as to get closer to 1 second and average it
    # The time in seconds is equal to the nanoseconds divided by 1,000,000,000 = 1e-9

    if localEndTime <= 1000000000:  # localEndTime is in ns
        
        #As num of vertices and edges in a dataset increase so does the localEndTime
        # Ref taken from Lab Exersice
        numCalls = 1000000000//localEndTime #  	Floor division 1s/localTime

        loopStartTime = time.perf_counter_ns()
        gc.disable()
        for i in range(0, numCalls):
            mst = MST()
            final_graph = mst.kruskal_naive(graph)
            kw = mst.get_mst_weight(final_graph.E)
            
        gc.enable()
        loopEndTime = time.perf_counter_ns() - loopStartTime
        rightTime = loopEndTime/numCalls
        executionTimes = numCalls
    else:
        rightTime = localEndTime
    

    # Once done, append the results to a file
    # with the following structure:
    # Note: the Same CSV export Structure is used for all Algorithms

    # ======================================================================
    # dataset number | n vertex | n edges | nano seconds time | seconds time | weight | exe times
    # ======================================================================
  
    with fileResultLock: 
        file_object = open(outputfile, 'a')
        # {:.7f} atleast
        file_object.write(str(filenumber)+ "," + str(len(graph.V))+ "," +str(len(graph.E))+ "," + "{:.7f}".format(rightTime) + "," + "{:.7f}".format(rightTime/1000000000)+ "," +str(kw) + "," +str(executionTimes)+ "\n")
        file_object.close()
    

def main():
    
    # Address to 'mst_dataset' folder
    dir_folder='D:/University Data/PADUA/2nd Semester/Adv Algo/HomeWork/1/mst_dataset'
    mul_lock = multiprocessing.Lock()
    start = time.time()  # Program start timer
    # Set for creating a graph
    graphs=[]
    assert path.isdir(dir_folder), "File or folder not found"
    
    #Load all datasets from the folder
    if path.isdir(dir_folder):
        graphs = load_all_dataset(dir_folder)
    
    #graphs has all dataset values in it
    #Reading one dataset at a time & showing the result
    
    print("Executing Kruskal Naive...")
    datasetNumber = 1
    output = "./output_kruskal_n.csv"

    #Multithreading is a problem in Python so
    for graph in graphs:
        execute_each_graph_in_dataset(output, graph, datasetNumber,mul_lock)
        datasetNumber += 1    
    
    print(" Total execution time: " + str(round(time.time()-start, 8)) + "s") # Sum of all time taken to compute graph

if __name__ == "__main__":
    main()