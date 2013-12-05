#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter


r.gStyle.SetOptStat(0)

psfile="/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/Plots/Iso.eps"

#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/analysis.root")

a = r.TH1F("a"," ", 50, 0, 10)
b = r.TH1F("b"," ", 50, 0, 10)

tree = ifile.Get("ttTreeFinal/eventTree")

for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)
    for j in range(tree.iso1.size()):
        a.Fill(tree.iso1.at(j))
        if tree.CombinedIso1.at(j):
            b.Fill(tree.iso1.at(j))

c = r.TCanvas("c","Test", 800, 600)
ps = r.TPostScript(psfile,112)
r.gPad.SetTickx()
r.gPad.SetTicky()
legendPosition = (0.25, 0.75, 0.9, 0.85)
l1 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l1.SetFillStyle(0)
l1.SetBorderSize(0)
l1.AddEntry(a,"Pre-IsoSelection")
l1.AddEntry(b,"Post-byMediumCombinedIsolationDeltaBetaCorr3Hits Selection")

a.SetTitle("Leg1 Iso; byCombinedIsolationDeltaBetaCorrRaw3Hits; Events")
a.SetLineWidth(2)
b.SetLineWidth(2)
a.Draw()
b.SetLineColor(2)
b.SetLineStyle(2)
b.Draw("same")
l1.Draw("same")
ps.Close()