#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="tauPt"

#Title = "No Required b Tags, EleMuLooseVeto on Leg1"
title = "tauPt"
xsNorm = False
JetPtEtaCut = True
CSVCut1 = -9999999#0.679
CSVCut2 = -9999999#0.244
diJetMassCut = (-5,9999)#(100,140)
diTauMassCut = (-5,9999)#(100,130)

applyMETCut = 0 
psfile = psfile + "_diJet_%d_%d" %(diJetMassCut[0], diJetMassCut[1])
psfile = psfile + "_diTau_%d_%d" %(diTauMassCut[0], diTauMassCut[1])
title = title + "_diJet_%d_%d" %(diJetMassCut[0], diJetMassCut[1])
title = title + "_diTau_%d_%d" %(diTauMassCut[0], diTauMassCut[1])

if CSVCut1 == 0.679 and CSVCut2 == 0.244:
    title = title + "(1 medium, 1 loose b tag)"
    psfile = psfile + "_2_b_tag"
else:
    psfile = psfile + "_no_b_tag"
psfile += "xsNorm" if xsNorm else ""

if applyMETCut:
    psfile+="_met%d" %(applyMETCut) 
    title+="Met Cut %d" %(applyMETCut)
psfile += ".eps"

r.gStyle.SetOptStat(0)
signalEntries = enVars.signalEntries
ttEntries = enVars.ttEntries
ZZEntries = enVars.ZZEntries
signalLocation = enVars.signalLocation
ttLocation = enVars.ttLocation
ZZLocation = enVars.ZZLocation
#*******Open input file and find associated tree*******
HChain = r.TChain("ttTreeFinal/eventTree")
ttChain = r.TChain("ttTreeFinal/eventTree")
ZZChain = r.TChain("ttTreeFinal/eventTree")
tool.addFiles(ch=HChain, dirName=signalLocation, knownEventNumber=signalEntries)
tool.addFiles(ch=ttChain, dirName=ttLocation, knownEventNumber=ttEntries)
tool.addFiles(ch=ZZChain, dirName=ZZLocation, knownEventNumber=ZZEntries)
sigPreSelection = tool.addHistFirstBinFromFiles(dirName=signalLocation)+0.
ttPreSelection = tool.addHistFirstBinFromFiles(dirName=ttLocation)+0.
ZZPreSelection = tool.addHistFirstBinFromFiles(dirName=ZZLocation)+0.
tauPt1_h = r.TH1F("tauPt1_h"," ", 45, 25, 250)
tauPt1_tt = r.TH1F("tauPt1_tt"," ", 45, 25, 250)
tauPt1_zz = r.TH1F("tauPt1_zz"," ", 45, 25, 250)
tauPt2_h = r.TH1F("tauPt2_h"," ", 25, 25, 150)
tauPt2_tt = r.TH1F("tauPt2_tt"," ", 25, 25, 150)
tauPt2_zz = r.TH1F("tauPt2_zz"," ", 25, 25, 150)
tauIso1_h = r.TH1F("tauIso1_h"," ", 30, 0, 1.5)
tauIso1_tt = r.TH1F("tauIso1_tt"," ", 30, 0, 1.5)
tauIso1_zz = r.TH1F("tauIso1_zz"," ", 30, 0, 1.5)
tauIso2_h = r.TH1F("tauIso2_h"," ", 30, 0, 1.5)
tauIso2_tt = r.TH1F("tauIso2_tt"," ", 30, 0, 1.5)
tauIso2_zz = r.TH1F("tauIso2_zz"," ", 30, 0, 1.5)

#for normalization
HistNameList = [tauPt1_h, tauPt1_tt, tauPt1_zz, tauPt2_h, tauPt2_tt, tauPt2_zz,
                tauIso1_h, tauIso1_tt, tauIso1_zz, tauIso2_h, tauIso2_tt, tauIso2_zz]
xsList = (15.9, 26197.5, 2502.)

ChainHistList = [(HChain, signalLocation, signalEntries, tauPt1_h, tauPt2_h, tauIso1_h, tauIso2_h),
                 (ttChain, ttLocation, ttEntries, tauPt1_tt, tauPt2_tt, tauIso1_tt, tauIso2_tt),
                 (ZZChain, ZZLocation, ZZEntries, tauPt1_zz, tauPt2_zz, tauIso1_zz, tauIso2_zz)]

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()

for iChain, iLocation, iEntries, iHist1, iHist2, iHist3, iHist4 in ChainHistList:
    total = iEntries if iEntries else iChain.GetEntriesFast()
    key =  "found" if not iEntries else "has"
    print "[%s] %s %d events" %(iLocation, key, total)

    for i in range(0, total):
        iChain.GetEntry(i)
        tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample')
        jetsList = [(iChain.J1CSVbtag, J1.SetCoordinates(iChain.J1Pt, iChain.J1Eta, iChain.J1Phi, iChain.J1Mass)),
                    (iChain.J2CSVbtag, J2.SetCoordinates(iChain.J2Pt, iChain.J2Eta, iChain.J2Phi, iChain.J2Mass)),
                    (iChain.J3CSVbtag, J3.SetCoordinates(iChain.J3Pt, iChain.J3Eta, iChain.J3Phi, iChain.J3Mass)),
                    (iChain.J4CSVbtag, J4.SetCoordinates(iChain.J4Pt, iChain.J4Eta, iChain.J4Phi, iChain.J4Mass))]
        jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
        if JetPtEtaCut:
            if jetsList[0][1].pt() < 20 or abs(jetsList[0][1].eta()) >= 2.4:
                continue
            if jetsList[1][1].pt() < 20 or abs(jetsList[1][1].eta()) >= 2.4:
                continue
        if (jetsList[0][0] < CSVCut1) or (jetsList[1][0] < CSVCut2):
            continue
        if (jetsList[0][1]+jetsList[1][1]).mass() < diJetMassCut[0] or (jetsList[0][1]+jetsList[1][1]).mass() > diJetMassCut[1]:
            continue
        for j in range(iChain.pt1.size()):
            iHist1.Fill(iChain.pt1.at(j))
            iHist2.Fill(iChain.pt2.at(j))
            iHist3.Fill(iChain.iso1.at(j))
            iHist4.Fill(iChain.iso2.at(j))
    print ''

