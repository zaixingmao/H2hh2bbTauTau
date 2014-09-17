#!/usr/bin/env python

import ROOT as r

psfile="jet_mass_Zjet.eps"

#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/TempCode/analysis.root")
tree = ifile.Get("ttTreeFinal/eventTree")

delta_r = r.TH1F("delta_r","delta_r", 100, 0, 5)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()

for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)

    tau1.SetCoordinates(tree.pt1, tree.eta1, tree.phi1, tree.m1)
    tau2.SetCoordinates(tree.pt2, tree.eta2, tree.phi2, tree.m2)

    delta_r.Fill(r.Math.VectorUtil.DeltaR(tau1, tau2))
   
delta_r.Draw()

# h_jjmass_bb.SetLineColor(2)
# 
# c = r.TCanvas("c","Test", 1000, 400);
# c.Divide(2,1)
# ps = r.TPostScript(psfile,112);
# ps.NewPage();
# 
# c.cd(1)
# l1 = r.TLegend(0.55,0.68,0.85,0.78);
# l1.SetFillStyle(0)
# l1.SetBorderSize(0)
# h_jjmass.Draw()
# h_jjmass_bb.Draw("same")
# l1.AddEntry(h_jjmass_bb,"m = 0")
# l1.AddEntry(h_jjmass,"m = jet mass")
# l1.Draw("same")
# c.cd(2)
# 
# h_genmass.Draw()
# ps.Close()
