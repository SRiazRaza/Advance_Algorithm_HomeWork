<Description of this Folder>
In this homework, we will do comparison and analysis between three algorithms for calculating the Minimum Spanning Tree problem given below:
1.	Prim's Algorithm implemented with a Heap
2.	Naive Kruskal's Algorithm having O(MN) complexity
3.	Efficient Kruskal's Algorithm based on Union-Find

You can find HW1_Report.pdf in the Report folder.The report summarizes the result by answering the following questions:

1.      Run the three algorithms you have implemented (Prim, Kruskal naive and Kruskal efficient) on the graphs of the dataset.
	Measure the execution times of the three algorithms and create a graph showing the increase of execution times as the number of vertices in the graph increases.
	Compare the measured times with the asymptotic complexity of the algorithms.
	For each problem instance, report the weight of the minimum spanning tree obtained by your code.

2. 	Comment on the results you have obtained: how do the algorithms behave with respect to the various instances? There is an algorithm that is always better than the others? 
   	Which of the three algorithms you have implemented is more efficient?

======================================================================================
<For running Code>

Before running make sure that dir address(in each file) points to your dataset folder:

dir_folder='D:/University Data/PADUA/2nd Semester/Adv Algo/HomeWork/1/mst_dataset'

Then run the file just click dubug button.

=====================================================================================
<For running visualize file>
There's a file named "Visualize_MST.ipynb", it's created for:
To compute asymptotic complexity and visualize and compare the results of our work. Please open this file at:
	.\Complexities and Output\Visualize_MST.ipynb

Make sure that each output file from algorithms is in the same folder as Visualize_MST.

Output Files for the result are named as
1. output_kruskal_n
2. output_kruskal_uf
3. output_prim

===============================================================================

<For Report>
.\Report\HW1_Report.pdf

===============================================================================