if xsNorm:
    tool.xsNormHists(HistNameList, xsList)
    title += "; tauPt; Events/bin/20 fb^{-1}"
else:
    intList = tool.unitNormHists(HistNameList)
    title1 = title + "; tau1 pt; Unit Normalized"
    title2 = title + "; tau2 pt; Unit Normalized"
    title3 = title + "; tau1 iso; Unit Normalized"
    title4 = title + "; tau2 iso; Unit Normalized"

legendPosition = (0.45, 0.75, 0.88, 0.85)
legendHistos1 = [(tauPt1_h,"H -> hh -> #tau^{+}#tau^{-} b#bar{b}"), #(%.2f events/20 fb^{-1})" %(intList[0]*xsList[0]*20/sigPreSelection)),
                (tauPt1_tt,"t#bar{t} -> b#bar{b} ll"),# (%.1f events/20 fb^{-1})" %(intList[1]*xsList[1]*20/ttPreSelection)),
                (tauPt1_zz,"ZZ + jets -> 2q 2l")]# (%.1f events/20 fb^{-1})" %(intList[2]*xsList[2]*20/ZZPreSelection))]
legendHistos2 = [(tauPt2_h,"H -> hh -> #tau^{+}#tau^{-} b#bar{b}"), #(%.2f events/20 fb^{-1})" %(intList[0]*xsList[0]*20/sigPreSelection)),
                (tauPt2_tt,"t#bar{t} -> b#bar{b} ll"),# (%.1f events/20 fb^{-1})" %(intList[1]*xsList[1]*20/ttPreSelection)),
                (tauPt2_zz,"ZZ + jets -> 2q 2l")]# (%.1f events/20 fb^{-1})" %(intList[2]*xsList[2]*20/ZZPreSelection))]
legendHistos3 = [(tauIso1_h,"H -> hh -> #tau^{+}#tau^{-} b#bar{b}"), #(%.2f events/20 fb^{-1})" %(intList[0]*xsList[0]*20/sigPreSelection)),
                (tauIso1_tt,"t#bar{t} -> b#bar{b} ll"),# (%.1f events/20 fb^{-1})" %(intList[1]*xsList[1]*20/ttPreSelection)),
                (tauIso1_zz,"ZZ + jets -> 2q 2l")]# (%.1f events/20 fb^{-1})" %(intList[2]*xsList[2]*20/ZZPreSelection))]
legendHistos4 = [(tauIso2_h,"H -> hh -> #tau^{+}#tau^{-} b#bar{b}"), #(%.2f events/20 fb^{-1})" %(intList[0]*xsList[0]*20/sigPreSelection)),
                (tauIso2_tt,"t#bar{t} -> b#bar{b} ll"),# (%.1f events/20 fb^{-1})" %(intList[1]*xsList[1]*20/ttPreSelection)),
                (tauIso2_zz,"ZZ + jets -> 2q 2l")]# (%.1f events/20 fb^{-1})" %(intList[2]*xsList[2]*20/ZZPreSelection))]


tauPt1_zz.SetTitle(title1)
tauPt1_zz.GetYaxis().SetTitleOffset(1.4)
tauPt2_zz.SetTitle(title2)
tauPt2_zz.GetYaxis().SetTitleOffset(1.4)
tauIso1_h.SetTitle(title3)
tauIso1_h.GetYaxis().SetTitleOffset(1)
tauIso2_h.SetTitle(title4)
tauIso2_h.GetYaxis().SetTitleOffset(1)

c = r.TCanvas("c","Test", 800, 500)
# c.Divide(2,2)

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)

# c.cd(1)
# r.gPad.SetTickx()
# r.gPad.SetTicky()
# tool.setDrawHists(sigHist=tauPt1_h, ttHist=tauPt1_tt, ZZHist=tauPt1_zz)
# l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos1)
# l1.Draw("same")

# c.cd(2)
r.gPad.SetTickx()
r.gPad.SetTicky()
tool.setDrawHists(sigHist=tauPt2_h, ttHist=tauPt2_tt, ZZHist=tauPt2_zz)
l2 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos2)
l2.Draw("same")
print "total events: %f" %(tauPt2_h.Integral(0,25))
print "events with pt2 < %f: %f" %(tauPt2_h.GetBinLowEdge(5),tauPt2_h.Integral(0,4))
print "events with pt2 > %f: %f" %(tauPt2_h.GetBinLowEdge(5),tauPt2_h.Integral(5, 25))
# c.cd(3)
# r.gPad.SetTickx()
# r.gPad.SetTicky()
# tool.setDrawHists(sigHist=tauIso1_h, ttHist=tauIso1_tt, ZZHist=tauIso1_zz)
# l3 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos3)
# l3.Draw("same")
# 
# c.cd(4)
# r.gPad.SetTickx()
# r.gPad.SetTicky()
# tool.setDrawHists(sigHist=tauIso2_h, ttHist=tauIso2_tt, ZZHist=tauIso2_zz)
# l4 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos4)
# l4.Draw("same")
# ps.Close()

print "Plot saved at %s" %(psfile)
