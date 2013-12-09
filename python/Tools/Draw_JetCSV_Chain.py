#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="JetCSV.eps"

Title = "Require "

signalEntries = enVars.signalEntries
ttEntries = enVars.ttEntries
ZZEntries = enVars.ZZEntries
signalLocation = enVars.signalLocation
ttLocation = enVars.ttLocation
ZZLocation = enVars.ZZLocation

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******
HChain = r.TChain("ttTreeFinal/eventTree")
ttChain = r.TChain("ttTreeFinal/eventTree")
ZZChain = r.TChain("ttTreeFinal/eventTree")
tool.addFiles(ch=HChain, dirName=signalLocation, knownEventNumber=signalEntries)
tool.addFiles(ch=ttChain, dirName=ttLocation, knownEventNumber=ttEntries)
tool.addFiles(ch=ZZChain, dirName=ZZLocation, knownEventNumber=ZZEntries)

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

ChainHistList = [(HChain, signalLocation, signalEntries, jetCSV1_signal, jetCSV2_signal),
                 (ttChain, ttLocation, ttEntries, jetCSV1_tt, jetCSV2_tt),
                 (ZZChain, ZZLocation, ZZEntries, jetCSV1_ZZ, jetCSV2_ZZ)]

#for normalization
HistNameList = [jetCSV1_signal, jetCSV2_signal, jetCSV1_tt, jetCSV2_tt, jetCSV1_ZZ, jetCSV2_ZZ]

for iChain, iLocation, iEntries, iHist1, iHist2 in ChainHistList:
    total = iEntries if iEntries else iChain.GetEntriesFast()
    key =  "found" if not iEntries else "has"
    print "[%s] %s %d events" %(iLocation, key, total)
    for i in range(0, total):
        iChain.GetEntry(i)
        tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping signal sample')
        jetsList = [(iChain.J1CSVbtag, J1.SetCoordinates(iChain.J1Pt, iChain.J1Eta, iChain.J1Phi, iChain.J1Mass)),
                    (iChain.J2CSVbtag, J2.SetCoordinates(iChain.J2Pt, iChain.J2Eta, iChain.J2Phi, iChain.J2Mass)),
                    (iChain.J3CSVbtag, J3.SetCoordinates(iChain.J3Pt, iChain.J3Eta, iChain.J3Phi, iChain.J3Mass)),
                    (iChain.J4CSVbtag, J4.SetCoordinates(iChain.J4Pt, iChain.J4Eta, iChain.J4Phi, iChain.J4Mass))]
        jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
        iHist1.Fill(jetsList[0][0])
        iHist2.Fill(jetsList[1][0])
    print ''


tool.unitNormHists(HistNameList)

legendPosition = (0.58, 0.7, 0.88, 0.80)
legendHist1 = [(jetCSV1_signal,"H->hh"), (jetCSV1_ZZ,"ZZjets -> 2q2l"), (jetCSV1_tt,"t#bar{t}")]
legendHist2 = [(jetCSV2_signal,"H->hh"), (jetCSV2_ZZ,"ZZjets -> 2q2l"), (jetCSV2_tt,"t#bar{t}")]

jetCSV1_signal.SetTitle("%s; CVS1; Unit Normalized" % (Title))
jetCSV2_tt.SetTitle("%s; CVS2; Unit Normalized" % (Title))
jetCSV1_signal.GetYaxis().SetTitleOffset(1.3)
jetCSV2_tt.GetYaxis().SetTitleOffset(1.3)

c = r.TCanvas("c","Test", 1400, 600)
r.gPad.SetTickx()
r.gPad.SetTicky()

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)

c.Divide(2,1)
c.cd(1)
tool.setDrawHists(sigHist=jetCSV1_signal, ttHist=jetCSV1_tt, ZZHist=jetCSV1_ZZ)
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHist1)
l1.Draw("same")
c.cd(2)
tool.setDrawHists(sigHist=jetCSV2_signal, ttHist=jetCSV2_tt, ZZHist=jetCSV2_ZZ)
l2 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHist2)
l2.Draw("same")
ps.Close()

print "Plot saved at %s" %(psfile)