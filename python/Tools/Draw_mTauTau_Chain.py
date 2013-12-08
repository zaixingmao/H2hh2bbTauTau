#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os

psfile="mTauTau_withRequirements.eps"

#Title = "No Required b Tags, EleMuLooseVeto on Leg1"
Title = " "

DrawSVMass = False

r.gStyle.SetOptStat(0)
#*******Open input file and find associated tree*******
HChain = r.TChain("ttTreeFinal/eventTree")
ttChain = r.TChain("ttTreeFinal/eventTree")
ZZChain = r.TChain("ttTreeFinal/eventTree")
tool.addFiles(ch=HChain, dirName="/hdfs/store/user/zmao/H2hh-SUB-TT")
tool.addFiles(ch=ttChain, dirName="/hdfs/store/user/zmao/tt-SUB-TT")
tool.addFiles(ch=ZZChain, dirName="/hdfs/store/user/zmao/ZZ2-SUB-TT")

mTauTau_h = r.TH1F("mTauTau_h"," ", 56, 20, 300)
mTauTau_tt = r.TH1F("mTauTau_tt"," ", 56, 20, 300)
mTauTau_zz = r.TH1F("mTauTau_zz"," ", 56, 20, 300)
total = r.TH1F("total"," ", 56, 20, 300)

ChainHistList = [(HChain, mTauTau_h), (ttChain, mTauTau_tt), (ZZChain, mTauTau_zz)]

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()

for iChain, iHist in ChainHistList:
    total= iChain.GetEntries()
    for i in range(0, total):
        iChain.GetEntry(i)
        tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping signal sample')
        if DrawSVMass:
            for iMass in range(iChain.svMass.size()):
                iHist.Fill(iChain.svMass.at(iMass))
        else:
            for iTauPair in range(iChain.pt1.size()):
                tau1.SetCoordinates(iChain.pt1.at(iTauPair), iChain.eta1.at(iTauPair), iChain.phi1.at(iTauPair), iChain.m1.at(iTauPair))
                tau2.SetCoordinates(iChain.pt2.at(iTauPair), iChain.eta2.at(iTauPair), iChain.phi2.at(iTauPair), iChain.m2.at(iTauPair))
                iHist.Fill((tau1+tau2).mass())
    print ''

integral = mTauTau_h.Integral()
signal = total.Integral()
ratio = integral/signal * 100
mTauTau_h.Scale(1/integral)
integral = mTauTau_zz.Integral()
mTauTau_zz.Scale(1/integral)
integral = mTauTau_tt.Integral()
mTauTau_tt.Scale(1/integral)

legendPosition = (0.58, 0.7, 0.88, 0.80)
l1 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l1.SetFillStyle(0)
l1.SetBorderSize(0)
text = r.TLatex()

mTauTau_zz.SetTitle("%s; mTauTau; Unit Normalized" % (Title))
mTauTau_h.SetTitle("%s; mTauTau; Unit Normalized" % (Title))
mTauTau_h.GetYaxis().SetTitleOffset(1.2)
mTauTau_zz.GetYaxis().SetTitleOffset(1.2)
c = r.TCanvas("c","Test", 800, 600)
r.gPad.SetTickx()
r.gPad.SetTicky()

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)

l1.AddEntry(mTauTau_h,"h(125) -> bb")
l1.AddEntry(mTauTau_zz,"ZZjets -> 2q2l")
l1.AddEntry(mTauTau_tt,"t#bar{t}")
mTauTau_zz.SetLineWidth(2)
mTauTau_h.SetLineWidth(2)
mTauTau_tt.SetLineWidth(2)
mTauTau_zz.SetLineStyle(2)

mTauTau_zz.SetLineColor(1)
if mTauTau_h.GetMaximum() > mTauTau_zz.GetMaximum():
    mTauTau_h.Draw()
    mTauTau_zz.Draw("same")
else:
    mTauTau_zz.Draw()
    mTauTau_h.Draw("same")
mTauTau_h.SetFillStyle(3001)
mTauTau_h.SetFillColor(4)
mTauTau_tt.SetFillStyle(3001)
mTauTau_tt.SetFillColor(2)
mTauTau_tt.SetLineColor(2)
mTauTau_tt.Draw("same")
l1.Draw("same")
text.SetTextFont(42)
text.SetTextSize(0.03)
text.DrawLatex(180, 0.045, "Signal Remaining: %s" %(round(ratio,1)) + "%")
ps.Close()