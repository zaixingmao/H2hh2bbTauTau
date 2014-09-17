#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter

psfile="JetCSVPt.eps"

Title = "jetPt"

CSVCut1 = -9999999. #0.679
CSVCut2 = -9999999. #0.679

signal = 1546.0
zz = 1206.0
tt= 3333.0

r.gStyle.SetOptStat(0)
#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/TempCode/analysis_signal.root")
ifile2 = r.TFile("/Users/zmao/M-Data/School/TempCode/analysis_tt.root")
ifile3 = r.TFile("/Users/zmao/M-Data/School/TempCode/analysis_zz.root")
tree = ifile.Get("ttTreeFinal/eventTree")
tree2 = ifile2.Get("ttTreeFinal/eventTree")
tree3 = ifile3.Get("ttTreeFinal/eventTree")

h_jetPt1_h = r.TH1F("h_jetPt1_h"," ", 48, 10, 250)
h_jetPt1_tt = r.TH1F("h_jetPt1_tt"," ", 48, 10, 250)
h_jetPt1_zz = r.TH1F("h_jetPt1_zz"," ", 48, 10, 250)
h_jetPt2_h = r.TH1F("h_jetPt2_h"," ", 48, 10, 250)
h_jetPt2_tt = r.TH1F("h_jetPt2_tt"," ", 48, 10, 250)
h_jetPt2_zz = r.TH1F("h_jetPt2_zz"," ", 48, 10, 250)
h_CSVjetPt1_h = r.TH1F("h_CSVjetPt1_h"," ", 48, 10, 250)
h_CSVjetPt1_tt = r.TH1F("h_CSVjetPt1_tt"," ", 48, 10, 250)
h_CSVjetPt1_zz = r.TH1F("h_CSVjetPt1_zz"," ", 48, 10, 250)
h_CSVjetPt2_h = r.TH1F("h_CSVjetPt2_h"," ", 48, 10, 250)
h_CSVjetPt2_tt = r.TH1F("h_CSVjetPt2_tt"," ", 48, 10, 250)
h_CSVjetPt2_zz = r.TH1F("h_CSVjetPt2_zz"," ", 48, 10, 250)
h_CSVjetPt1_h_btag = r.TH1F("h_CSVjetPt1_h_btag"," ", 48, 10, 250)
h_CSVjetPt1_tt_btag = r.TH1F("h_CSVjetPt1_tt_btag"," ", 48, 10, 250)
h_CSVjetPt1_zz_btag = r.TH1F("h_CSVjetPt1_zz_btag"," ", 48, 10, 250)
h_CSVjetPt2_h_btag = r.TH1F("h_CSVjetPt2_h_btag"," ", 48, 10, 250)
h_CSVjetPt2_tt_btag = r.TH1F("h_CSVjetPt2_tt_btag"," ", 48, 10, 250)
h_CSVjetPt2_zz_btag = r.TH1F("h_CSVjetPt2_zz_btag"," ", 48, 10, 250)

tree.Draw("J1Pt >> h_jetPt1_h")
tree.Draw("J2Pt >> h_jetPt2_h")
tree2.Draw("J1Pt >> h_jetPt1_tt")
tree2.Draw("J2Pt >> h_jetPt2_tt")
tree3.Draw("J1Pt >> h_jetPt1_zz")
tree3.Draw("J2Pt >> h_jetPt2_zz")

