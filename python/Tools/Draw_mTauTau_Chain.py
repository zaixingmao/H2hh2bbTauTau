#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="mTauTau"

#Title = "No Required b Tags, EleMuLooseVeto on Leg1"
title = "mTauTau"
xsNorm = True
DrawSVMass = True
CSVCut1 = 0.679
CSVCut2 = 0.244 

if CSVCut1 == 0.679 and CSVCut2 == 0.244:
    title = title + "(1 medium, 1 loose b tag)"
    psfile = psfile + "_2_b_tag"
else:
    psfile = psfile + "_no_b_tag"
psfile += "xsNorm" if xsNorm else ""
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
mTauTau_h = r.TH1F("mTauTau_h"," ", 56, 20, 300)
mTauTau_tt = r.TH1F("mTauTau_tt"," ", 56, 20, 300)
mTauTau_zz = r.TH1F("mTauTau_zz"," ", 56, 20, 300)

#for normalization
HistNameList = [mTauTau_h, mTauTau_tt, mTauTau_zz]
xsList = (15.9, 3110.9, 2502)

ChainHistList = [(HChain, signalLocation, signalEntries, mTauTau_h),
                 (ttChain, ttLocation, ttEntries, mTauTau_tt),
                 (ZZChain, ZZLocation, ZZEntries, mTauTau_zz)]

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()
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
        jetsList = [(iChain.J1CSVbtag, J1.SetCoordinates(iChain.J1Pt, iChain.J1Eta, iChain.J1Phi, iChain.J1Mass)),
                    (iChain.J2CSVbtag, J2.SetCoordinates(iChain.J2Pt, iChain.J2Eta, iChain.J2Phi, iChain.J2Mass)),
                    (iChain.J3CSVbtag, J3.SetCoordinates(iChain.J3Pt, iChain.J3Eta, iChain.J3Phi, iChain.J3Mass)),
                    (iChain.J4CSVbtag, J4.SetCoordinates(iChain.J4Pt, iChain.J4Eta, iChain.J4Phi, iChain.J4Mass))]
        jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
        if (jetsList[0][0] < CSVCut1) or (jetsList[1][0] < CSVCut2):
            continue
        if DrawSVMass:
            for iMass in range(iChain.svMass.size()):
                iHist.Fill(iChain.svMass.at(iMass))
        else:
            for iTauPair in range(iChain.pt1.size()):
                tau1.SetCoordinates(iChain.pt1.at(iTauPair), iChain.eta1.at(iTauPair), iChain.phi1.at(iTauPair), iChain.m1.at(iTauPair))
                tau2.SetCoordinates(iChain.pt2.at(iTauPair), iChain.eta2.at(iTauPair), iChain.phi2.at(iTauPair), iChain.m2.at(iTauPair))
                iHist.Fill((tau1+tau2).mass())
    print ''

if xsNorm:
    tool.xsNormHists(HistNameList, xsList)
    title += "; mTauTau; Events/bin/20 fb^{-1}"
else:
    tool.unitNormHists(HistNameList)
    title += "; mTauTau; Unit Normalized"
legendPosition = (0.58, 0.7, 0.88, 0.80)
legendHistos = [(mTauTau_h,"h(125) -> bb"), (mTauTau_zz,"ZZjets -> 2q2l"), (mTauTau_tt,"t#bar{t}")]

mTauTau_zz.SetTitle(title)
mTauTau_h.SetTitle(title)
mTauTau_h.GetYaxis().SetTitleOffset(1.2)
mTauTau_zz.GetYaxis().SetTitleOffset(1.2)
c = r.TCanvas("c","Test", 800, 600)
r.gPad.SetTickx()
r.gPad.SetTicky()

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)

tool.setDrawHists(sigHist=mTauTau_h, ttHist=mTauTau_tt, ZZHist=mTauTau_zz)
l = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos)
l.Draw("same")
ps.Close()

print "Plot saved at %s" %(psfile)
