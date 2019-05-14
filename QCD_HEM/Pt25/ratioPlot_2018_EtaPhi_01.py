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

file_noHEM = "root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/Run2ProductionV16/Skims/tree_dijetmtdetahad/tree_QCD_Pt-15to7000_MC2018.root"
file_HEM = "root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/Run2ProductionV16/Skims/tree_dijetmtdetahad/tree_QCD_Pt-15to7000_MC2018HEM.root"

# luminosity in inverse picobarn
lumi = 59.5 * 1000

# veto: pT > 30, -3.0 < eta < -1.4, -1.57 < phi < -0.87
EtaLow = np.arange(-3.0,-3.51,-0.05/2)[:6]
EtaHigh = np.arange(-1.40,-0.89,0.05/2)[:6]
PhiLow = np.arange(-1.57,-2.08,-0.05/2)[:6]
PhiHigh = np.arange(-0.87,-0.36,0.05/2)[:6]

for k in range(len(EtaLow)):
	print k
	# Defining histograms
	phiMET = TH1F("phiMET", "phiMET", 50, -np.pi, np.pi)
	METH = TH1F("MET", "MET", 50, 0, 1500)
	DeltaPhi = TH1F("DeltaPhi", "DeltaPhi", 50, 0, 1)
	phi1 = TH1F("phi1", "phi1", 50, -np.pi, np.pi)
	phi2 = TH1F("phi2", "phi2", 50, -np.pi, np.pi)

	phiMET_HEM = TH1F("phiMET_HEM", (";; number of events"), 50, -np.pi, np.pi)
	METH_HEM = TH1F("MET_HEM", (";; number of events"), 50, 0, 1500)
	DeltaPhi_HEM = TH1F("DeltaPhi_HEM", (";; number of events"), 50, 0, 1)
	phi1_HEM = TH1F("phi1_HEM", (";; number of events"), 50, -np.pi, np.pi)
	phi2_HEM = TH1F("phi2_HEM", (";; number of events"), 50, -np.pi, np.pi)

	# Veto parameters
	Ptmax = 25
	EtaL = EtaLow[k]
	EtaH = EtaHigh[k]
	PhiL = PhiLow[k]
	PhiH = PhiHigh[k]

	totEvent_noHEM = 0
	totEvent_HEM = 0
	noHEM_cut = 0
	HEM_cut = 0

	# no HEM
	tf = r.TFile.Open(file_noHEM)
	tr = tf.Get('tree')

	numberOfEntries = tr.GetEntries()
	for entry in range(numberOfEntries):
		tr.GetEntry(entry)

		npass = 1

		w = tr.Weight
		totEvent_noHEM += w*lumi

		nJet = tr.Jets.size()
	# veto: pT > 30, -3.0 < eta < -1.4, -1.57 < phi < -0.87
		for i in range(nJet):
			jet_i = tr.Jets[i]
			if jet_i.Pt() > Ptmax and EtaL < jet_i.Eta() < EtaH and PhiL < jet_i.Phi() < PhiH:
				npass = 0
		if npass == 1:
			METPhi = tr.METPhi
			MET = tr.MET
			FJet1 = tr.JetsAK8[0]
			FJet2 = tr.JetsAK8[1]
		
			## calculate min DeltaPhi
			dphi1 = deltaPhi(FJet1.Phi(),METPhi)
			dphi2 = deltaPhi(FJet2.Phi(),METPhi)
			minDPhi = np.amin([dphi1,dphi2])

			phiMET.Fill(METPhi,w*lumi)
			METH.Fill(MET,w*lumi)
			DeltaPhi.Fill(minDPhi,w*lumi)
			phi1.Fill(FJet1.Phi(),w*lumi)
			phi2.Fill(FJet2.Phi(),w*lumi)

			noHEM_cut += w*lumi

	# HEM
	tf = r.TFile.Open(file_HEM)
	tr = tf.Get('tree')

	for entry in range(numberOfEntries):
		tr.GetEntry(entry)

		npass = 1
	
		w = tr.Weight

		totEvent_HEM += w*lumi

		nJet = tr.Jets.size()
	# veto: pT > 30, -3.0 < eta < -1.4, -1.57 < phi < -0.87
		for i in range(nJet):
			jet_i = tr.Jets[i]
			if jet_i.Pt() > Ptmax and EtaL < jet_i.Eta() < EtaH and PhiL < jet_i.Phi() < PhiH:
				npass = 0
		if npass == 1:
			METPhi = tr.METPhi
			MET = tr.MET
			FJet1 = tr.JetsAK8[0]
			FJet2 = tr.JetsAK8[1]
		
			## calculate min DeltaPhi
			dphi1 = deltaPhi(FJet1.Phi(),METPhi)
			dphi2 = deltaPhi(FJet2.Phi(),METPhi)
			minDPhi = np.amin([dphi1,dphi2])

			phiMET_HEM.Fill(METPhi,w*lumi)
			METH_HEM.Fill(MET,w*lumi)
			DeltaPhi_HEM.Fill(minDPhi,w*lumi)
			phi1_HEM.Fill(FJet1.Phi(),w*lumi)
			phi2_HEM.Fill(FJet2.Phi(),w*lumi)
			
			HEM_cut += w*lumi

	# Percentage of Events Removed
	pnoHEM = (totEvent_noHEM - noHEM_cut)*100./float(totEvent_noHEM)
	pHEM = (totEvent_HEM - HEM_cut)*100./float(totEvent_HEM)
	
	# label for the image files
	pML = 'phiMET'
	mETL = 'MET'
	DPL = 'DeltaPhi'
	p1L = 'phi1'
	p2L = 'phi2'

	SOR1 = ratioplot(phiMET_HEM,phiMET,'#phi(#slash{E}_{T})', pML + str(Ptmax) + "_EtaLow" + str(EtaL))
	SOR2 = ratioplot(METH_HEM,METH,'#slash{E}_{T} #[]{GeV}', mETL + str(Ptmax) + "_EtaLow" + str(EtaL))
	SOR3 = ratioplot(DeltaPhi_HEM,DeltaPhi,'#Delta#phi_{min}', DPL + str(Ptmax) + "_EtaLow" + str(EtaL))
	SOR4 = ratioplot(phi1_HEM,phi1,'#phi(j_{1})', p1L + str(Ptmax) + "_EtaLow" + str(EtaL))
	SOR5 = ratioplot(phi2_HEM,phi2,'#phi(j_{2})', p2L + str(Ptmax) + "_EtaLow" + str(EtaL))

	# a list of all the results to be saved
	rnum = [pnoHEM,pHEM,SOR1,SOR2,SOR3,SOR4,SOR5]

	# save results to results.txt
	print k
	print pnoHEM
	if k == 0:
		rfile = open('results.txt','r+')
		rfile.truncate(0) # clear the content in a file	
		f1 = rfile.readlines()	
		f1.append('%4.3f\n%4.3f\n%4.3f\n%4.3f\n%4.3f\n%4.3f\n%4.3f\n' % (pnoHEM,pHEM,SOR1,SOR2,SOR3,SOR4,SOR5))
		rfile.seek(0) 	# this together with .truncate() allows us to overwrite the text file
		rfile.writelines(f1)
		rfile.truncate()
		rfile.close()
	else:
		rfile = open('results.txt','r+')
		f1 = rfile.readlines()
		for j in range(len(f1)):
			f1[j] = list(f1[j])
			f1[j].insert(-1,'\t%4.3f' % (rnum[j]))
			f1[j] = ''.join(f1[j])
		rfile.seek(0)
		rfile.writelines(f1)
		rfile.truncate()
		rfile.close()

