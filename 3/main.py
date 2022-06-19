"""
=================================================
    Advanced Algorithm - HomeWork 3 (2022)
  Master's in Computer Science - University of Padua
    ** Min-Cut problem for weighted graphs **
    Stoer and Wagner's deterministic algorithm 
    Karger and Stein's randomized algorithm
==================================================
"""


from algorithms.stoerwagner import StoerWagner
from algorithms.karger_stein import KargerStein
from data_structures.graph import Graph
from data_structures.karger_graph import KargerGraph
import sys
from os import path
import time
import gc
from os import walk

def loadFromFolder(dirpath, is_karger: bool):
    print("Loading dataset files...", end="")
    sys.stdout.flush()

    graphs = []
    filenames = []

    for root, dirs, files in walk(dirpath):  # load filenames
        for filename in files:
            filenames.append(filename)
    filenames.sort() 

    for file in filenames:  # load files
        g = populateGraphFromFile(dirpath + '/' + file, is_karger)
        graphs.append(g)

    print("DONE")
    sys.stdout.flush()

    return graphs


def loadData(dirpath: str, is_karger: bool):
    graphs = loadFromFolder(dirpath, is_karger)

    return graphs

def populateGraphFromFile(filepath, is_karger: bool):

    file = open(filepath, 'r')
    g = None

    if is_karger:
        formatted_file = file.read().split('\n')
        n_vertices, n_edges = int(formatted_file[0].split(
            ' ')[0]), int(formatted_file[0].split(' ')[1])

        g = KargerGraph(n_vertices, n_edges)

        for i in range(n_edges):
            row = formatted_file[i + 1].split(' ')
            g.add_edge(int(row[0]), int(row[1]), int(row[2]))

    else:
        g = Graph()
        formatted_file = file.read().split('\n')
        n_vertices, n_edges = int(formatted_file[0].split(
            ' ')[0]), int(formatted_file[0].split(' ')[1])
        g.totalVertex, g.totalEdges = n_vertices, n_edges
        g.datasetName = path.basename(file.name)

        for i in range(n_edges):
            row = formatted_file[i+1].split(' ')
            g.add_vertex(int(row[0]))
            g.add_vertex(int(row[1]))
            g.add_edge(int(row[0]), int(row[1]), int(row[2]))

    file.close()
    return g


def execute_each_graph_in_dataset(outputfile, algoname, graph, filenumber):

    #outputfile = result save file
    #algoname = type of algorithm to run
    #graph = starting graph in input
    #filenumber = dataset number

    executionTimes = 1

    localStartTime = time.perf_counter_ns()
    gc.disable()

    if algoname == "sw":

        res = StoerWagner().algorithm(graph)

        gc.enable()
        localEndTime = time.perf_counter_ns()-localStartTime

    # If the running time < 1 second, run it n times
    # such as to get closer to 1 second and average it
    # The time in seconds is equal to the nanoseconds divided by 1,000,000,000 = 1e-9

        if localEndTime <= 1000000000: 
            numCalls = 1000000000//localEndTime
            loopStartTime = time.perf_counter_ns()
            gc.disable()

            for i in range(0, numCalls):

                if algoname == "sw":
                    res = StoerWagner().algorithm(graph)

                elif algoname == "ks": #TODO
                    pass
                
            gc.enable()
            loopEndTime = time.perf_counter_ns() - loopStartTime
            rightTime = loopEndTime/numCalls
            executionTimes = numCalls
        else:
            rightTime = localEndTime

    # Once done, append the results to a file
    # with the following structure:
    # Note: the Same CSV export Structure is used for all Algorithms
    # Result of both algorithms are stored in different pattern because of Question#2 asked in the homework
        
        # Stoer and Wagner's deterministic algorithm 
        # ======================================================================
        # dataset number | n vertex | n edges | nano seconds time | seconds time | result | exe times
        # ======================================================================
    
        file_object = open(outputfile, 'a')
        file_object.write(str(filenumber) + "," + str(len(graph.V)) + "," +   str(len(graph.E)) + "," + "{:.7f}".format(rightTime) + "," + "{:.7f}".  format(rightTime/1000000000) + "," + str(res) + "," + str(executionTimes) + "\n")
        file_object.close()


    elif algoname == "ks":
        res = KargerStein(graph)
        min_cut, k, k_min, discovery_time, total_time, n_repetitions, is_threshold_activated = res.measurements()

        # Karger and Stein algorithm
        # ======================================================================
        # dataset number | n vertex | n edges | nano seconds time | seconds time | result | discovery time | rep times | k | k_min | is_treshold_activated
        # ======================================================================

        file_object = open(outputfile, 'a')
        file_object.write(str(filenumber) + "," + str(graph.n_vertices) + "," +   str(graph.n_edges) + "," + "{:.7f}".format(total_time) + "," + "{:.7f}".  format(total_time/1000000000) + "," + str(min_cut) + "," + str(discovery_time) + "," + str(n_repetitions) + "," + str(k) + "," + str(k_min) + "," + str(is_threshold_activated) + "\n")
        file_object.close()

def execute_all(dirpath):
    # Execute algo one by one
    # For each algo load data pass data to the executeSingleGraphCalculus function and execute it
    # In the last csv file data will be represnted as questions asked in homework
    outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"

    # ======= Stoer-Wagner ========
    print("Executing StoerWagner...")
    datasetNumber = 1
    output = "./output_stoerwagner_" + outputfilePostfix

    graphs = loadData(dirpath, False)

    for graph in graphs:
        execute_each_graph_in_dataset(output, "sw", graph, datasetNumber)
        datasetNumber += 1    

    # ======= Karger-Stein ========
    print("Executing Karger-Stein...")
    datasetNumber = 1
    output = "./output_kargerstein_" + outputfilePostfix

    graphs = loadData(dirpath, True)

    for graph in graphs:
        execute_each_graph_in_dataset(output, "ks", graph, datasetNumber)
        datasetNumber += 1    

def main():

    start = time.time()  # Program start timer
    
    # Please change the directory of this variable to the folder where all datasets files exist
    dirpath='D:/University Data/PADUA/2nd Semester/Adv Algo/HomeWork/3/dataset'

    #assert path.isfile(dirpath) or path.isdir(dirpath), "File or folder not found"
    assert path.isdir(dirpath), "File or folder not found"
    execute_all(dirpath)
    print(" Total execution time: " + str(round(time.time()-start, 8)) + "s")

if __name__ == "__main__":
    main()
