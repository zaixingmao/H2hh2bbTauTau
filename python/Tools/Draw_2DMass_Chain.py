#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os

psfile="2DMass_signal"

r.gStyle.SetOptStat(0)

CSVCut1 = 0.679

#title = "t#bar{t}"
title = "H -> hh"

if CSVCut1 == 0.679:
    title = title + "(1 medium b tag)"
    psfile = psfile + "_1_b_tag.eps"
# if CSVCut1 == 0.679 and CSVCut2 == 0.679:
#     title = title + "(2 medium b tags)"
#     psfile = psfile + "_2_b_tag.eps"
# if CSVCut1 < 0 and CSVCut2 < 0:
#     title = title + "(no b tags)"
#     psfile = psfile + "_no_b_tag.eps"


#*******Open input file and find associated tree*******
Chain = r.TChain("ttTreeFinal/eventTree")
tool.addFiles(ch=Chain, dirName="/hdfs/store/user/zmao/H2hh-SUB-TT")
#tool.addFiles(ch=Chain, dirName="/hdfs/store/user/zmao/tt-SUB-TT")
# tool.addFiles(ch=Chain, dirName="/hdfs/store/user/zmao/ZZ2-SUB-TT")

mjj = r.TH1F("mjj"," ", 40, 0, 200)
mTauTau = r.TH1F("mTauTau"," ", 40, 0, 200)
Mass = r.TH2F("2DMass"," ", 70, 0, 350, 60, 0, 300)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()

print 'Getting nEntries in sample...'
total= Chain.GetEntries()
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

    for i in range(Chain.pt1.size()):
        tau1.SetCoordinates(Chain.pt1.at(i), Chain.eta1.at(i), Chain.phi1.at(i), Chain.m1.at(i))
        tau2.SetCoordinates(Chain.pt2.at(i), Chain.eta2.at(i), Chain.phi2.at(i), Chain.m2.at(i))
        mTauTau.Fill((tau1+tau2).mass())
        Mass.Fill((jetsList[0][1]+jetsList[1][1]).mass(), (tau1+tau2).mass())


print ''

c = r.TCanvas("c","Test", 800, 600)
psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)
Mass.SetTitle("%s; mJJCSVSort; m(#tau#tau)" %(title))
Mass.GetYaxis().SetTitleOffset(1.2)
Mass.Draw("COLZ")

ps.Close()
