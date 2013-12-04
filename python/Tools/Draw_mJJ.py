#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter

psfile="mJJprerequire"

#Title = "No Required b Tags, EleMuLooseVeto on Leg1"
Title = "Require "

applyEleMuLooseVeto1 = 0

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
if applyEleMuLooseVeto1:
    psfile = psfile[0:psfile.find('.')] + "_emLooseVeto.eps"
    Title = Title + " emLooseVeto"

r.gStyle.SetOptStat(0)
#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/analysis_signal.root")
ifile2 = r.TFile("/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/analysis_tt.root")
ifile3 = r.TFile("/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/analysis_zz.root")
tree = ifile.Get("ttTreeFinal/eventTree")
tree2 = ifile2.Get("ttTreeFinal/eventTree")
tree3 = ifile3.Get("ttTreeFinal/eventTree")

h_mjj_h = r.TH1F("h_mjj_h"," ", 56, 20, 300)
h_mjj_tt = r.TH1F("h_mjj_tt"," ", 56, 20, 300)
h_mjj_zz = r.TH1F("h_mjj_zz"," ", 56, 20, 300)
total = r.TH1F("total"," ", 56, 20, 300)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()

for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)

    jetsList = [(tree.J1CSVbtag, J1.SetCoordinates(tree.J1Pt, tree.J1Eta, tree.J1Phi, tree.J1Mass)),
                (tree.J2CSVbtag, J2.SetCoordinates(tree.J2Pt, tree.J2Eta, tree.J2Phi, tree.J2Mass)),
                (tree.J3CSVbtag, J3.SetCoordinates(tree.J3Pt, tree.J3Eta, tree.J3Phi, tree.J3Mass)),
                (tree.J4CSVbtag, J4.SetCoordinates(tree.J4Pt, tree.J4Eta, tree.J4Phi, tree.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    total.Fill((jetsList[0][1]+jetsList[1][1]).mass())
    if jetsList[0][0] > CSVCut1 and jetsList[1][0] > CSVCut2:
        if applyEleMuLooseVeto1:
            if tree.tauElectronLMVAPass1 == 0 or tree.againstMuonLoose1 == 0:
                continue
        h_mjj_h.Fill((jetsList[0][1]+jetsList[1][1]).mass())

for i in range(0, tree2.GetEntries()):
    tree2.GetEntry(i)

    jetsList = [(tree2.J1CSVbtag, J1.SetCoordinates(tree2.J1Pt, tree2.J1Eta, tree2.J1Phi, tree2.J1Mass)),
                (tree2.J2CSVbtag, J2.SetCoordinates(tree2.J2Pt, tree2.J2Eta, tree2.J2Phi, tree2.J2Mass)),
                (tree2.J3CSVbtag, J3.SetCoordinates(tree2.J3Pt, tree2.J3Eta, tree2.J3Phi, tree2.J3Mass)),
                (tree2.J4CSVbtag, J4.SetCoordinates(tree2.J4Pt, tree2.J4Eta, tree2.J4Phi, tree2.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    if jetsList[0][0] > CSVCut1 and jetsList[1][0] > CSVCut2:
        if applyEleMuLooseVeto1:
            if tree2.tauElectronLMVAPass1 == 0 or tree2.againstMuonLoose1 == 0:
                continue
        h_mjj_tt.Fill((jetsList[0][1]+jetsList[1][1]).mass())

for i in range(0, tree3.GetEntries()):
    tree3.GetEntry(i)

    jetsList = [(tree3.J1CSVbtag, J1.SetCoordinates(tree3.J1Pt, tree3.J1Eta, tree3.J1Phi, tree3.J1Mass)),
                (tree3.J2CSVbtag, J2.SetCoordinates(tree3.J2Pt, tree3.J2Eta, tree3.J2Phi, tree3.J2Mass)),
                (tree3.J3CSVbtag, J3.SetCoordinates(tree3.J3Pt, tree3.J3Eta, tree3.J3Phi, tree3.J3Mass)),
                (tree3.J4CSVbtag, J4.SetCoordinates(tree3.J4Pt, tree3.J4Eta, tree3.J4Phi, tree3.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    if jetsList[0][0] > CSVCut1 and jetsList[1][0] > CSVCut2:
        if applyEleMuLooseVeto1:
            if tree3.tauElectronLMVAPass1 == 0 or tree3.againstMuonLoose1 == 0:
                continue
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

ps = r.TPostScript(psfile,112)

l1.AddEntry(h_mjj_h,"h(125) -> bb")
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