for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)
    jetsList = [(tree.J1CSVbtag, tree.J1Pt),
                (tree.J2CSVbtag, tree.J2Pt),
                (tree.J3CSVbtag, tree.J3Pt),
                (tree.J4CSVbtag, tree.J4Pt)
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    h_CSVjetPt1_h.Fill(jetsList[0][1])
    h_CSVjetPt2_h.Fill(jetsList[1][1])
    if jetsList[0][0] > 0.679:
        h_CSVjetPt1_h_btag.Fill(jetsList[0][1])
    if jetsList[1][0] > 0.679:
        h_CSVjetPt2_h_btag.Fill(jetsList[1][1])

for i in range(0, tree2.GetEntries()):
    tree2.GetEntry(i)
    jetsList = [(tree2.J1CSVbtag, tree2.J1Pt),
                (tree2.J2CSVbtag, tree2.J2Pt),
                (tree2.J3CSVbtag, tree2.J3Pt),
                (tree2.J4CSVbtag, tree2.J4Pt)
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    h_CSVjetPt1_tt.Fill(jetsList[0][1])
    h_CSVjetPt2_tt.Fill(jetsList[1][1])
    if jetsList[0][0] > 0.679:
        h_CSVjetPt1_tt_btag.Fill(jetsList[0][1])
    if jetsList[1][0] > 0.679:
        h_CSVjetPt2_tt_btag.Fill(jetsList[1][1])

for i in range(0, tree3.GetEntries()):
    tree3.GetEntry(i)
    jetsList = [(tree3.J1CSVbtag, tree3.J1Pt),
                (tree3.J2CSVbtag, tree3.J2Pt),
                (tree3.J3CSVbtag, tree3.J3Pt),
                (tree3.J4CSVbtag, tree3.J4Pt)
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    h_CSVjetPt1_zz.Fill(jetsList[0][1])
    h_CSVjetPt2_zz.Fill(jetsList[1][1])
    if jetsList[0][0] > 0.679:
        h_CSVjetPt1_zz_btag.Fill(jetsList[0][1])
    if jetsList[1][0] > 0.679:
        h_CSVjetPt2_zz_btag.Fill(jetsList[1][1])


integral = h_jetPt1_h.Integral()
h_jetPt1_h.Scale(1/integral)
integral = h_jetPt1_zz.Integral()
h_jetPt1_zz.Scale(1/integral)
integral = h_jetPt1_tt.Integral()
h_jetPt1_tt.Scale(1/integral)

integral = h_jetPt2_h.Integral()
h_jetPt2_h.Scale(1/integral)
integral = h_jetPt2_zz.Integral()
h_jetPt2_zz.Scale(1/integral)
integral = h_jetPt2_tt.Integral()
h_jetPt2_tt.Scale(1/integral)

integral = h_CSVjetPt1_h.Integral()
h_CSVjetPt1_h.Scale(1/integral)
integral = h_CSVjetPt1_zz.Integral()
h_CSVjetPt1_zz.Scale(1/integral)
integral = h_CSVjetPt1_tt.Integral()
h_CSVjetPt1_tt.Scale(1/integral)

integral = h_CSVjetPt2_h.Integral()
h_CSVjetPt2_h.Scale(1/integral)
integral = h_CSVjetPt2_zz.Integral()
h_CSVjetPt2_zz.Scale(1/integral)
integral = h_CSVjetPt2_tt.Integral()
h_CSVjetPt2_tt.Scale(1/integral)

integral = h_CSVjetPt1_h_btag.Integral()
h_CSVjetPt1_h_btag.Scale(1/integral)
integral = h_CSVjetPt1_zz_btag.Integral()
h_CSVjetPt1_zz_btag.Scale(1/integral)
integral = h_CSVjetPt1_tt_btag.Integral()
h_CSVjetPt1_tt_btag.Scale(1/integral)

integral = h_CSVjetPt2_h_btag.Integral()
h_CSVjetPt2_h_btag.Scale(1/integral)
integral = h_CSVjetPt2_zz_btag.Integral()
h_CSVjetPt2_zz_btag.Scale(1/integral)
integral = h_CSVjetPt2_tt_btag.Integral()
h_CSVjetPt2_tt_btag.Scale(1/integral)


legendPosition = (0.58, 0.7, 0.88, 0.80)
l1 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l1.SetFillStyle(0)
l1.SetBorderSize(0)
l2 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l2.SetFillStyle(0)
l2.SetBorderSize(0)
l3 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l3.SetFillStyle(0)
l3.SetBorderSize(0)
l4 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l4.SetFillStyle(0)
l4.SetBorderSize(0)
l5 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l5.SetFillStyle(0)
l5.SetBorderSize(0)
l6 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l6.SetFillStyle(0)
l6.SetBorderSize(0)


h_jetPt1_zz.SetTitle("%s; Jet1 Pt; Unit Normalized" % (Title))
h_jetPt2_zz.SetTitle("%s; Jet2 Pt; Unit Normalized" % (Title))
h_CSVjetPt1_zz.SetTitle("%s;CSV Sorted Jet1 Pt; Unit Normalized" % (Title))
h_CSVjetPt2_h.SetTitle("%s;CSV Sorted Jet2 Pt; Unit Normalized" % (Title))
h_CSVjetPt1_zz_btag.SetTitle("%s Medium bTag;CSV Sorted Jet1 Pt (CSV > 0.679); Unit Normalized" % (Title))
h_CSVjetPt2_zz_btag.SetTitle("%s Medium bTag;CSV Sorted Jet2 Pt (CSV > 0.679); Unit Normalized" % (Title))
h_jetPt1_zz.GetYaxis().SetTitleOffset(1.5)
h_jetPt2_zz.GetYaxis().SetTitleOffset(1.5)
h_CSVjetPt1_zz.GetYaxis().SetTitleOffset(1.5)
h_CSVjetPt2_h.GetYaxis().SetTitleOffset(1.5)
h_CSVjetPt1_zz_btag.GetYaxis().SetTitleOffset(1.5)
h_CSVjetPt2_zz_btag.GetYaxis().SetTitleOffset(1.5)

c = r.TCanvas("c","Test", 800, 1200)
c.Divide(2,3)
ps = r.TPostScript(psfile,113)
c.cd(1) 
r.gPad.SetTickx()
r.gPad.SetTicky()
l1.AddEntry(h_jetPt1_h,"h(125) -> bb")
l1.AddEntry(h_jetPt1_zz,"ZZjets -> 2q2l")
l1.AddEntry(h_jetPt1_tt,"t#bar{t}")
h_jetPt1_zz.SetLineWidth(2)
h_jetPt1_h.SetLineWidth(2)
h_jetPt1_tt.SetLineWidth(2)
h_jetPt1_zz.SetLineStyle(2)

h_jetPt1_zz.SetLineColor(1)
h_jetPt1_zz.Draw()
h_jetPt1_h.SetFillStyle(3001)
h_jetPt1_h.SetFillColor(4)
h_jetPt1_tt.SetFillStyle(3001)
h_jetPt1_tt.SetFillColor(2)
h_jetPt1_tt.SetLineColor(2)
h_jetPt1_h.Draw("same")
h_jetPt1_tt.Draw("same")
l1.Draw("same")

c.cd(2)
r.gPad.SetTickx()
r.gPad.SetTicky()
l2.AddEntry(h_jetPt2_h,"h(125) -> bb")
l2.AddEntry(h_jetPt2_zz,"ZZjets -> 2q2l")
l2.AddEntry(h_jetPt2_tt,"t#bar{t}")
h_jetPt2_zz.SetLineWidth(2)
h_jetPt2_h.SetLineWidth(2)
h_jetPt2_tt.SetLineWidth(2)
h_jetPt2_zz.SetLineStyle(2)

h_jetPt2_zz.SetLineColor(1)
h_jetPt2_zz.Draw()
h_jetPt2_h.SetFillStyle(3001)
h_jetPt2_h.SetFillColor(4)
h_jetPt2_tt.SetFillStyle(3001)
h_jetPt2_tt.SetFillColor(2)
h_jetPt2_tt.SetLineColor(2)
h_jetPt2_h.Draw("same")
h_jetPt2_tt.Draw("same")
l2.Draw("same")

c.cd(3) 
r.gPad.SetTickx()
r.gPad.SetTicky()
l3.AddEntry(h_CSVjetPt1_h,"h(125) -> bb")
l3.AddEntry(h_CSVjetPt1_zz,"ZZjets -> 2q2l")
l3.AddEntry(h_CSVjetPt1_tt,"t#bar{t}")
h_CSVjetPt1_zz.SetLineWidth(2)
h_CSVjetPt1_h.SetLineWidth(2)
h_CSVjetPt1_tt.SetLineWidth(2)
h_CSVjetPt1_zz.SetLineStyle(2)

h_CSVjetPt1_zz.SetLineColor(1)
h_CSVjetPt1_zz.Draw()
h_CSVjetPt1_h.SetFillStyle(3001)
h_CSVjetPt1_h.SetFillColor(4)
h_CSVjetPt1_tt.SetFillStyle(3001)
h_CSVjetPt1_tt.SetFillColor(2)
h_CSVjetPt1_tt.SetLineColor(2)
h_CSVjetPt1_h.Draw("same")
h_CSVjetPt1_tt.Draw("same")
l3.Draw("same")

c.cd(4)
r.gPad.SetTickx()
r.gPad.SetTicky()
l4.AddEntry(h_CSVjetPt2_h,"h(125) -> bb")
l4.AddEntry(h_CSVjetPt2_zz,"ZZjets -> 2q2l")
l4.AddEntry(h_CSVjetPt2_tt,"t#bar{t}")
h_CSVjetPt2_zz.SetLineWidth(2)
h_CSVjetPt2_h.SetLineWidth(2)
h_CSVjetPt2_tt.SetLineWidth(2)
h_CSVjetPt2_zz.SetLineStyle(2)

h_CSVjetPt2_h.SetFillStyle(3001)
h_CSVjetPt2_h.SetFillColor(4)
h_CSVjetPt2_h.Draw()
h_CSVjetPt2_zz.SetLineColor(1)
h_CSVjetPt2_zz.Draw("same")
h_CSVjetPt2_tt.SetFillStyle(3001)
h_CSVjetPt2_tt.SetFillColor(2)
h_CSVjetPt2_tt.SetLineColor(2)
h_CSVjetPt2_tt.Draw("same")
l4.Draw("same")

c.cd(5) 
r.gPad.SetTickx()
r.gPad.SetTicky()
l5.AddEntry(h_CSVjetPt1_h_btag,"h(125) -> bb")
l5.AddEntry(h_CSVjetPt1_zz_btag,"ZZjets -> 2q2l")
l5.AddEntry(h_CSVjetPt1_tt_btag,"t#bar{t}")
h_CSVjetPt1_zz_btag.SetLineWidth(2)
h_CSVjetPt1_h_btag.SetLineWidth(2)
h_CSVjetPt1_tt_btag.SetLineWidth(2)
h_CSVjetPt1_zz_btag.SetLineStyle(2)

h_CSVjetPt1_zz_btag.SetLineColor(1)
h_CSVjetPt1_zz_btag.Draw()
h_CSVjetPt1_h_btag.SetFillStyle(3001)
h_CSVjetPt1_h_btag.SetFillColor(4)
h_CSVjetPt1_tt_btag.SetFillStyle(3001)
h_CSVjetPt1_tt_btag.SetFillColor(2)
h_CSVjetPt1_tt_btag.SetLineColor(2)
h_CSVjetPt1_h_btag.Draw("same")
h_CSVjetPt1_tt_btag.Draw("same")
l5.Draw("same")

c.cd(6)
r.gPad.SetTickx()
r.gPad.SetTicky()
l6.AddEntry(h_CSVjetPt2_h_btag,"h(125) -> bb")
l6.AddEntry(h_CSVjetPt2_zz_btag,"ZZjets -> 2q2l")
l6.AddEntry(h_CSVjetPt2_tt_btag,"t#bar{t}")
h_CSVjetPt2_zz_btag.SetLineWidth(2)
h_CSVjetPt2_h_btag.SetLineWidth(2)
h_CSVjetPt2_tt_btag.SetLineWidth(2)
h_CSVjetPt2_zz_btag.SetLineStyle(2)

h_CSVjetPt2_zz_btag.SetLineColor(1)
h_CSVjetPt2_zz_btag.Draw("same")
h_CSVjetPt2_h_btag.SetFillStyle(3001)
h_CSVjetPt2_h_btag.SetFillColor(4)
h_CSVjetPt2_h_btag.Draw("same")
h_CSVjetPt2_tt_btag.SetFillStyle(3001)
h_CSVjetPt2_tt_btag.SetFillColor(2)
h_CSVjetPt2_tt_btag.SetLineColor(2)
h_CSVjetPt2_tt_btag.Draw("same")
l6.Draw("same")


ps.Close()