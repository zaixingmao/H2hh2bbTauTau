#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="mJJprerequire"

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
h_mjj_h = r.TH1F("h_mjj_h"," ", 56, 20, 300)
h_mjj_tt = r.TH1F("h_mjj_tt"," ", 56, 20, 300)
h_mjj_zz = r.TH1F("h_mjj_zz"," ", 56, 20, 300)
total = r.TH1F("total"," ", 56, 20, 300)

ChainHistList = [(HChain, signalLocation, signalEntries, h_mjj_h),
                 (ttChain, ttLocation, ttEntries, h_mjj_tt),
                 (ZZChain, ZZLocation, ZZEntries, h_mjj_zz)]

#for normalization
HistNameList = [h_mjj_h, h_mjj_tt, h_mjj_zz]
xsList = (15.9, 26197.5, 2502.)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()

for iChain, iLocation, iEntries, iHist in ChainHistList:
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
            iHist.Fill((jetsList[0][1]+jetsList[1][1]).mass())
    print ''
            
intList = tool.unitNormHists(HistNameList)
            
legendPosition = (0.58, 0.7, 0.88, 0.80)
legendHistos = [(h_mjj_h,"H -> hh -> #tau^{+}#tau^{-} b#bar{b}"),#(%.2f events/20 fb^{-1})" %(intList[0]*xsList[0]*20/sigPreSelection)),
                (h_mjj_tt,"t#bar{t} -> b#bar{b} ll"), #(%.1f events/20 fb^{-1})" %(intList[1]*xsList[1]*20/ttPreSelection)),
                (h_mjj_zz,"ZZ + jets -> 2q 2l")]#(%.1f events/20 fb^{-1})" %(intList[2]*xsList[2]*20/ZZPreSelection))]

h_mjj_zz.SetTitle("%s; mJJCSVSort; Unit Normalized" % (Title))
h_mjj_zz.GetYaxis().SetTitleOffset(1.2)
c = r.TCanvas("c","Test", 800, 600)
r.gPad.SetTickx()
r.gPad.SetTicky()

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)

tool.setDrawHists(sigHist=h_mjj_h, ttHist=h_mjj_tt, ZZHist=h_mjj_zz)
l = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos)
l.Draw("same")
ps.Close()

print "Plot saved at %s" %(psfile)
