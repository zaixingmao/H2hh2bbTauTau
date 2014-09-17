#!/usr/bin/env python

import ROOT as r

psfile="pdgs.eps"

#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/TempCode/analysisZjet.root")
tree = ifile.Get("ttTreeFinal/eventTree")

h1 = r.TH1F("h1"," ", 40, -10, 10)
h2 = r.TH1F("h1"," ", 40, -10, 10)


for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)

    h1.Fill(tree.pdg1)
    h2.Fill(tree.pdg2)


c = r.TCanvas("c","Test", 1000, 400);
c.SetBorderMode(0)
c.Divide(2,1)
c.cd(1)
h1.Draw()
c.cd(2)
h2.Draw()