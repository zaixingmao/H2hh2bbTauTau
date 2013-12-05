#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os

psfile="mJJprerequire.eps"

Title = "Require "


CSVCut1 = -99999
CSVCut2 = -99999

if CSVCut1 == 0.679 and CSVCut2 < 0:
    Title = Title + "1 medium b tag"
    psfile = psfile + "_1_b_tag.eps"
if CSVCut1 == 0.679 and CSVCut2 == 0.679:
    Title = Title + "2 medium b tags"
    psfile = psfile + "_2_b_tag.eps"
if CSVCut1 < 0 and CSVCut2 < 0:
    Title = Title + "no b tags"
    psfile = psfile + "_no_b_tag.eps"

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******
HChain = r.TChain("ttTreeFinal/eventTree")
ttChain = r.TChain("ttTreeFinal/eventTree")
ZZChain = r.TChain("ttTreeFinal/eventTree")
tool.addFiles(HChain, " ")
tool.addFiles(ttChain, " ")
tool.addFiles(ZZchain, "/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC")

h_mjj_h = r.TH1F("h_mjj_h"," ", 56, 20, 300)
h_mjj_tt = r.TH1F("h_mjj_tt"," ", 56, 20, 300)
h_mjj_zz = r.TH1F("h_mjj_zz"," ", 56, 20, 300)
total = r.TH1F("total"," ", 56, 20, 300)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()

for i in range(0, HChain.GetEntries()):
    HChain.GetEntry(i)

    jetsList = [(HChain.J1CSVbtag, J1.SetCoordinates(HChain.J1Pt, HChain.J1Eta, HChain.J1Phi, HChain.J1Mass)),
                (HChain.J2CSVbtag, J2.SetCoordinates(HChain.J2Pt, HChain.J2Eta, HChain.J2Phi, HChain.J2Mass)),
                (HChain.J3CSVbtag, J3.SetCoordinates(HChain.J3Pt, HChain.J3Eta, HChain.J3Phi, HChain.J3Mass)),
                (HChain.J4CSVbtag, J4.SetCoordinates(HChain.J4Pt, HChain.J4Eta, HChain.J4Phi, HChain.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    total.Fill((jetsList[0][1]+jetsList[1][1]).mass())
        h_mjj_h.Fill((jetsList[0][1]+jetsList[1][1]).mass())

for i in range(0, ttChain.GetEntries()):
    ttChain.GetEntry(i)

    jetsList = [(ttChain.J1CSVbtag, J1.SetCoordinates(ttChain.J1Pt, ttChain.J1Eta, ttChain.J1Phi, ttChain.J1Mass)),
                (ttChain.J2CSVbtag, J2.SetCoordinates(ttChain.J2Pt, ttChain.J2Eta, ttChain.J2Phi, ttChain.J2Mass)),
                (ttChain.J3CSVbtag, J3.SetCoordinates(ttChain.J3Pt, ttChain.J3Eta, ttChain.J3Phi, ttChain.J3Mass)),
                (ttChain.J4CSVbtag, J4.SetCoordinates(ttChain.J4Pt, ttChain.J4Eta, ttChain.J4Phi, ttChain.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    if jetsList[0][0] > CSVCut1 and jetsList[1][0] > CSVCut2:
        h_mjj_tt.Fill((jetsList[0][1]+jetsList[1][1]).mass())

for i in range(0, ZZchain.GetEntries()):
    ZZchain.GetEntry(i)

    jetsList = [(ZZchain.J1CSVbtag, J1.SetCoordinates(ZZchain.J1Pt, ZZchain.J1Eta, ZZchain.J1Phi, ZZchain.J1Mass)),
                (ZZchain.J2CSVbtag, J2.SetCoordinates(ZZchain.J2Pt, ZZchain.J2Eta, ZZchain.J2Phi, ZZchain.J2Mass)),
                (ZZchain.J3CSVbtag, J3.SetCoordinates(ZZchain.J3Pt, ZZchain.J3Eta, ZZchain.J3Phi, ZZchain.J3Mass)),
                (ZZchain.J4CSVbtag, J4.SetCoordinates(ZZchain.J4Pt, ZZchain.J4Eta, ZZchain.J4Phi, ZZchain.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    if jetsList[0][0] > CSVCut1 and jetsList[1][0] > CSVCut2:
        h_mjj_zz.Fill((jetsList[0][1]+jetsList[1][1]).mass())

integral = h_mjj_h.Integral()
signal = total.Integral()
ratio = integral/signal * 100
h_mjj_h.Scale(1/integral)
integral = h_mjj_zz.Integral()
h_mjj_zz.Scale(1/integral)
integral = h_mjj_tt.Integral()
h_mjj_tt.Scale(1/integral)

legendPosition = (0.58, 0.7, 0.88, 0.80)
l1 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l1.SetFillStyle(0)
l1.SetBorderSize(0)
text = r.TLatex()

h_mjj_zz.SetTitle("%s; mJJCSVSort; Unit Normalized" % (Title))
h_mjj_zz.GetYaxis().SetTitleOffset(1.2)
c = r.TCanvas("c","Test", 800, 600)
r.gPad.SetTickx()
r.gPad.SetTicky()

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)

l1.AddEntry(h_mjj_h,"H->hh")
l1.AddEntry(h_mjj_zz,"ZZjets -> 2q2l")
l1.AddEntry(h_mjj_tt,"t#bar{t}")
h_mjj_zz.SetLineWidth(2)
h_mjj_h.SetLineWidth(2)
h_mjj_tt.SetLineWidth(2)
h_mjj_zz.SetLineStyle(2)

h_mjj_zz.SetLineColor(1)
h_mjj_zz.Draw()
h_mjj_h.SetFillStyle(3001)
h_mjj_h.SetFillColor(4)
h_mjj_tt.SetFillStyle(3001)
h_mjj_tt.SetFillColor(2)
h_mjj_tt.SetLineColor(2)
h_mjj_tt.Draw("same")
l1.Draw("same")
h_mjj_h.Draw("same")
text.SetTextFont(42)
text.SetTextSize(0.03)
text.DrawLatex(180, 0.045, "Signal Remaining: %s" %(round(ratio,1)) + "%")
ps.Close()
