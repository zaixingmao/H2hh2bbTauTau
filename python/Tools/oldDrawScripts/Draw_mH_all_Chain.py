#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="mH_all"

#Title = "No Required b Tags, EleMuLooseVeto on Leg1"
title = psfile
xsNorm = False
DrawSVMass = False
JetPtEtaCut = True
CSVCut1 = -999999#0.679
CSVCut2 = -999999#0.244
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

title = "mTauTauJJ"
if DrawSVMass: 
    title += " SVFit"

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
signal1Location = enVars.signal1Location
signal2Location = enVars.signal2Location
signal3Location = enVars.signal3Location
ttLocation = enVars.ttLocation
ZZLocation = enVars.ZZLocation
#*******Open input file and find associated tree*******
H1Chain = r.TChain("ttTreeFinal/eventTree")
H2Chain = r.TChain("ttTreeFinal/eventTree")
H3Chain = r.TChain("ttTreeFinal/eventTree")
ttChain = r.TChain("ttTreeFinal/eventTree")
ZZChain = r.TChain("ttTreeFinal/eventTree")
tool.addFiles(ch=H1Chain, dirName=signal1Location, knownEventNumber=signalEntries)
tool.addFiles(ch=H2Chain, dirName=signal2Location, knownEventNumber=signalEntries)
tool.addFiles(ch=H3Chain, dirName=signal3Location, knownEventNumber=signalEntries)
tool.addFiles(ch=ttChain, dirName=ttLocation, knownEventNumber=ttEntries)
tool.addFiles(ch=ZZChain, dirName=ZZLocation, knownEventNumber=ZZEntries)
mTauTauJJ_h1 = r.TH1F("mTauTauJJ_h1"," ", 120, 100, 700)
mTauTauJJ_h2 = r.TH1F("mTauTauJJ_h2"," ", 120, 100, 700)
mTauTauJJ_h3 = r.TH1F("mTauTauJJ_h3"," ", 120, 100, 700)
mTauTauJJ_tt = r.TH1F("mTauTauJJ_tt"," ", 120, 100, 700)
mTauTauJJ_zz = r.TH1F("mTauTauJJ_zz"," ", 120, 100, 700)

mTauTauJJ_h1_svFit = r.TH1F("mTauTauJJ_h1_svFit"," ", 120, 100, 700)
mTauTauJJ_h2_svFit = r.TH1F("mTauTauJJ_h2_svFit"," ", 120, 100, 700)
mTauTauJJ_h3_svFit = r.TH1F("mTauTauJJ_h3_svFit"," ", 120, 100, 700)
mTauTauJJ_tt_svFit = r.TH1F("mTauTauJJ_tt_svFit"," ", 120, 100, 700)
mTauTauJJ_zz_svFit = r.TH1F("mTauTauJJ_zz_svFit"," ", 120, 100, 700)

#for normalization
HistNameList1 = [mTauTauJJ_h1, mTauTauJJ_h1_svFit]
HistNameList2 = [mTauTauJJ_h2, mTauTauJJ_h2_svFit]
HistNameList3 = [mTauTauJJ_h3, mTauTauJJ_h3_svFit]
HistNameListtt = [mTauTauJJ_tt, mTauTauJJ_tt_svFit]
HistNameListZZ = [mTauTauJJ_zz, mTauTauJJ_zz_svFit]

ChainHistList = [(H1Chain, signal1Location, signalEntries, mTauTauJJ_h1, mTauTauJJ_h1_svFit),
                 (H2Chain, signal2Location, signalEntries, mTauTauJJ_h2, mTauTauJJ_h2_svFit),
                 (H3Chain, signal3Location, signalEntries, mTauTauJJ_h3, mTauTauJJ_h3_svFit),
                 (ttChain, ttLocation, ttEntries, mTauTauJJ_tt, mTauTauJJ_tt_svFit),
                 (ZZChain, ZZLocation, ZZEntries, mTauTauJJ_zz, mTauTauJJ_zz_svFit)]

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()
combinedJJ = lvClass()
combinedTauTau = lvClass()

for iChain, iLocation, iEntries, iHist1, iHist2 in ChainHistList:
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
        for iMass in range(iChain.svMass.size()):
            if applyMETCut:
                if iChain.met.at(iMass) < applyMETCut:
                    continue
            diTauCandMass = iChain.svMass.at(iMass)
            combinedTauTau.SetCoordinates(iChain.svPt.at(iMass), iChain.svEta.at(iMass), iChain.svPhi.at(iMass), diTauCandMass)
            if diTauCandMass < diTauCandMassCut[0] or diTauCandMass > diTauCandMassCut[1]:
                continue
            iHist2.Fill((combinedTauTau + combinedJJ).mass())
        for iTauPair in range(iChain.pt1.size()):
            if applyMETCut:
                if iChain.met.at(iTauPair) < applyMETCut:
                    continue
            tau1.SetCoordinates(iChain.pt1.at(iTauPair), iChain.eta1.at(iTauPair), iChain.phi1.at(iTauPair), iChain.m1.at(iTauPair))
            tau2.SetCoordinates(iChain.pt2.at(iTauPair), iChain.eta2.at(iTauPair), iChain.phi2.at(iTauPair), iChain.m2.at(iTauPair))
            iHist1.Fill((tau1+tau2+combinedJJ).mass())
    print ''

