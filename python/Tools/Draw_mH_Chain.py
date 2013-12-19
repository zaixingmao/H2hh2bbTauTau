#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="mTauTauJJ"

#Title = "No Required b Tags, EleMuLooseVeto on Leg1"
title = "mTauTauJJ"
xsNorm = False
DrawSVMass = True
JetPtEtaCut = True
CSVCut1 = -9999999#0.679
CSVCut2 = -9999999#0.244
diJetCandMassCut = (-5,9999)#(100,140)
diTauCandMassCut = (-5,9999)#(100,130)

useVarHMass = False

applyMETCut = 0 
psfile = psfile + "_diJet_%d_%d" %(diJetCandMassCut[0], diJetCandMassCut[1])
psfile = psfile + "_diTau_%d_%d" %(diTauCandMassCut[0], diTauCandMassCut[1])
title = title + "_diJet_%d_%d" %(diJetCandMassCut[0], diJetCandMassCut[1])
title = title + "_diTau_%d_%d" %(diTauCandMassCut[0], diTauCandMassCut[1])
if useVarHMass:
    psfile += "_useHMass"

title = "mTauTauJJ SVFit"

if CSVCut1 == 0.679 and CSVCut2 == 0.244:
    title = title + "(1 medium, 1 loose b tag)"
    psfile = psfile + "_2_b_tag"
else:
    psfile = psfile + "_no_b_tag"
psfile += "xsNorm" if xsNorm else ""

if applyMETCut:
    psfile+="_met%d" %(applyMETCut) 
    title+="Met Cut %d" %(applyMETCut)
psfile += ".eps" if not DrawSVMass else "_SVFitMass.eps"

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
mTauTauJJ_h = r.TH1F("mTauTauJJ_h"," ", 120, 100, 700)
mTauTauJJ_tt = r.TH1F("mTauTauJJ_tt"," ", 120, 100, 700)
mTauTauJJ_zz = r.TH1F("mTauTauJJ_zz"," ", 120, 100, 700)

#for normalization
HistNameList = [mTauTauJJ_h, mTauTauJJ_tt, mTauTauJJ_zz]
xsList = (15.9, 26197.5, 2502.)

ChainHistList = [(HChain, signalLocation, signalEntries, mTauTauJJ_h),
                 (ttChain, ttLocation, ttEntries, mTauTauJJ_tt),
                 (ZZChain, ZZLocation, ZZEntries, mTauTauJJ_zz)]

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()
combinedJJ = lvClass()
combinedTauTau = lvClass()

for iChain, iLocation, iEntries, iHist in ChainHistList:
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
        mJJ = (jetsList[0][1]+jetsList[1][1]).mass()
        combinedJJ = jetsList[0][1]+jetsList[1][1]
        if JetPtEtaCut:
            if jetsList[0][1].pt() < 20 or abs(jetsList[0][1].eta()) >= 2.4:
                continue
            if jetsList[1][1].pt() < 20 or abs(jetsList[1][1].eta()) >= 2.4:
                continue
        if (jetsList[0][0] < CSVCut1) or (jetsList[1][0] < CSVCut2):
            continue
        if mJJ < diJetCandMassCut[0] or mJJ > diJetCandMassCut[1]:
            continue
        if DrawSVMass:
            for iMass in range(iChain.svMass.size()):
                if applyMETCut:
                    if iChain.met.at(iMass) < applyMETCut:
                        continue
                diTauCandMass = iChain.svMass.at(iMass)
                combinedTauTau.SetCoordinates(iChain.fullPt, iChain.fullEta, iChain.fullPhi, diTauCandMass)
                if diTauCandMass < diTauCandMassCut[0] or diTauCandMass > diTauCandMassCut[1]:
                    continue
                iHist.Fill((combinedTauTau + combinedJJ).mass())
        elif useVarHMass:
            iHist.Fill(iChain.HMass)
        else:
            for iTauPair in range(iChain.pt1.size()):
                if applyMETCut:
                    if iChain.met.at(iTauPair) < applyMETCut:
                        continue
                tau1.SetCoordinates(iChain.pt1.at(iTauPair), iChain.eta1.at(iTauPair), iChain.phi1.at(iTauPair), iChain.m1.at(iTauPair))
                tau2.SetCoordinates(iChain.pt2.at(iTauPair), iChain.eta2.at(iTauPair), iChain.phi2.at(iTauPair), iChain.m2.at(iTauPair))
                tauTauJJMass = (tau1+tau2+jetsList[0][1]+jetsList[1][1]).mass()
                iHist.Fill(tauTauJJMass)
    print ''

if xsNorm:
    tool.xsNormHists(HistNameList, xsList)
    title += "; mTauTauJJ; Events/bin/20 fb^{-1}"
else:
    intList = tool.unitNormHists(HistNameList)
    title += "; mTauTauJJ; Unit Normalized"

legendPosition = (0.45, 0.75, 0.88, 0.85)
legendHistos = [(mTauTauJJ_h,"H -> hh -> #tau^{+}#tau^{-} b#bar{b}"), #(%.2f events/20 fb^{-1})" %(intList[0]*xsList[0]*20/sigPreSelection)),
                (mTauTauJJ_tt,"t#bar{t} -> b#bar{b} ll"),# (%.1f events/20 fb^{-1})" %(intList[1]*xsList[1]*20/ttPreSelection)),
                (mTauTauJJ_zz,"ZZ + jets -> 2q 2l")]# (%.1f events/20 fb^{-1})" %(intList[2]*xsList[2]*20/ZZPreSelection))]

mTauTauJJ_zz.SetTitle(title)
mTauTauJJ_h.SetTitle(title)
mTauTauJJ_h.GetYaxis().SetTitleOffset(1.2)
mTauTauJJ_zz.GetYaxis().SetTitleOffset(1.3)
c = r.TCanvas("c","Test", 800, 600)
r.gPad.SetTickx()
r.gPad.SetTicky()

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)

tool.setDrawHists(sigHist=mTauTauJJ_h, ttHist=mTauTauJJ_tt, ZZHist=mTauTauJJ_zz)
l = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos)
l.Draw("same")
ps.Close()

print "Plot saved at %s" %(psfile)