#jet_i.Pt() > Ptmax and EtaL < jet_i.Eta() < EtaH and PhiL < jet_i.Phi() < PhiH
	print("Percentage removed for no HEM (Pt>" + str(Ptmax) + ", " + str(EtaL) +"<Eta<"+ str(EtaH) + ", " + str(PhiL) +"<phi<"+ str(PhiH)+"): %4.3f %%" % (pnoHEM))
	print("Percentage removed for HEM (Pt>" + str(Ptmax) + ", " + str(EtaL) +"<Eta<"+ str(EtaH) + ", " + str(PhiL) +"<phi<"+ str(PhiH)+"): %4.3f %%" % (pHEM))
	print("Pt>" + str(Ptmax) + ", " + str(EtaL) +"<Eta<"+ str(EtaH) + ", " + str(PhiL) +"<phi<"+ str(PhiH) + " " + pML + ": %4.3f" % (SOR1))
	print("Pt>" + str(Ptmax) + ", " + str(EtaL) +"<Eta<"+ str(EtaH) + ", " + str(PhiL) +"<phi<"+ str(PhiH) + " " + mETL + ": %4.3f" % (SOR2))
	print("Pt>" + str(Ptmax) + ", " + str(EtaL) +"<Eta<"+ str(EtaH) + ", " + str(PhiL) +"<phi<"+ str(PhiH) + " " + DPL + ": %4.3f" % (SOR3))
	print("Pt>" + str(Ptmax) + ", " + str(EtaL) +"<Eta<"+ str(EtaH) + ", " + str(PhiL) +"<phi<"+ str(PhiH) + " " + p1L + ": %4.3f" % (SOR4))
	print("Pt>" + str(Ptmax) + ", " + str(EtaL) +"<Eta<"+ str(EtaH) + ", " + str(PhiL) +"<phi<"+ str(PhiH) + " " + p2L + ": %4.3f" % (SOR5))

	tf.Close()
# need to add sum of the ratios
# may add a loop for using different pT
# optimize the pT value by making sure that the sum of ratios is as close to zero as possible
# may change the bin size to 50
# fix starting yield for HEM
