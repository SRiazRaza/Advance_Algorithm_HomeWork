<Description>
In this report we will compare the execution times and the quality of the solutions that can be obtained with different approximation algorithms.
1.	Nearest Neighbor Algorithm (Constructive Heuristics).
2.	Random Insertion Algorithm (Constructive Heuristics).
3.	2-approximate algorithm based on MST.

You can find HW2_Report.pdf in the Report folder.The report summarizes the result by answering the following questions:

1. Run the three algorithms (the two constructive heuristics and 2-approximate) on the 13 graphs of the dataset. 
Show your results in a table like the one below. The rows in the table correspond to the problem instances(Question#1 in Report). 
The columns show, for each algorithm, the weight of the approximate solution, the execution time and the relative error calculated as: approxSol-optimalSol/optimalSol.

2. Comment on the results you have obtained: how do the algorithms behave with respect to the various instances?
There is an algorithm that is always better than the others? Which of the three algorithms you have implemented is more efficient?

==========================================================================
<For running Code>

Before running make sure  that dir address(in each file) points to your dataset folder:

# Please change the directory of this variable to the folder where all datasets files exist
dirpath='D:/University Data/PADUA/2nd Semester/Adv Algo/HomeWork/2/dataset/tsp_dataset'

Goto main.py
Then run the file just click dubug button.

=====================================================================================
<For runnig visualize file>
There's a file named "Visualize_TSP.ipynb", it's created for:
To compute asymptotic complexity and visualize and compare the results of our work. Please open this file at:
	.\complexities and output\Visualize_TSP.ipynb

Make sure that each output file from algorithms are in the same folder as Visualize_TSP.

Output Files for the result are named as
1. output_2approx.csv
2. output_nearest_neighbour.csv
3. output_random_insertion.csv

===============================================================================

<For Report>
.\HW2_Report.pdf

===============================================================================