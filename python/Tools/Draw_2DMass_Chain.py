#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars


DrawWhichSample = "signal"
DrawSVMass = False

r.gStyle.SetOptStat(0)

CSVCut1 = 0.679

title = "H -> hh" if DrawWhichSample == "signal" else "t#bar{t}"


psfile= "2DMass_" + DrawWhichSample
if CSVCut1 == 0.679:
    title = title + "(1 medium b tag)"
    psfile = psfile + "_1_b_tag.eps"
# if CSVCut1 == 0.679 and CSVCut2 == 0.679:
#     title = title + "(2 medium b tags)"
#     psfile = psfile + "_2_b_tag.eps"
# if CSVCut1 < 0 and CSVCut2 < 0:
#     title = title + "(no b tags)"
#     psfile = psfile + "_no_b_tag.eps"

signalLocation = enVars.signalLocation
ttLocation = enVars.ttLocation
signalEntries = enVars.signalEntries
ttEntries = enVars.ttEntries

#*******Open input file and find associated tree*******
Chain = r.TChain("ttTreeFinal/eventTree")
if DrawWhichSample == "signal":
    tool.addFiles(ch=Chain, dirName=signalLocation, knownEventNumber=signalEntries)
    knownSampleEntries=signalEntries
    Location=signalLocation
else:
    tool.addFiles(ch=Chain, dirName=ttLocation, knownEventNumber=ttEntries)
    knownSampleEntries=ttEntries
    Location=ttLocation

Mass = r.TH2F("2DMass"," ", 70, 0, 350, 60, 0, 300)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()

total = knownSampleEntries if knownSampleEntries else Chain.GetEntriesFast()
key =  "found" if not knownSampleEntries else "has"
print "[%s] %s %d events" %(Location, key, total)
for i in range(0, total):
    Chain.GetEntry(i)
    tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample')

    jetsList = [(Chain.J1CSVbtag, J1.SetCoordinates(Chain.J1Pt, Chain.J1Eta, Chain.J1Phi, Chain.J1Mass)),
                (Chain.J2CSVbtag, J2.SetCoordinates(Chain.J2Pt, Chain.J2Eta, Chain.J2Phi, Chain.J2Mass)),
                (Chain.J3CSVbtag, J3.SetCoordinates(Chain.J3Pt, Chain.J3Eta, Chain.J3Phi, Chain.J3Mass)),
                (Chain.J4CSVbtag, J4.SetCoordinates(Chain.J4Pt, Chain.J4Eta, Chain.J4Phi, Chain.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    if not (jetsList[0][0] < CSVCut1):
        continue
    if DrawSVMass:
        for iMass in range(Chain.svMass.size()):
            Mass.Fill((jetsList[0][1]+jetsList[1][1]).mass(), Chain.svMass.at(iMass))
    else:
        for iTauPair in range(Chain.pt1.size()):
            tau1.SetCoordinates(Chain.pt1.at(iTauPair), Chain.eta1.at(iTauPair), Chain.phi1.at(iTauPair), Chain.m1.at(iTauPair))
            tau2.SetCoordinates(Chain.pt2.at(iTauPair), Chain.eta2.at(iTauPair), Chain.phi2.at(iTauPair), Chain.m2.at(iTauPair))
            Mass.Fill((jetsList[0][1]+jetsList[1][1]).mass(), (tau1+tau2).mass())

print ''

c = r.TCanvas("c","Test", 800, 600)
psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)
Mass.SetTitle("%s; mJJCSVSort; m(#tau#tau)" %(title))
Mass.GetYaxis().SetTitleOffset(1.2)
Mass.Draw("COLZ")

ps.Close()

print "Plot saved at %s" %(psfile)