intList1 = tool.unitNormHists(HistNameList1)
intList2 = tool.unitNormHists(HistNameList2)
intList3 = tool.unitNormHists(HistNameList3)
intListtt = tool.unitNormHists(HistNameListtt)
intListZZ = tool.unitNormHists(HistNameListZZ)
title += "; mTauTauJJ; Unit Normalized"


legendPosition = (0.4, 0.75, .9, 0.85)#(0.45, 0.75, 0.88, 0.85)

legendHistos1 = [(mTauTauJJ_h1,"(H260) mean=%.1f, rms=%.1f" %(mTauTauJJ_h1.GetMean(), mTauTauJJ_h1.GetRMS())),
                 (mTauTauJJ_h1_svFit,"(H260_SVFit) mean=%.1f, rms=%.1f" %(mTauTauJJ_h1_svFit.GetMean(), mTauTauJJ_h1_svFit.GetRMS()))]
legendHistos2 = [(mTauTauJJ_h2,"(H300) mean=%.1f, rms=%.1f" %(mTauTauJJ_h2.GetMean(), mTauTauJJ_h2.GetRMS())),
                 (mTauTauJJ_h2_svFit,"(H300_SVFit) mean=%.1f, rms=%.1f" %(mTauTauJJ_h2_svFit.GetMean(), mTauTauJJ_h2_svFit.GetRMS()))]
legendHistos3 = [(mTauTauJJ_h3,"(H350) mean=%.1f, rms=%.1f" %(mTauTauJJ_h3.GetMean(), mTauTauJJ_h3.GetRMS())),
                 (mTauTauJJ_h3_svFit,"(H350_SVFit) mean=%.1f, rms=%.1f" %(mTauTauJJ_h3_svFit.GetMean(), mTauTauJJ_h3_svFit.GetRMS()))]
legendHistos4 = [(mTauTauJJ_tt,"(t#bar{t}) mean=%.1f, rms=%.1f" %(mTauTauJJ_tt.GetMean(), mTauTauJJ_tt.GetRMS())),
                 (mTauTauJJ_tt_svFit,"(t#bar{t}_SVFit) mean=%.1f, rms=%.1f" %(mTauTauJJ_tt_svFit.GetMean(), mTauTauJJ_tt_svFit.GetRMS()))]
legendHistos5 = [(mTauTauJJ_zz,"(ZZ) mean=%.1f, rms=%.1f" %(mTauTauJJ_zz.GetMean(), mTauTauJJ_zz.GetRMS())),
                 (mTauTauJJ_zz_svFit,"(ZZ_SVFit) mean=%.1f, rms=%.1f" %(mTauTauJJ_zz_svFit.GetMean(), mTauTauJJ_zz_svFit.GetRMS()))]

mTauTauJJ_zz.SetTitle(title)
mTauTauJJ_h1.SetTitle(title)
mTauTauJJ_h1.GetYaxis().SetTitleOffset(1.2)
mTauTauJJ_h2.SetTitle(title)
mTauTauJJ_h2.GetYaxis().SetTitleOffset(1.2)
mTauTauJJ_h3.SetTitle(title)
mTauTauJJ_h3.GetYaxis().SetTitleOffset(1.2)
mTauTauJJ_zz.GetYaxis().SetTitleOffset(1.3)
c = r.TCanvas("c","Test", 500, 800)

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,113)

c.Divide(2,3)
c.cd(1)
r.gPad.SetTickx()
r.gPad.SetTicky()
tool.setDraw2Hists(hist1=mTauTauJJ_h1, hist2=mTauTauJJ_h1_svFit, drawColor=4)
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos1)
l1.Draw("same")
c.cd(2)
r.gPad.SetTickx()
r.gPad.SetTicky()
tool.setDraw2Hists(hist1=mTauTauJJ_h2, hist2=mTauTauJJ_h2_svFit, drawColor=6)
l2 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos2)
l2.Draw("same")
c.cd(3)
r.gPad.SetTickx()
r.gPad.SetTicky()
tool.setDraw2Hists(hist1=mTauTauJJ_h3, hist2=mTauTauJJ_h3_svFit, drawColor=8)
l3 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos3)
l3.Draw("same")
c.cd(4)
r.gPad.SetTickx()
r.gPad.SetTicky()
tool.setDraw2Hists(hist1=mTauTauJJ_tt, hist2=mTauTauJJ_tt_svFit, drawColor=2)
l4 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos4)
l4.Draw("same")
c.cd(5)
r.gPad.SetTickx()
r.gPad.SetTicky()
tool.setDraw2Hists(hist1=mTauTauJJ_zz, hist2=mTauTauJJ_zz_svFit, drawColor=1)
l5 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos5)
l5.Draw("same")

ps.Close()

print "Plot saved at %s" %(psfile)
