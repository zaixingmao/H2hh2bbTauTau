#!/usr/bin/env python

import ROOT as r

psfile="gen_lep_pt.eps"
r.gStyle.SetOptStat(0)
#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/TempCode/noRequirements.root")
tree = ifile.Get("ttTreeFinal/eventTree")

ele1 = r.TH1F("ele1"," ", 30, 0, 300)
ele2 = r.TH1F("ele2"," ", 30, 0, 300)
mu1 = r.TH1F("mu1"," ", 30, 0, 300)
mu2 = r.TH1F("mu2"," ", 30, 0, 300)
tau1 = r.TH1F("tau1"," ", 30, 0, 300)
tau2 = r.TH1F("tau2"," ", 30, 0, 300)
# 
mu1.SetTitle("; gen lepton 1 pt; ")
mu2.SetTitle("; gen lepton 2 pt; ")


for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)
    if tree.genK0toElePt.size():
        ele1.Fill(tree.genK0toElePt.at(0))
        ele2.Fill(tree.genK0toElePt.at(1))
    if tree.genK0toMuPt.size():
        mu1.Fill(tree.genK0toMuPt.at(0))
        mu2.Fill(tree.genK0toMuPt.at(1))
    if tree.genK0toTauPt.size():
        tau1.Fill(tree.genK0toTauPt.at(0))
        tau2.Fill(tree.genK0toTauPt.at(1))

l1 = r.TLegend(0.55,0.68,0.85,0.78)
l1.SetFillStyle(0)
l1.SetBorderSize(0)
l2 = r.TLegend(0.55,0.68,0.85,0.78)
l2.SetFillStyle(0)
l2.SetBorderSize(0)

ele1.SetLineColor(2)
mu1.SetLineColor(1)
tau1.SetLineColor(4)
ele2.SetLineColor(2)
mu2.SetLineColor(1)
tau2.SetLineColor(4)
tau1.SetFillStyle(3001)
tau2.SetFillStyle(3001)
tau1.SetFillColor(4)
tau1.SetLineWidth(2)
tau2.SetFillColor(4)
tau2.SetLineWidth(2)
ele1.SetLineWidth(2)
ele1.SetFillStyle(3001)
ele1.SetFillColor(2)
ele2.SetLineWidth(2)
ele2.SetFillStyle(3001)
ele2.SetFillColor(2)
mu1.SetLineColor(1)
mu1.SetLineWidth(2)
mu1.SetLineStyle(2)
mu2.SetLineColor(1)
mu2.SetLineWidth(2)
mu2.SetLineStyle(2)

c = r.TCanvas("c","Test", 1300, 500);
c.SetBorderMode(0)
c.Divide(2,1)

ps = r.TPostScript(psfile,112);
ps.NewPage();

c.cd(1)
mu1.Draw()
ele1.Draw("same")
tau1.Draw("same")
l1.AddEntry(ele1,"genEle leg1 pt")
l1.AddEntry(mu1,"genMu leg1 pt")
l1.AddEntry(tau1,"genTau leg1 pt")
l1.Draw("same")

c.cd(2)
mu2.Draw()
ele2.Draw("same")
tau2.Draw("same")
l2.AddEntry(ele2,"genEle leg2 pt")
l2.AddEntry(mu2,"genMu leg2 pt")
l2.AddEntry(tau2,"genTau leg2 pt")
l2.Draw("same")


ps.Close()