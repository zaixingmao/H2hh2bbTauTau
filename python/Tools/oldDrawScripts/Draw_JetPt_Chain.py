#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="JetPt"

Title = "Require "

signalEntries = enVars.signalEntries
ttEntries = enVars.ttEntries
ZZEntries = enVars.ZZEntries
signalLocation = enVars.signalLocation
ttLocation = enVars.ttLocation
ZZLocation = enVars.ZZLocation

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
tool.addFiles(HChain, signalLocation, signalEntries)
tool.addFiles(ttChain, ttLocation, ttEntries)
tool.addFiles(ZZChain, ZZLocation, ZZEntries)
sigPreSelection = tool.addHistFirstBinFromFiles(dirName=signalLocation)+0.
ttPreSelection = tool.addHistFirstBinFromFiles(dirName=ttLocation)+0.
ZZPreSelection = tool.addHistFirstBinFromFiles(dirName=ZZLocation)+0.
h_jetPt1_h = r.TH1F("h_jetPt1_h"," ", 57, 15, 300)
h_jetPt1_tt = r.TH1F("h_jetPt1_tt"," ", 57, 15, 300)
h_jetPt1_zz = r.TH1F("h_jetPt1_zz"," ", 57, 15, 300)
h_jetPt2_h = r.TH1F("h_jetPt2_h"," ", 57, 15, 300)
h_jetPt2_tt = r.TH1F("h_jetPt2_tt"," ", 57, 15, 300)
h_jetPt2_zz = r.TH1F("h_jetPt2_zz"," ", 57, 15, 300)
total = r.TH1F("total"," ", 57, 15, 300)

ChainHistList = [(HChain, signalLocation, signalEntries, h_jetPt1_h, h_jetPt2_h),
                 (ttChain, ttLocation, ttEntries, h_jetPt1_tt, h_jetPt2_tt),
                 (ZZChain, ZZLocation, ZZEntries, h_jetPt1_zz, h_jetPt2_zz)]

#for normalization
HistNameList = [h_jetPt1_h, h_jetPt1_tt, h_jetPt1_zz,
                h_jetPt2_h, h_jetPt2_tt, h_jetPt2_zz]
xsList = (15.9, 26197.5, 2502.)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()

for iChain, iLocation, iEntries, iHist1, iHist2 in ChainHistList:
    total = iEntries if iEntries else iChain.GetEntriesFast()
    key =  "found" if not iEntries else "has"
    print "[%s] %s %d events" %(iLocation, key, total)
    for i in range(0, total):
        iChain.GetEntry(i)
        tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample')
        jetsList = [(iChain.J1CSVbtag, J1.SetCoordinates(iChain.J1Pt, iChain.J1Eta,
                                                         iChain.J1Phi, iChain.J1Mass)),
                    (iChain.J2CSVbtag, J2.SetCoordinates(iChain.J2Pt, iChain.J2Eta,
                                                         iChain.J2Phi, iChain.J2Mass)),
                    (iChain.J3CSVbtag, J3.SetCoordinates(iChain.J3Pt, iChain.J3Eta,
                                                         iChain.J3Phi, iChain.J3Mass)),
                    (iChain.J4CSVbtag, J4.SetCoordinates(iChain.J4Pt, iChain.J4Eta,
                                                         iChain.J4Phi, iChain.J4Mass))]
        jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
        if jetsList[0][1].pt() < 20 or abs(jetsList[0][1].eta()) >= 2.4:
            continue
        if jetsList[1][1].pt() < 20 or abs(jetsList[1][1].eta()) >= 2.4:
            continue
        if jetsList[0][0] > CSVCut1 and jetsList[1][0] > CSVCut2:
            iHist1.Fill(iChain.J1Pt)
            iHist2.Fill(iChain.J2Pt)
    print ''
            
intList = tool.unitNormHists(HistNameList)
            
legendPosition = (0.58, 0.7, 0.88, 0.80)
legendHistos1 = [(h_jetPt1_h,"H -> hh -> #tau^{+}#tau^{-} b#bar{b}"),#(%.2f events/20 fb^{-1})" %(intList[0]*xsList[0]*20/sigPreSelection)),
                (h_jetPt1_tt,"t#bar{t} -> b#bar{b} ll"), #(%.1f events/20 fb^{-1})" %(intList[1]*xsList[1]*20/ttPreSelection)),
                (h_jetPt1_zz,"ZZ + jets -> 2q 2l")]#(%.1f events/20 fb^{-1})" %(intList[2]*xsList[2]*20/ZZPreSelection))]
legendHistos2 = [(h_jetPt2_h,"H -> hh -> #tau^{+}#tau^{-} b#bar{b}"),#(%.2f events/20 fb^{-1})" %(intList[0]*xsList[0]*20/sigPreSelection)),
                (h_jetPt2_tt,"t#bar{t} -> b#bar{b} ll"), #(%.1f events/20 fb^{-1})" %(intList[1]*xsList[1]*20/ttPreSelection)),
                (h_jetPt2_zz,"ZZ + jets -> 2q 2l")]#(%.1f events/20 fb^{-1})" %(intList[2]*xsList[2]*20/ZZPreSelection))]

h_jetPt1_h.SetTitle("%s; jet1 Pt; Unit Normalized" % (Title))
h_jetPt1_h.GetYaxis().SetTitleOffset(1.2)
h_jetPt2_zz.SetTitle("%s; jet2 Pt; Unit Normalized" % (Title))
h_jetPt2_zz.GetYaxis().SetTitleOffset(1.2)
c = r.TCanvas("c","Test", 1200, 500)
c.Divide(2,1)

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)
c.cd(1)
r.gPad.SetTickx()
r.gPad.SetTicky()
tool.setDrawHists(sigHist=h_jetPt1_h, ttHist=h_jetPt1_tt, ZZHist=h_jetPt1_zz)
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos1)
l1.Draw("same")
c.cd(2)
r.gPad.SetTickx()
r.gPad.SetTicky()
tool.setDrawHists(sigHist=h_jetPt2_h, ttHist=h_jetPt2_tt, ZZHist=h_jetPt2_zz)
l2 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos2)
l2.Draw("same")
ps.Close()

print "Plot saved at %s" %(psfile)
