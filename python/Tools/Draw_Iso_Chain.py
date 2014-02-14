#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="Iso1"

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
HChain = r.TChain("ttTreeIni/eventTree")
ttChain = r.TChain("ttTreeIni/eventTree")
ZZChain = r.TChain("ttTreeIni/eventTree")
tool.addFiles(HChain, signalLocation, signalEntries, 10)
tool.addFiles(ttChain, ttLocation, ttEntries, 1)
tool.addFiles(ZZChain, ZZLocation, ZZEntries, 1)
h_mjj_h = r.TH1F("h_mjj_h"," ", 28, 0.1, 1.5)
h_mjj_tt = r.TH1F("h_mjj_tt"," ", 28, 0.1, 1.5)
h_mjj_zz = r.TH1F("h_mjj_zz"," ", 28, 0.1, 1.5)
total = r.TH1F("total"," ", 28, 0.1, 1.5)

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
        for iIso in range(iChain.iso1.size()):
            iHist.Fill(iChain.iso1.at(iIso))
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
