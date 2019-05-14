# run this only after you have run ratioPlot_2018_EtaPhi_01.py, ...02.py, ...03.py, and ...04.py
# this makes it easier to copy and paste the results into Jupyter-notebook
rfile = open('results.txt','r+')
f1 = rfile.readlines()
for j in range(len(f1)):
	f1[j] = list(f1[j])
	for n, i in enumerate(f1[j]):
	    if i == '\t':
		f1[j][n] = ','
	f1[j] = ''.join(f1[j])
rfile.seek(0)
rfile.writelines(f1)
rfile.truncate()
rfile.close()
