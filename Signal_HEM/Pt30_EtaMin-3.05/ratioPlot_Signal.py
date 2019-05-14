from ROOT import TCanvas, TColor, TH1F, TPad, TLine, TLegend
from ROOT import kBlack, kBlue, kRed
import ROOT as r
import numpy as np

def FormatH1(h1):
	h1.SetLineColor(kRed)
	h1.SetMarkerStyle(20)
	h1.SetMarkerColor(kRed)
	h1.GetYaxis().SetTitleSize(20)
	h1.GetYaxis().SetTitleFont(43)
	h1.GetYaxis().SetTitleOffset(1.55)
	h1.SetStats(0)
	# get rid of x values
	h1.GetXaxis().SetLabelOffset(999)
	h1.GetXaxis().SetLabelSize(0)
	return h1
 
def FormatH2(h2):
	h2.SetLineColor(kBlue+1)
	h2.SetMarkerStyle(20)
	h2.SetMarkerColor(kBlue+1)
	return h2
 
def createRatio(h1, h2, xtitle):
	h3 = h1.Clone("h3"+xtitle)
	h3.SetLineColor(kBlack)
	h3.SetMarkerStyle(20)
	h3.SetMarkerColor(kBlack)
	h3.SetTitle("")
	h3.SetMinimum(0)
	h3.SetMaximum(2)
	# Set up plot for markers and errors
	#h3.Sumw2()
	h3.SetStats(0)
	h3.Divide(h2)
 
	# Adjust y-axis settings
	y = h3.GetYaxis()
	y.SetTitle("HEM/nominal")
	y.SetNdivisions(505)
	y.SetTitleSize(20)
	y.SetTitleFont(43)
	y.SetTitleOffset(1.55)
	y.SetLabelFont(43)
	y.SetLabelSize(15)
 
	# Adjust x-axis settings
	x = h3.GetXaxis()
	x.SetTitle(xtitle)
	x.SetTitleSize(20)
	x.SetTitleFont(43)
	x.SetTitleOffset(4.0)
	x.SetLabelFont(43)
	x.SetLabelSize(15)
	x.SetLabelOffset(0.05)
 
	return h3
 
def createCanvasPads():
	c = TCanvas("c", "canvas", 800, 800)
	# Upper histogram plot is pad1
	pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
	pad1.SetBottomMargin(0.03)  # joins upper and lower plot
	pad1.Draw()
	# Lower ratio plot is pad2
	c.cd()  # returns to main canvas before defining pad2
	pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
	pad2.SetTopMargin(0)  # joins upper and lower plot
	pad2.SetBottomMargin(0.3)
	pad2.Draw()
 
	return c, pad1, pad2

def sum_of_ratio(h3):
	SOR = []	
	for i in range(h3.GetNbinsX()):
		if h3.GetBinContent(i) != 0:		
			SOR.append(abs(1 - h3.GetBinContent(i)))
	SOR = np.array(SOR)
	return np.sum(SOR)
 
def ratioplot(hist1,hist2,xtitle,plotname):
	# create required parts
	h1 = FormatH1(hist1)
	h2 = FormatH2(hist2)
	h3 = createRatio(h1, h2, xtitle)
	SOR = sum_of_ratio(h3)
	c, pad1, pad2 = createCanvasPads()

	# draw everything
	pad1.cd()
	h1.Draw("EX0P")
	h2.Draw("SAME EX0P")

	# Legend
	leg = TLegend(0.75,0.8,0.9,0.9)
	leg.AddEntry(h1,"QCD (HEM)", "l")
	leg.AddEntry(h2, "QCD", "l")
	leg.Draw('same')
	## to avoid clipping the bottom zero, redraw a small axis
	#h1.GetYaxis().SetLabelSize(0.0)
	#axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "") 
	#axis.SetLabelFont(43)
	#axis.SetLabelSize(15)
	#axis.Draw()
	pad2.cd()
	h3.Draw("EX0P")

	# line at y = 1 of the ratio plot
	xmin = h1.GetXaxis().GetBinCenter(0)
	xmax = h1.GetXaxis().GetBinCenter(h1.GetNbinsX())
	line = TLine(xmin,1,xmax,1)
	line.SetLineColor(kRed)
	line.SetLineStyle(2)
	line.Draw()

	c.SaveAs(plotname + ".png")
	return SOR

