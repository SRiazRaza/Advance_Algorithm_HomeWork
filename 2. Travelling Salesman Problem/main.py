"""
=================================================
    Advanced Algorithm - HomeWork 2 (2022)
  Master's in Computer Science - University of Padua
    ** Implementation of TSP **
    + 2-Approximation with Prims MST
    + Nearest Neighbour (Heuristic)
    + Random Insertion (Heuristic) 
==================================================
"""
import argparse
from random import randint
import gc
from data_structures.tsp import TSP
from algorithms.two_approximation import TwoApproximation
from algorithms.nearestneighbor import NearestNeighbor
from algorithms.altered_random_insertion import RandomInsertion
import sys
from os import walk, path
import time

def load_all_dataset(dirpath):
    print("Loading dataset files...", end="")
    sys.stdout.flush()

    tsps = []
    filenames = []

    for  root, dirs, files in walk(dirpath,topdown=True):  # load filenames
        for filename in files:
            filenames.append(filename)
    #print(filenames)
    filenames.sort() 

    for file in filenames:  # load files
        p = populateTSPFromFile(dirpath + '/' + file)
        tsps.append(p)

    print("DONE")
    sys.stdout.flush()

    return tsps #List of adjecent matrix 

def populateTSPFromFile(filepath):
    file = open(filepath, 'r')
    formatted_file = file.read().split('\n')
    tsp = TSP()

    a = 0
    for i in range(10):
        a += 1 # (i+1) past the NODE_COORD_SECTION

        if formatted_file[i].split(':')[0].strip() == "NAME":
            tsp.name = formatted_file[i].split(':')[1].strip()
            
        elif formatted_file[i].split(':')[0].strip() == "EDGE_WEIGHT_TYPE":
            tsp.etype = formatted_file[i].split(':')[1].strip()

        elif formatted_file[i].split(':')[0].strip() == "DIMENSION":
            tsp.dimension = int(formatted_file[i].split(':')[1].strip())
    
        elif formatted_file[i] == "NODE_COORD_SECTION":
            break

    if a == 10:
        print("Non")
        exit()

    for i in range(tsp.dimension):
        row = formatted_file[i+a].split(' ')
        tsp.add_node(int(row[0]), float(row[1]), float(row[2]))
    file.close()

    tsp.calculateAdjMatrix()  # A single adjecent Matrix
    #tsp.printAdjMatrix()
    #print(tsp)

    return tsp
"""
Execution of a single graph

    outputfile = result save file
    algoname = type of algorithm to run
    graph = starting graph in input

"""
def execute_each_graph_in_dataset(outputfile,algoname, tsp ):
    executionTimes = 1

    localStartTime = time.perf_counter_ns() #counter for bench marking in ns
    gc.disable() # Garbage Collector disabled

    #==============================
    #Main part of program (Executing algo sequentially)
    if algoname =='2ap':
        final = TwoApproximation()
        res = final.algorithm(tsp)
        
    elif algoname == 'nn':
        res = NearestNeighbor().algorithm(tsp)

    elif algoname == 'ri':
        res = RandomInsertion().algorithm(tsp)
        
    #======================================


    # If the running time < 1 second, run it n times
    # such as to get closer to 1 second and average it
    # The time in seconds is equal to the nanoseconds divided by 1,000,000,000 = 1e-9

    gc.enable()
    localEndTime = time.perf_counter_ns() - localStartTime

    # If the running time is less than 1 second, I run it n times
    # such as to get closer to 1 second
    # and I average it

    if localEndTime <= 1000000000: 
        #As num of vertices and edges in a dataset increase so does the localEndTime
        # Ref taken from Lab Exersice
        numCalls = 1000000000//localEndTime #  	Floor division 1s/localTime
        loopStartTime = time.perf_counter_ns()
        gc.disable()
        for i in range(0, numCalls):

            if algoname =='2ap':
                final = TwoApproximation()
                res = final.algorithm(tsp)
                
            elif algoname == 'nn':
                res = NearestNeighbor().algorithm(tsp)

            elif algoname == 'ri':
                res = RandomInsertion().algorithm(tsp)

        gc.enable()
        loopEndTime = time.perf_counter_ns() - loopStartTime
        rightTime = loopEndTime/numCalls
        executionTimes = numCalls
    else:
        rightTime = localEndTime


    # Once done, append the results to a file
    # with the following structure:
    # Note: the Same CSV export Structure is used for all Algorithms

    # OUTPUT
    # ======================================================================
    # dataset name | tsp result | ns time | s time | exe times
    # ======================================================================

    file_object = open(outputfile, 'a')
    file_object.write("{:<15},{:<15},{:<12},{:<20},{:<20},{:<20}".format(tsp.name,tsp.dimension,str(int(res)), str(rightTime),'{:.7f}'.format(rightTime/1000000000),str(executionTimes)))
    file_object.write('\n')
    file_object.close()

def execute_all_graph(tsps):

    #======= 2 approx ==============
    print('Executing 2 approximation...')
    output = './output_2approx.csv'

    for tsp in tsps:
        execute_each_graph_in_dataset(output, '2ap' , tsp)
    #=================================

    #======= Nearest Neighbors ========
    print('Executing Nearest Neighbors...')
    output = './output_nearest_neighbor.csv'

    for tsp in tsps:
        execute_each_graph_in_dataset(output, 'nn', tsp)
    #==================================

    #================ Random ==========
    print('Executing Random Insertion...')
    output = './output_alt_random_insertion.csv'

    for tsp in tsps:
        execute_each_graph_in_dataset(output, 'ri', tsp)
    #==================================

def main():

    start = time.time()  # Program Start Timer

    # Please change the directory of this variable to the folder where all datasets files exist
    dirpath='D:/University Data/PADUA/2nd Semester/Adv Algo/HomeWork/2/dataset/tsp_dataset'

    assert path.isdir(dirpath), "File or folder not found"

    if path.isdir(dirpath):
        tsps = load_all_dataset(dirpath)
    
    execute_all_graph(tsps)
    #print(int(TSP().dimension+1))
    print(" Total execution time: " + str(round(time.time()-start, 8)) + "s" )


if __name__ == "__main__":

    main()