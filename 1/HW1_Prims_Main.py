"""
=================================================
    Advanced Algorithm - HomeWork1 (2022)
  Master's in Computer Science - University of Padua
    Implementation of prims with heap

    <Code Structure>

HW1_Prims_Main:
    funct primsMSTAlgorithm:
        funct updateHeap

    funct graph:
    funct load_all_dataset
    funct execute_each_graph_in_dataset
    funct main()

=================================================
Pseudo-code of prims algorithm implemented with HEAP
    
    
    
    Let X = nodes covered so far, V = all the nodes in the graph, E = all the edges in the graph
    Pick an arbitrary initial node s and put that into X
    for v ∈ V - X
        key[v] = cheapest edge (u,v) with v ∈ X
    while X ≠ V:
        let v = extract-min(heap) (i.e. v is the node which has the minimal edge cost into X)
        Add v to X
        for each edge v, w ∈ E
            if w ∈ V - X (i.e. w is a node which hasn’t yet been covered)
                Delete w from heap
                recompute key[w] = min(key[w], weight(v, w)) (key[w] would only change if the weight of the edge (v,w) is less than the current weight for that key).
                reinsert w into the heap


================================================
"""

from fileinput import filename
import sys
from heap import Heap
import sys
from collections import defaultdict
from os import walk, path
import time
import multiprocessing
import math
import gc

def primsMSTAlgorithm(adjList):
	'''
	Prim's Minimum Spanning Tree (MST) Algorithm 
	It finds a MST of an undirected graph
	Args:
		adjList: a dictionary, as a realization of an adjacency list, in the form
				 adjList[vertex1] = [(vertex21,weight1,edgeId1), (vertex22,weight2,edgeId2), ...]
				 Note: Every vertex should have an entry in the adjList
	Returns:
		mst: a set of all the edges (ids) that constitute the minimum spanning tree
	'''
	def updateHeap(v):
		'''
		Updates the heap with entries of all the vertices incident to vertex v that was recently explored
		Args:
			v: a vertex that was recently explored
		'''
		for vertex,weight,edgeID in adjList[v]:
			if vertex not in explored:
				# Updates (!) the weight and reinserts the element into the heap
				element = unexplored.delete(vertex)
				if element and element[0] < weight: unexplored.insert(element)
				else: unexplored.insert((weight,vertex,edgeID))

	source = list(adjList.keys())[0]  # Chooses an arbitrary vertex as the starting point of the algorithm
	# unexplored: a heap with elements of the following format (minWeight, destinationVertex, edgeID)
	unexplored, explored, mst = Heap(), set([source]), set()
	updateHeap(source)

	while unexplored.length():
		weight, vertex, edgeID = unexplored.extractMin()
		explored.add(vertex)
		mst.add(edgeID)
		updateHeap(vertex)
	
	return mst


def graph(filename):
    global numVertices, numEdges 
    '''
	Builds an adjacency list and an incidence list
	Args:
		filename: the name of the file with a representation of the graph. The first line of the file specifies
				  the number of the vertices and the number of the edges. The file is assumed to specify
				  the edges of the graph in the following format: v w e, where v is one vertex of the
				  associated edge, w is the other vertex, and e is the edge's weight
	
	Returns:
		adjList: a dictionary, as a realization of an adjacency list, in the form
				 adjList[vertex1] = [(vertex21,weight1,edgeId1), (vertex22,weight2,edgeId2), ...]
		edgeList: a dictionary, as a realization of an incidence list, in the form
				  edgeList[edgeId] = (vertex1,vertex2,weight)
                  '''
    
    adjList, edgeList = {}, {}
    with open(filename, 'r') as f:
        numbers = f.readline().split()
        numVertices, numEdges = int(numbers[0]), int(numbers[1])
        edgeID = 1
        
        for line in f:
            edge = line.split()
            vertex1, vertex2, weight = int(edge[0]), int(edge[1]), int(edge[2])
			
            if vertex1 in adjList: adjList[vertex1].append((vertex2,weight,edgeID))
            else: adjList[vertex1] = [(vertex2,weight,edgeID)]
            if vertex2 in adjList: adjList[vertex2].append((vertex1,weight,edgeID))
            else: adjList[vertex2] = [(vertex1,weight,edgeID)]
            
            edgeList[edgeID] = (vertex1,vertex2,weight)
            edgeID += 1
            
    return adjList, edgeList

def load_all_dataset(dirpath):
    print("Loading dataset files...", end="")
    sys.stdout.flush()

    filenames = []

    for root, dirs, files in walk(dirpath):  # load filenames
        for filename in files:
            filenames.append(filename)
    filenames.sort() 

    #for file in filenames:  # load files
    #    g = populate_each_Graph_from_Dataset(dirpath + '/' + file) #Reading and Popolulating each dataset and appending
    #    graphs.append(g)

    print("DONE")
    sys.stdout.flush()

    return filenames


def execute_each_graph_in_dataset(outputfile, filenumber, fileResultLock):
  
    output_result = "./output_prim.csv"
    executionTimes = 1
    
    localStartTime = time.perf_counter_ns() #counter for bench marking in ns
    gc.disable() # Garbage Collector disabled

    #=====================================
    ################################
    adjList, edgeList = graph(outputfile)
    mst = primsMSTAlgorithm(adjList)
    cost = 0
	# Computes the sum of the weights of all edges in the MST
    for edgeID in mst:
        cost += edgeList[edgeID][2]  ## Tried to( Cost is computed only one Time)
    #####################################
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
            adjList, edgeList = graph(outputfile)
            mst = primsMSTAlgorithm(adjList)
            cost = 0
            # Computes the sum of the weights of all edges in the MST
            for edgeID in mst:
                cost += edgeList[edgeID][2]  ## Tried to( Cost is computed only one Time)
            
        gc.enable()
        loopEndTime = time.perf_counter_ns() - loopStartTime
        rightTime = loopEndTime/numCalls
        executionTimes = numCalls
    else:
        rightTime = localEndTime
     

    # Once done, append the results to a file
    # with the following structure:
    # Note the Same Structure is used for all Algorithms

    # ======================================================================
    # dataset number | n vertex | n edges | nano seconds time | seconds time | weight | exe times
    # ======================================================================
  
    with fileResultLock: 
       file_object = open(output_result, 'a')
       file_object.write(str(filenumber)+ "," + str(len(graph.V))+ "," +str(len(graph.E))+ "," + "{:.7f}".format(rightTime) + "," + "{:.7f}".format(rightTime/1000000000)+ "," +str(cost) + "," +str(executionTimes)+ "\n")
       file_object.close()

def main():
    
    dir_folder='E:/Advance Algorithm/1/mst_dataset'
    
    fileResultLock = multiprocessing.Lock()

    start = time.time()  # Program start timer
    # Set for creating a graph
    filename=[]
    assert path.isdir(dir_folder), "File or folder not found"
    
    #Load all datasets from the folder
    if path.isdir(dir_folder):
        filename = load_all_dataset(dir_folder)
    
    #graphs has all dataset values in it
    #Reading one dataset at a time & showing the result
    
    print("Executing Prims...")
    datasetNumber = 1
    

    #Multithreading is a problem in Python so
    for file in filename:
        output= dir_folder + '/' + file
        execute_each_graph_in_dataset(output, datasetNumber,fileResultLock)
        datasetNumber += 1    
    
    print(" Total execution time: " + str(round(time.time()-start, 8)) + "s") # Sum of all time taken to compute graph




if __name__ == "__main__":
    main()