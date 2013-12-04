#!/usr/bin/env python

import ROOT as r

psfile="gen_jet.eps"

#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/TempCode/analysis_new.root")
tree = ifile.Get("ttTreeFinal/eventTree")

h_r1 = r.TH1F("r1","r1", 10, 0, 1)
h_r2 = r.TH1F("r2","r2", 10, 0, 1)
h_genpt1 = r.TH1F("h_genpt1","h_genpt1", 50, 0, 250)
h_genpt2 = r.TH1F("h_genpt2","h_genpt2", 50, 0, 250)
h_jpt1 = r.TH1F("h_jpt1","h_jpt1", 50, 0, 250)
h_jpt2 = r.TH1F("h_jpt2","h_jpt2", 50, 0, 250)

h_r1.SetTitle("closet jet to gen jet1; #Deltar; ")
h_r2.SetTitle("closet jet to gen jet2; #Deltar; ")

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
v1 = lvClass()
v2 = lvClass()
v_tmp = lvClass()

for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)
    pt1 = tree.GetLeaf("J1GenPt").GetValue(0)
    pt2 = tree.GetLeaf("J2GenPt").GetValue(0)
    eta1 = tree.GetLeaf("J1GenEta").GetValue(0)
    eta2 = tree.GetLeaf("J2GenEta").GetValue(0)
    phi1 = tree.GetLeaf("J1GenPhi").GetValue(0)
    phi2 = tree.GetLeaf("J2GenPhi").GetValue(0)

    v1.SetCoordinates(pt1, eta1, phi1, 0)
    v2.SetCoordinates(pt2, eta2, phi2, 0)

    dr1 = 1000
    dr2 = 1000
    for j in range(1, 5):
        v_tmp.SetCoordinates(tree.GetLeaf("J%sPt" %(j)).GetValue(0),
                             tree.GetLeaf("J%sEta" %(j)).GetValue(0),
                             tree.GetLeaf("J%sPhi" %(j)).GetValue(0),
                             0)
        if dr1 > r.Math.VectorUtil.DeltaR(v1, v_tmp):
            dr1 = r.Math.VectorUtil.DeltaR(v1, v_tmp)
            jpt1 = tree.GetLeaf("J%sPt" %(j)).GetValue(0)
        if dr2 > r.Math.VectorUtil.DeltaR(v2, v_tmp):
            dr2 = r.Math.VectorUtil.DeltaR(v2, v_tmp)
            jpt2 = tree.GetLeaf("J%sPt" %(j)).GetValue(0)

    h_r1.Fill(dr1)
    h_r2.Fill(dr2)
    h_genpt1.Fill(pt1)
    h_genpt2.Fill(pt2)
    h_jpt1.Fill(jpt1)
    h_jpt2.Fill(jpt2)

c = r.TCanvas("c","Test", 800, 600);
c.SetBorderMode(0)
c.Divide(2,2)

ps = r.TPostScript(psfile,112);
ps.NewPage();

c.cd(1)
h_r1.Draw()
c.cd(2)
h_r2.Draw()
c.cd(3)
l1 = r.TLegend(0.55,0.68,0.85,0.78);
l1.SetFillStyle(0);
l1.SetBorderSize(0);
h_genpt1.Draw()
h_jpt1.SetLineColor(2)
h_jpt1.Draw("same")
l1.AddEntry(h_genpt1,"gen jet1 pt");
l1.AddEntry(h_jpt1,"closest reco jet pt");
l1.Draw("same")
c.cd(4)
l2 = r.TLegend(0.55,0.68,0.85,0.78);
l2.SetFillStyle(0);
l2.SetBorderSize(0);
h_genpt2.Draw()
h_jpt2.SetLineColor(2)
h_jpt2.Draw("same")
l2.AddEntry(h_genpt2,"gen jet2 pt");
l2.AddEntry(h_jpt2,"closest reco jet pt");
l2.Draw("same")

ps.Close()