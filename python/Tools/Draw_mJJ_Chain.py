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
tool.addFiles(HChain, "/hdfs/store/user/zmao/H2hh-SUB-TT")
tool.addFiles(ttChain, "/hdfs/store/user/zmao/tt-SUB-TT")
tool.addFiles(ZZChain, "/hdfs/store/user/zmao/ZZ2-SUB-TT")

h_mjj_h = r.TH1F("h_mjj_h"," ", 56, 20, 300)
h_mjj_tt = r.TH1F("h_mjj_tt"," ", 56, 20, 300)
h_mjj_zz = r.TH1F("h_mjj_zz"," ", 56, 20, 300)
total = r.TH1F("total"," ", 56, 20, 300)

ChainHistList = [(HChain, h_mjj_h,
                 (ttChain, h_mjj_tt),
                 (ZZChain, h_mjj_zz)]

#for normalization
HistNameList = [h_mjj_h, h_mjj_tt, h_mjj_zz]

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()

for i in range(len(ChainHistList)):
    total= ChainHistList[i].GetEntries()
    for i in range(0, total):
        ChainHistList[i].GetEntry(i)
        tool.printProcessStatus(iCurrent=i, total=Htotal, processName = 'Looping signal sample')
        jetsList = [(ChainHistList[i].J1CSVbtag, J1.SetCoordinates(ChainHistList[i].J1Pt, ChainHistList[i].J1Eta, ChainHistList[i].J1Phi, ChainHistList[i].J1Mass)),
                    (ChainHistList[i].J2CSVbtag, J2.SetCoordinates(ChainHistList[i].J2Pt, ChainHistList[i].J2Eta, ChainHistList[i].J2Phi, ChainHistList[i].J2Mass)),
                    (ChainHistList[i].J3CSVbtag, J3.SetCoordinates(ChainHistList[i].J3Pt, ChainHistList[i].J3Eta, ChainHistList[i].J3Phi, ChainHistList[i].J3Mass)),
                    (ChainHistList[i].J4CSVbtag, J4.SetCoordinates(ChainHistList[i].J4Pt, ChainHistList[i].J4Eta, ChainHistList[i].J4Phi, ChainHistList[i].J4Mass))
                    ]
        jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
        total.Fill((jetsList[0][1]+jetsList[1][1]).mass())
        if jetsList[0][0] > CSVCut1 and jetsList[1][0] > CSVCut2:
            ChainHistList[i][0].Fill((jetsList[0][1]+jetsList[1][1]).mass())
    print ''

tool.unitNormHists(HistNameList)

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

l1.AddEntry(ChainHistList[i][0],"H->hh")
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
