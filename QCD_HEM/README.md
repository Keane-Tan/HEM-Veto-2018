# Sample Code for Creating Ratio Plots and Evaluating Veto Performance

In this example, the HEM vetos are pT>25 and:

-2.07 + 0.025n < phi < 870 + 0.025n

-3.5 + 0.025n < eta < -1.40 + 0.025n

where n = 1, 2, ..., 21

To create ratio plots of QCD (HEM) to QCD for the kinematic distributions -- phi MET, phi jet1, phi jet2, MET, and Delta phi, run
```
cd Pt25
./runRatio.sh
```


After running the lines above, results.txt should now contain 7 rows of numbers. Each row contains 21 numbers (1 number for each HEM veto). The meaning of each row is as follows:
1. Percentage of QCD events removed by the veto
1. Percentage of QCD (HEM) events removed
1. FOM for phi MET
1. FOM for MET
1. FOM for Delta phi
1. FOM for phi jet 1
1. FOM for phi jet 2

FOM (Figure of Merit) is the sum over all bins of the absolute difference of the ratio in the ratio plot and 1.

To compare the performance of the different vetos by looking at the FOM, you may run
```
python FastCopy.py
```
and copy the values in results.txt over to HEM_Performance_Comparison.ipynb in the home directory.
