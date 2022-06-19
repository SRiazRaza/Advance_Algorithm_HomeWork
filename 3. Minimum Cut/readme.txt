<Description>
In this report we are comparing the performance of two algorithms for the min-cut problem for weighted graphs. 
1. Stoer and Wagner's deterministic algorithm. 
2. Karger and Stein's randomized algorithm.

You can find HW3_Report.pdf in the Report folder.The report summarizes the result by answering the following questions:

1. 	Run the two algorithms you have implemented on the graphs of the dataset. For the Karger e Stein algorithm, use several repetitions that guarantees a probability to obtain a global min-cut for at least 1−1/n.
	Measure the execution times of the algorithms and create a graph showing the increase of execution times as the number of vertices in the graph increases. 
	Compare the measured times with the asymptotic complexity of the algorithms. For each problem instance, report the weight of the minimum cut obtains by your code.

2.	Measure the discovery time of the Karger and Stein algorithm. The discovery time is the instant (in seconds) when the algorithm finds the minimum cost cut. 
	Compare the discovery time with the overall execution time for each of the graphs in the dataset.

3. 	Comment on the results you have obtained: how do the algorithms behave with respect to the various instances? 
	There is an algorithm that is always better than the other? Which algorithm is more efficient?
==========================================================================
<For running Code>

Before running make sure  that dir address(in each file) points to your dataset folder:

# Please change the directory of this variable to the folder where all datasets files exist
dirpath=.\HomeWork\3. Minimum Cut\dataset'

Goto main.py
Then run the file just click dubug button.

=====================================================================================
<For runnig visualize file>
There's a file named "Visualize.ipynb", it's created for:
To compute asymptotic complexity and visualize and compare the results of our work. Please open this file at:
	.\Result and output\Visualize.ipynb

Make sure that each output file from algorithms are in the same folder as Visualize.

Output Files for the result are named as
1. output_kargerstein.csv
2. output_stoerwagner.csv

===============================================================================

<For Report>
.\Report\HW3_Report.pdf

===============================================================================