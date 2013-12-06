#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os

psfile="JetCSV.eps"

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
tool.addFiles(ch=HChain, dirName="/hdfs/store/user/zmao/H2hh-SUB-TT")
tool.addFiles(ch=ttChain, dirName="/hdfs/store/user/zmao/tt-SUB-TT")
tool.addFiles(ch=ZZChain, dirName="/hdfs/store/user/zmao/ZZ2-SUB-TT")

jetCSV1_signal = r.TH1F("jetCSV1_signal"," ", 100, 0, 1)
jetCSV1_tt = r.TH1F("jetCSV1_tt"," ", 100, 0, 1)
jetCSV1_ZZ = r.TH1F("jetCSV1_ZZ"," ", 100, 0, 1)
total = r.TH1F("total"," ", 100, 0, 1)
jetCSV2_signal = r.TH1F("jetCSV2_signal"," ", 100, 0, 1)
jetCSV2_tt = r.TH1F("jetCSV2_tt"," ", 100, 0, 1)
jetCSV2_ZZ = r.TH1F("jetCSV2_ZZ"," ", 100, 0, 1)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()
print 'Getting nEntries in signal sample...'
Htotal= HChain.GetEntries()
for i in range(0, Htotal):
    HChain.GetEntry(i)
    tool.printProcessStatus(iCurrent=i, total=Htotal, processName = 'Looping signal sample')
    jetsList = [(HChain.J1CSVbtag, J1.SetCoordinates(HChain.J1Pt, HChain.J1Eta, HChain.J1Phi, HChain.J1Mass)),
                (HChain.J2CSVbtag, J2.SetCoordinates(HChain.J2Pt, HChain.J2Eta, HChain.J2Phi, HChain.J2Mass)),
                (HChain.J3CSVbtag, J3.SetCoordinates(HChain.J3Pt, HChain.J3Eta, HChain.J3Phi, HChain.J3Mass)),
                (HChain.J4CSVbtag, J4.SetCoordinates(HChain.J4Pt, HChain.J4Eta, HChain.J4Phi, HChain.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    total.Fill((jetsList[0][1]+jetsList[1][1]).mass())
    if jetsList[0][0] > CSVCut1 and jetsList[1][0] > CSVCut2:
        jetCSV1_signal.Fill(jetsList[0][0])
        jetCSV2_signal.Fill(jetsList[1][0])
print '\nGetting nEntries in tt sample...'
ttTotal = ttChain.GetEntries()
for i in range(0, ttTotal):
    ttChain.GetEntry(i)
    tool.printProcessStatus(iCurrent=i, total=ttTotal, processName = 'Looping tt sample')
    jetsList = [(ttChain.J1CSVbtag, J1.SetCoordinates(ttChain.J1Pt, ttChain.J1Eta, ttChain.J1Phi, ttChain.J1Mass)),
                (ttChain.J2CSVbtag, J2.SetCoordinates(ttChain.J2Pt, ttChain.J2Eta, ttChain.J2Phi, ttChain.J2Mass)),
                (ttChain.J3CSVbtag, J3.SetCoordinates(ttChain.J3Pt, ttChain.J3Eta, ttChain.J3Phi, ttChain.J3Mass)),
                (ttChain.J4CSVbtag, J4.SetCoordinates(ttChain.J4Pt, ttChain.J4Eta, ttChain.J4Phi, ttChain.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    if jetsList[0][0] > CSVCut1 and jetsList[1][0] > CSVCut2:
        jetCSV1_tt.Fill(jetsList[0][0])
        jetCSV2_tt.Fill(jetsList[1][0])

print  '\nGetting nEntries in ZZ sample...'
ZZTotal = ZZChain.GetEntries()
for i in range(0, ZZChain.GetEntries()):
    ZZChain.GetEntry(i)
    tool.printProcessStatus(iCurrent=i, total=ZZTotal, processName = 'Looping ZZ sample')
    jetsList = [(ZZChain.J1CSVbtag, J1.SetCoordinates(ZZChain.J1Pt, ZZChain.J1Eta, ZZChain.J1Phi, ZZChain.J1Mass)),
                (ZZChain.J2CSVbtag, J2.SetCoordinates(ZZChain.J2Pt, ZZChain.J2Eta, ZZChain.J2Phi, ZZChain.J2Mass)),
                (ZZChain.J3CSVbtag, J3.SetCoordinates(ZZChain.J3Pt, ZZChain.J3Eta, ZZChain.J3Phi, ZZChain.J3Mass)),
                (ZZChain.J4CSVbtag, J4.SetCoordinates(ZZChain.J4Pt, ZZChain.J4Eta, ZZChain.J4Phi, ZZChain.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    if jetsList[0][0] > CSVCut1 and jetsList[1][0] > CSVCut2:
        jetCSV1_ZZ.Fill(jetsList[0][0])
        jetCSV2_ZZ.Fill(jetsList[1][0])

print ''
integral = jetCSV1_signal.Integral()
signal = total.Integral()
ratio = integral/signal * 100
jetCSV1_signal.Scale(1/integral)
integral = jetCSV1_ZZ.Integral()
jetCSV1_ZZ.Scale(1/integral)
integral = jetCSV1_tt.Integral()
jetCSV1_tt.Scale(1/integral)

integral = jetCSV2_signal.Integral()
jetCSV2_signal.Scale(1/integral)
integral = jetCSV2_ZZ.Integral()
jetCSV2_ZZ.Scale(1/integral)
integral = jetCSV2_tt.Integral()
jetCSV2_tt.Scale(1/integral)


legendPosition = (0.58, 0.7, 0.88, 0.80)
l1 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l1.SetFillStyle(0)
l1.SetBorderSize(0)
l2 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l2.SetFillStyle(0)
l2.SetBorderSize(0)
text = r.TLatex()

text = r.TLatex()

jetCSV1_signal.SetTitle("%s; CVS1; Unit Normalized" % (Title))
jetCSV1_signal.GetYaxis().SetTitleOffset(1.3)
jetCSV2_tt.SetTitle("%s; CVS2; Unit Normalized" % (Title))
jetCSV2_tt.GetYaxis().SetTitleOffset(1.3)
c = r.TCanvas("c","Test", 1400, 600)
r.gPad.SetTickx()
r.gPad.SetTicky()

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)

l1.AddEntry(jetCSV1_signal,"H->hh")
l1.AddEntry(jetCSV1_ZZ,"ZZjets -> 2q2l")
l1.AddEntry(jetCSV1_tt,"t#bar{t}")
l2.AddEntry(jetCSV2_signal,"H->hh")
l2.AddEntry(jetCSV2_ZZ,"ZZjets -> 2q2l")
l2.AddEntry(jetCSV2_tt,"t#bar{t}")
jetCSV1_ZZ.SetLineWidth(2)
jetCSV1_signal.SetLineWidth(2)
jetCSV1_tt.SetLineWidth(2)
jetCSV1_ZZ.SetLineStyle(2)
jetCSV1_ZZ.SetLineColor(1)
jetCSV1_signal.SetFillStyle(3001)
jetCSV1_signal.SetFillColor(4)
jetCSV1_tt.SetFillStyle(3001)
jetCSV1_tt.SetFillColor(2)
jetCSV1_tt.SetLineColor(2)
jetCSV2_ZZ.SetLineWidth(2)
jetCSV2_signal.SetLineWidth(2)
jetCSV2_tt.SetLineWidth(2)
jetCSV2_ZZ.SetLineStyle(2)
jetCSV2_ZZ.SetLineColor(1)
jetCSV2_signal.SetFillStyle(3001)
jetCSV2_signal.SetFillColor(4)
jetCSV2_tt.SetFillStyle(3001)
jetCSV2_tt.SetFillColor(2)
jetCSV2_tt.SetLineColor(2)

c.Divide(2,1)
c.cd(1)
jetCSV1_signal.Draw()
jetCSV1_ZZ.Draw("same")
jetCSV1_tt.Draw("same")
l1.Draw("same")

c.cd(2)
jetCSV2_tt.Draw()
jetCSV2_signal.Draw("same")
jetCSV2_ZZ.Draw("same")
l2.Draw("same")
ps.Close()
