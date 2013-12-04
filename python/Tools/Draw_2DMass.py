#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter

psfile="2DMass_tt"

r.gStyle.SetOptStat(0)
CSVCut1 = 0.679
CSVCut2 = 0.679

applyEleMuLooseVeto1 = 1

title = "t#bar{t}"
#title = "H -> hh "

if CSVCut1 == 0.679 and CSVCut2 < 0:
    title = title + "(1 medium b tag)"
    psfile = psfile + "_1_b_tag.eps"
if CSVCut1 == 0.679 and CSVCut2 == 0.679:
    title = title + "(2 medium b tags)"
    psfile = psfile + "_2_b_tag.eps"
if CSVCut1 < 0 and CSVCut2 < 0:
    title = title + "(no b tags)"
    psfile = psfile + "_no_b_tag.eps"
if applyEleMuLooseVeto1:
    psfile = psfile[0:psfile.find('.')] + "_emLooseVeto.eps"
    title = title + " emLooseVeto"


#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/TempCode/analysis_tt.root")
tree = ifile.Get("ttTreeFinal/eventTree")

mjj = r.TH1F("mjj"," ", 40, 0, 200)
mTauTau = r.TH1F("mTauTau"," ", 40, 0, 200)
Mass = r.TH2F("2DMass"," ", 35, 0, 350, 35, 0, 350)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()
for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)
    if applyEleMuLooseVeto1:
        if tree.tauElectronLMVAPass1 == 0 or tree.againstMuonLoose1 == 0:
            continue

    tau1.SetCoordinates(tree.pt1, tree.eta1, tree.phi1, tree.m1)
    tau2.SetCoordinates(tree.pt2, tree.eta2, tree.phi2, tree.m2)
    mTauTau.Fill((tau1+tau2).mass())

    jetsList = [(tree.J1CSVbtag, J1.SetCoordinates(tree.J1Pt, tree.J1Eta, tree.J1Phi, tree.J1M)),
                (tree.J2CSVbtag, J2.SetCoordinates(tree.J2Pt, tree.J2Eta, tree.J2Phi, tree.J2M)),
                (tree.J3CSVbtag, J3.SetCoordinates(tree.J3Pt, tree.J3Eta, tree.J3Phi, tree.J3M)),
                (tree.J4CSVbtag, J4.SetCoordinates(tree.J4Pt, tree.J4Eta, tree.J4Phi, tree.J4M))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    if jetsList[0][0] > CSVCut1 and jetsList[1][0] > CSVCut2:
        if jetsList[0][1].Pt() > 10 and jetsList[1][1].Pt() > 10:
            Mass.Fill((jetsList[0][1]+jetsList[1][1]).mass(), (tau1+tau2).mass())


c = r.TCanvas("c","Test", 800, 600)
ps = r.TPostScript(psfile,112)
Mass.SetTitle("%s; mJJCSVSort (both jetPt > 10); m(#tau#tau)" %(title))
Mass.GetYaxis().SetTitleOffset(1.2)
Mass.Draw("COLZ")

ps.Close()
