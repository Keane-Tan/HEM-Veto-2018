# Sample Code for Calculating Signal Effiencies after Applying a HEM Veto

In this example, the HEM veto is pT &#60 30, -3.05 &#60 eta &#60 -1.35, -1.62 &#60 phi &#60 -0.82, run

```
python ratioPlot_Signal.py
```

the results.txt file will store 3 rows of outputs, with 66 outputs in each row (since there are 66 signal samples). The meaning of each row is as follows:
1. Name of the signal sample
1. Percentage of signal events removed by the HEM veto
1. Percentage of signal events removed by the original HEM veto (pT &#x003C 30, -3.0 &#x003C eta &#x003C -1.4, -1.57 &#x003C phi &#x003C -0.87)

You may copy and paste the output to Signal_Efficiency_Test.ipynb to compare signal efficiency of different HEM vetoes.

