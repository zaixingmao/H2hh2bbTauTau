#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter

psfile="mTauTau_withRequirements.eps"

#Title = "No Required b Tags, EleMuLooseVeto on Leg1"
Title = " "

r.gStyle.SetOptStat(0)
#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/analysis_signal.root")
ifile2 = r.TFile("/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/analysis_tt.root")
ifile3 = r.TFile("/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/analysis_zz.root")
tree = ifile.Get("ttTreeFinal/eventTree")
tree2 = ifile2.Get("ttTreeFinal/eventTree")
tree3 = ifile3.Get("ttTreeFinal/eventTree")

mTauTau_h = r.TH1F("mTauTau_h"," ", 56, 20, 300)
mTauTau_tt = r.TH1F("mTauTau_tt"," ", 56, 20, 300)
mTauTau_zz = r.TH1F("mTauTau_zz"," ", 56, 20, 300)
total = r.TH1F("total"," ", 56, 20, 300)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()

for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)
    for iTauPair in range(tree.pt1.size()):
        tau1.SetCoordinates(tree.pt1.at(iTauPair), tree.eta1.at(iTauPair), tree.phi1.at(iTauPair), tree.m1.at(iTauPair))
        tau2.SetCoordinates(tree.pt2.at(iTauPair), tree.eta2.at(iTauPair), tree.phi2.at(iTauPair), tree.m2.at(iTauPair))
        total.Fill((tau1+tau2).mass())
        mTauTau_h.Fill((tau1+tau2).mass())

for i in range(0, tree2.GetEntries()):
    tree2.GetEntry(i)
    for iTauPair in range(tree2.pt1.size()):
        tau1.SetCoordinates(tree2.pt1.at(iTauPair), tree2.eta1.at(iTauPair), tree2.phi1.at(iTauPair), tree2.m1.at(iTauPair))
        tau2.SetCoordinates(tree2.pt2.at(iTauPair), tree2.eta2.at(iTauPair), tree2.phi2.at(iTauPair), tree2.m2.at(iTauPair))
        mTauTau_tt.Fill((tau1+tau2).mass())

for i in range(0, tree3.GetEntries()):
    tree3.GetEntry(i)
    for iTauPair in range(tree3.pt1.size()):
        tau1.SetCoordinates(tree3.pt1.at(iTauPair), tree3.eta1.at(iTauPair), tree3.phi1.at(iTauPair), tree3.m1.at(iTauPair))
        tau2.SetCoordinates(tree3.pt2.at(iTauPair), tree3.eta2.at(iTauPair), tree3.phi2.at(iTauPair), tree3.m2.at(iTauPair))
        mTauTau_zz.Fill((tau1+tau2).mass())

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