def deltaPhi(fjetPhi,metPhi):
	dphi = fjetPhi - metPhi
	if dphi < -np.pi:
		dphi += 2*np.pi
	if dphi > np.pi:
		dphi -= 2*np.pi

	return abs(dphi)

fileList = open('FileNames.txt','r+')
f1 = fileList.readlines()

file_start = "root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/Run2ProductionV16/Skims/tree_dijetmtdetahad/"
label = []

for j in range(len(f1)):
    file_start = list(file_start)
    label_j = f1[j][:-13].replace("tree_SVJ_mZprime-","SVJ_").replace("mDark-","").replace("rinv-","").replace("alpha-","")
    label.append(label_j)
    f1[j] = list(f1[j])
    f1[j] = f1[j][:-1]
    f1[j] = ''.join(file_start+f1[j])

# luminosity in inverse picobarn
lumi = 59.5 * 1000

for i in range(len(f1)):
	# Signal
	tf = r.TFile.Open(f1[i])
	tr = tf.Get('tree')

	totEvent = 0
	sig_cut = 0 # number of events that pass the cuts
	sig_cut_ori = 0

	numberOfEntries = tr.GetEntries()
	for entry in range(numberOfEntries):
		tr.GetEntry(entry)

		npass = 1
		npass_ori = 1

		totEvent += 1

		nJet = tr.Jets.size()
	# original veto: pT > 30, -3.0 < eta < -1.4, -1.57 < phi < -0.87
		for k in range(nJet):
			jet_i = tr.Jets[k]
			if jet_i.Pt() > 30 and -3.050< jet_i.Eta() <-1.350 and -1.620< jet_i.Phi() <-0.820:
				npass = 0
			if jet_i.Pt() > 30 and -3.0 < jet_i.Eta() < -1.4 and -1.57 < jet_i.Phi() < -0.87:
				npass_ori = 0
		if npass == 1:
			sig_cut += 1
		if npass_ori == 1:
			sig_cut_ori += 1

	prBest = (totEvent - sig_cut)*100./float(totEvent)
	prOri = (totEvent - sig_cut_ori)*100./float(totEvent)
	allR = [prBest,prOri]

	if i == 0:
		rfile = open('results.txt','r+')
		rfile.truncate(0) # clear the content in a file	
		f2 = rfile.readlines()	
		f2.append(label[i]+'\n%4.3f\n%4.3f' % (prBest,prOri))
		rfile.seek(0) 	# this together with .truncate() allows us to overwrite the text file
		rfile.writelines(f2)
		rfile.truncate()
		rfile.close()
	else:
		rfile = open('results.txt','r+')
		f2 = rfile.readlines()
		for m in range(len(f2)):
			f2[m] = list(f2[m])
			if m == 0:
				f2[m].insert(-1,',' + label[i])
			else:		
				f2[m].insert(-1,',%4.3f' % (allR[m-1]))
			f2[m] = ''.join(f2[m])
		rfile.seek(0)
		rfile.writelines(f2)
		rfile.truncate()
		rfile.close()

	print("Percent removed for " + label[i] + " (best veto)    : %4.2f %%" % (prBest))
	print("Percent removed for " + label[i] + " (original veto): %4.2f %%" % (prOri))
	tf.Close()

fileList.close()
# need to add sum of the ratios
# may add a loop for using different pT
# optimize the pT value by making sure that the sum of ratios is as close to zero as possible
# may change the bin size to 50
# fix starting yield for HEM
