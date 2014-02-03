#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="genHiggsPtvsTauTauPt"

#Title = "No Required b Tags, EleMuLooseVeto on Leg1"
title = psfile
xsNorm = False
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

title = "genHiggsPtvsTauTauPt"

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

genHiggsPtvsTauTauPt_h1 = r.TH2F("genHiggsPtvsTauTauPt_h1"," ", 36, 20, 200, 36, 20, 200)
genHiggsPtvsTauTauPt_h2 = r.TH2F("genHiggsPtvsTauTauPt_h2"," ", 36, 20, 200, 36, 20, 200)
genHiggsPtvsTauTauPt_h3 = r.TH2F("genHiggsPtvsTauTauPt_h3"," ", 36, 20, 200, 36, 20, 200)
genHiggsPtvsTauTauPt_tt = r.TH2F("genHiggsPtvsTauTauPt_tt"," ", 36, 20, 200, 36, 20, 200)
genHiggsPtvsTauTauPt_zz = r.TH2F("genHiggsPtvsTauTauPt_zz"," ", 36, 20, 200, 36, 20, 200)

genHiggsPtvsTauTauPt_h1_svFit = r.TH2F("genHiggsPtvsTauTauPt_h1_svFit"," ", 36, 20, 200, 36, 20, 200)
genHiggsPtvsTauTauPt_h2_svFit = r.TH2F("genHiggsPtvsTauTauPt_h2_svFit"," ", 36, 20, 200, 36, 20, 200)
genHiggsPtvsTauTauPt_h3_svFit = r.TH2F("genHiggsPtvsTauTauPt_h3_svFit"," ", 36, 20, 200, 36, 20, 200)
genHiggsPtvsTauTauPt_tt_svFit = r.TH2F("genHiggsPtvsTauTauPt_tt_svFit"," ", 36, 20, 200, 36, 20, 200)
genHiggsPtvsTauTauPt_zz_svFit = r.TH2F("genHiggsPtvsTauTauPt_zz_svFit"," ", 36, 20, 200, 36, 20, 200)


ChainHistList = [(H1Chain, signal1Location, signalEntries, genHiggsPtvsTauTauPt_h1, genHiggsPtvsTauTauPt_h1_svFit),
                 (H2Chain, signal2Location, signalEntries, genHiggsPtvsTauTauPt_h2, genHiggsPtvsTauTauPt_h2_svFit),
                 (H3Chain, signal3Location, signalEntries, genHiggsPtvsTauTauPt_h3, genHiggsPtvsTauTauPt_h3_svFit),
                 (ttChain, ttLocation, ttEntries, genHiggsPtvsTauTauPt_tt, genHiggsPtvsTauTauPt_tt_svFit),
                 (ZZChain, ZZLocation, ZZEntries, genHiggsPtvsTauTauPt_zz, genHiggsPtvsTauTauPt_zz_svFit)]

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()
combinedJJ = lvClass()
combinedTauTau = lvClass()
vetoedHiggs = lvClass()

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
        if JetPtEtaCut:
            if jetsList[0][1].pt() < 20 or abs(jetsList[0][1].eta()) >= 2.4:
                continue
            if jetsList[1][1].pt() < 20 or abs(jetsList[1][1].eta()) >= 2.4:
                continue
        if (jetsList[0][0] < CSVCut1) or (jetsList[1][0] < CSVCut2):
            continue

        #loop through gen higgs
        vetoedHiggs, dr = tool.genHiggsMatchGenTaus(iChain)
        if dr > 0.5:  #look for genTaus matching genHiggs within dr = 0.5
            continue

        for iMass in range(iChain.svMass.size()):
            if applyMETCut:
                if iChain.met.at(iMass) < applyMETCut:
                    continue
            diTauCandMass = iChain.svMass.at(iMass)
            combinedTauTau.SetCoordinates(iChain.svPt.at(iMass), iChain.svEta.at(iMass), iChain.svPhi.at(iMass), diTauCandMass)
            if diTauCandMass < diTauCandMassCut[0] or diTauCandMass > diTauCandMassCut[1]:
                continue
            iHist2.Fill((combinedTauTau).pt(), vetoedHiggs.pt())
        for iTauPair in range(iChain.pt1.size()):
            if applyMETCut:
                if iChain.met.at(iTauPair) < applyMETCut:
                    continue
            tau1.SetCoordinates(iChain.pt1.at(iTauPair), iChain.eta1.at(iTauPair), iChain.phi1.at(iTauPair), iChain.m1.at(iTauPair))
            tau2.SetCoordinates(iChain.pt2.at(iTauPair), iChain.eta2.at(iTauPair), iChain.phi2.at(iTauPair), iChain.m2.at(iTauPair))
            iHist1.Fill((tau1+tau2).pt(), vetoedHiggs.pt())

    print ''

