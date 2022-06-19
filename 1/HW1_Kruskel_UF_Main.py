"""
=================================================
    Advanced Algorithm - HomeWork1 (2022)
  Master's in Computer Science - University of Padua
    Implementation of Kruskal with Union-Find
==================================================
    <Code Structure>
    
    Class MergeSort:
        funct algorithm
        funct _merge

    class KruskalUnionFind:
        funct kruskal_union_find

    class DisjointSet:
        funct __init__
        funct make_set
        funct find_set
        funct union_by_size

    class MST:
        funct kruskal_union_find
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
     Pseudo-codice Kruskal with Union-Find
    
     Time Complexity: O(m * log(n))
    
     Kruskal-Union-Find(G, w)
       A = empty_set
       for each vertex belongs to G.V
         make-set(v)
       sort the edges of G.E into nondecreasing order by weight w
       for each edge (u, v) belongs to G.E, taken in nondecreasing order by weight
         if find-set(u) != find-set(v)
           A = A U {(u, v)}
           Union(u, v)
       return A

================================================
"""

import csv
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

class KruskalUnionFind:

    def kruskal_union_find(self, G):
        ds = DisjointSet(len(G.V))

        # A is a list that will contain the sides that make up the Minimum Spanning Tree
        A = []

        # Put all the nodes in the DisjointSet data structure
        #
        # Time complexity: : theta(n)
        for v in G.V:
            ds.make_set(int(v))

        # Sort the sides by their WEIGHT, in ascending order
        #
        # Time complexity: teta(m * log(m)))
        merge_sort = MergeSort()
        merge_sort.algorithm(G.E, 0, len(G.E) - 1)

        # Time complexity: O(m * log(n))
        for (u, v, w) in G.E:

            # If the parent of the two nodes is not the same, then insert the side that joins u and v of weight w
            if ds.find_set(int(u)) != ds.find_set(int(v)):
                A.append((u, v, w))
                ds.union_by_size(int(u), int(v))
        return A

class DisjointSet:
    def __init__(self, n: int):

        # This array represents the relatives of the various nodes
        self.parents = [math.inf] * (n + 1)

        # This array represents the various sizes of the nodes
        self.sizes = [0] * (n + 1)

    # Add a node to the data structure
    # Creates a new set consisting of the new element 
    # Time complexity: O(1)
    def make_set(self, x: int):
        self.parents[x] = x
        self.sizes[x] = 1

    # Given a node, it allows to determine which is the parent node of the given element V or which that node belongs
    # Changes each time after  union_by_size is called
    # Time complexity: O(log n)
    def find_set(self, x: int):
        root = x

        while self.parents[root] != root:
            root = self.parents[root]

        return root

    # It allows you to join two nodes under a single tree
    #
    # Time complexity: O(log n)
    def union_by_size(self, x: int, y: int):
        i = self.find_set(x)
        j = self.find_set(y)

        if i != j:
            if self.sizes[i] >= self.sizes[j]:
                self.parents[j] = i
                self.sizes[i] += self.sizes[j]
            else:
                self.parents[i] = j
                self.sizes[j] += self.sizes[i]

class MST:
    #Main Program to call Kruskal core function and get_mst_weight function
    def kruskal_union_find(self, G): #Just a calling function
        algorithm = KruskalUnionFind()
        return algorithm.kruskal_union_find(G)

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
        #print(int(row[0]), int(row[1]), int(row[2]))

    file.close()

    return g

def execute_each_graph_in_dataset(outputfile, graph, filenumber, mul_lock):

    executionTimes = 1

    localStartTime = time.perf_counter_ns() #counter for bench marking in ns
    gc.disable() # Garbage Collector disabled

    #==============================
    #Main part of program (Executing Kruskel)
    mst = MST()
    final_graph = mst.kruskal_union_find(graph)
    kw = mst.get_mst_weight(final_graph)
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
            final_graph = mst.kruskal_union_find(graph)
            kw = mst.get_mst_weight(final_graph)
            
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
    # {:.7f} atleast
    with mul_lock: 
        file_object = open(outputfile, 'a')
        file_object.write(str(filenumber)+ "," + str(len(graph.V))+ "," +str(len(graph.E))+ "," + "{:.7f}".format(rightTime) + "," + "{:.7f}".format(rightTime/1000000000)+ "," +str(kw) + "," +str(executionTimes)+ "\n")
        #print(mul_lock)
        file_object.close()
    

def main():
    
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
    
    print("Executing Kruskal Union Find...")
    datasetNumber = 1
    output = "./output_kruskal_uf.csv"

    #Multithreading is a problem in Python so
    for graph in graphs:
        execute_each_graph_in_dataset(output, graph, datasetNumber,mul_lock)
        datasetNumber += 1    
    
    print(" Total execution time: " + str(round(time.time()-start, 8)) + "s") # Sum of all time taken to compute graph

if __name__ == "__main__":
    main()