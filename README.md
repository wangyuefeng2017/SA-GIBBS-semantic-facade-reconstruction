# SA-GIBBS-semantic-facade-reconstruction

3D FACADE RECONSTRUCTION

Steps:
1. Refining the facade point cloud according to the quality.
2. Transferring the 3D points to 2D plane
3. Running the Simulated Annealing to search for the optimal solution

NOTE: some example has been attached in the folder of example. And 3 kinds of reining method has been put in the folder of fine.

Requirement:
Python 3.5+

Example:
5 facades has been add to the folder for experiment. The ground-truth of face1 and face3 can be found in folder of gt. Apart from existing data, the other datasets can be downloaded as follows:
	Dataset-B: 
Paris-Lille-3D can be downloaded from https://npm3d.fr/paris-lille-3d
	Dataset-C: 
semantic-8 can be downloaded from http://www.semantic3d.net/view_dbase.php?chl=2

Running the code:
Each step is divided separately in the optimization process. The main file can be run to obtain an optimized process.
For the refinement of facade structure, you can run the codes in folder refine.