title += "; tauTauPt; genHiggsPt"


legendPosition = (0.4, 0.75, .9, 0.85)#(0.45, 0.75, 0.88, 0.85)

legendHistos1 = [(genHiggsPtvsTauTauPt_h1,"(H260) reco TauTau vs gen Higgs" )]
legendHistos2 = [(genHiggsPtvsTauTauPt_h1_svFit,"(H260_SVFit) reco TauTau vs gen Higgs")]
legendHistos3 = [(genHiggsPtvsTauTauPt_h2,"(H300) reco TauTau vs gen Higgs" )]
legendHistos4 = [(genHiggsPtvsTauTauPt_h2_svFit,"(H300_SVFit) reco TauTau vs gen Higgs")]
legendHistos5 = [(genHiggsPtvsTauTauPt_h3,"(H350) reco TauTau vs gen Higgs" )]
legendHistos6 = [(genHiggsPtvsTauTauPt_h3_svFit,"(H350_SVFit) reco TauTau vs gen Higgs")]
legendHistos7 = [(genHiggsPtvsTauTauPt_tt,"(t#bar{t}) reco TauTau vs gen Higgs" )]
legendHistos8 = [(genHiggsPtvsTauTauPt_tt_svFit,"(t#bar{t}) reco TauTau vs gen Higgs")]
legendHistos9 = [(genHiggsPtvsTauTauPt_zz,"(ZZ) reco TauTau vs gen Higgs" )]
legendHistos10 = [(genHiggsPtvsTauTauPt_zz_svFit,"(ZZ) reco TauTau vs gen Higgs")]

genHiggsPtvsTauTauPt_h1.SetTitle(title)
genHiggsPtvsTauTauPt_h2.SetTitle(title)
genHiggsPtvsTauTauPt_h3.SetTitle(title)
genHiggsPtvsTauTauPt_h1_svFit.SetTitle(title)
genHiggsPtvsTauTauPt_h2_svFit.SetTitle(title)
genHiggsPtvsTauTauPt_h3_svFit.SetTitle(title)
genHiggsPtvsTauTauPt_tt.SetTitle(title)
genHiggsPtvsTauTauPt_zz.SetTitle(title)
genHiggsPtvsTauTauPt_tt_svFit.SetTitle(title)
genHiggsPtvsTauTauPt_zz_svFit.SetTitle(title)
c = r.TCanvas("c","Test", 500, 1000)

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,113)

c.Divide(2,5)
c.cd(1)
r.gPad.SetTickx()
r.gPad.SetTicky()
genHiggsPtvsTauTauPt_h1.Draw()
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos1)
l1.Draw("same")
c.cd(2)
r.gPad.SetTickx()
r.gPad.SetTicky()
genHiggsPtvsTauTauPt_h1_svFit.Draw()
l2 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos2)
l2.Draw("same")
c.cd(3)
r.gPad.SetTickx()
r.gPad.SetTicky()
genHiggsPtvsTauTauPt_h2.Draw()
l3 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos3)
l3.Draw("same")
c.cd(4)
r.gPad.SetTickx()
r.gPad.SetTicky()
genHiggsPtvsTauTauPt_h2_svFit.Draw()
l4 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos4)
l4.Draw("same")
c.cd(5)
r.gPad.SetTickx()
r.gPad.SetTicky()
genHiggsPtvsTauTauPt_h3.Draw()
l5 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos5)
l5.Draw("same")
c.cd(6)
r.gPad.SetTickx()
r.gPad.SetTicky()
genHiggsPtvsTauTauPt_h3_svFit.Draw()
l6 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos6)
l6.Draw("same")

c.cd(7)
r.gPad.SetTickx()
r.gPad.SetTicky()
genHiggsPtvsTauTauPt_tt.Draw()
l7 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos7)
l7.Draw("same")
c.cd(8)
r.gPad.SetTickx()
r.gPad.SetTicky()
genHiggsPtvsTauTauPt_tt_svFit.Draw()
l8 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos8)
l8.Draw("same")

c.cd(9)
r.gPad.SetTickx()
r.gPad.SetTicky()
genHiggsPtvsTauTauPt_zz.Draw()
l9 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos9)
l9.Draw("same")
c.cd(10)
r.gPad.SetTickx()
r.gPad.SetTicky()
genHiggsPtvsTauTauPt_zz_svFit.Draw()
l10 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos10)
l10.Draw("same")

ps.Close()

print "Plot saved at %s" %(psfile)
