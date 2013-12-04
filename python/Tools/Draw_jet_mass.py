#!/usr/bin/env python

import ROOT as r

psfile="jet_mass_Zjet.eps"

#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/TempCode/analysisZjet.root")
tree = ifile.Get("ttTreeFinal/eventTree")

h_r1 = r.TH1F("r1","r1", 10, 0, 1)
h_r2 = r.TH1F("r2","r2", 10, 0, 1)
h_genmass = r.TH1F("h_genmass","genjj invariant mass", 90, 20, 200)
h_jjmass = r.TH1F("h_jjmass","jj invariant mass", 90, 20, 200)
h_jjmass_bb = r.TH1F("h_jjmass_bb","jj invariant mass", 90, 20, 200)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
j1 = lvClass()
j2 = lvClass()
j1b = lvClass()
j2b = lvClass()
genj1 = lvClass()
genj2 = lvClass()
v_tmp = lvClass()

for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)

    if tree.GetLeaf("pdg1").GetValue(0) == 0 or tree.GetLeaf("pdg2").GetValue(0) == 0:
        continue

    genj1pt = tree.GetLeaf("J1GenPt").GetValue(0)
    genj2pt = tree.GetLeaf("J2GenPt").GetValue(0)
    genj1eta = tree.GetLeaf("J1GenEta").GetValue(0)
    genj2eta = tree.GetLeaf("J2GenEta").GetValue(0)
    genj1phi = tree.GetLeaf("J1GenPhi").GetValue(0)
    genj2phi = tree.GetLeaf("J2GenPhi").GetValue(0)

    genj1.SetCoordinates(genj1pt, genj1eta, genj1phi, 4.19)
    genj2.SetCoordinates(genj2pt, genj2eta, genj2phi, 4.19)

    dr1 = 1000
    dr2 = 1000
    for j in range(1, 5):
        v_tmp.SetCoordinates(tree.GetLeaf("J%sPt" %(j)).GetValue(0),
                             tree.GetLeaf("J%sEta" %(j)).GetValue(0),
                             tree.GetLeaf("J%sPhi" %(j)).GetValue(0),
                             tree.GetLeaf("J%sM" %(j)).GetValue(0))
        if dr1 > r.Math.VectorUtil.DeltaR(genj1, v_tmp):
            dr1 = r.Math.VectorUtil.DeltaR(genj1, v_tmp)
            j1pt = tree.GetLeaf("J%sPt" %(j)).GetValue(0)
            j1eta = tree.GetLeaf("J%sEta" %(j)).GetValue(0)
            j1phi = tree.GetLeaf("J%sPhi" %(j)).GetValue(0)
            j1mass = tree.GetLeaf("J%sM" %(j)).GetValue(0)
        if dr2 > r.Math.VectorUtil.DeltaR(genj2, v_tmp):
            dr2 = r.Math.VectorUtil.DeltaR(genj2, v_tmp)
            j2pt = tree.GetLeaf("J%sPt" %(j)).GetValue(0)
            j2eta = tree.GetLeaf("J%sEta" %(j)).GetValue(0)
            j2phi = tree.GetLeaf("J%sPhi" %(j)).GetValue(0)
            j2mass = tree.GetLeaf("J%sM" %(j)).GetValue(0)

    j1.SetCoordinates(j1pt, j1eta, j1phi, j1mass)
    j2.SetCoordinates(j2pt, j2eta, j2phi, j2mass)
    j1b.SetCoordinates(j1pt, j1eta, j1phi, 0)
    j2b.SetCoordinates(j2pt, j2eta, j2phi, 0)
    genj1.SetCoordinates(genj1pt, genj1eta, genj1phi, j1mass)
    genj2.SetCoordinates(genj2pt, genj2eta, genj2phi, j2mass)    

#     dr1 = 1000
#     dr2 = 1000
#     for j in range(1, 5):
#         v_tmp.SetCoordinates(tree.GetLeaf("J%sPt" %(j)).GetValue(0),
#                              tree.GetLeaf("J%sEta" %(j)).GetValue(0),
#                              tree.GetLeaf("J%sPhi" %(j)).GetValue(0),
#                              0)
#         if dr1 > r.Math.VectorUtil.DeltaR(v1, v_tmp):
#             dr1 = r.Math.VectorUtil.DeltaR(v1, v_tmp)
#             jpt1 = tree.GetLeaf("J%sPt" %(j)).GetValue(0)
#         if dr2 > r.Math.VectorUtil.DeltaR(v2, v_tmp):
#             dr2 = r.Math.VectorUtil.DeltaR(v2, v_tmp)
#             jpt2 = tree.GetLeaf("J%sPt" %(j)).GetValue(0)

    h_jjmass.Fill((j1+j2).mass())
    h_genmass.Fill((genj1+genj2).mass())
    h_jjmass_bb.Fill((j1b+j2b).mass())

h_jjmass_bb.SetLineColor(2)

c = r.TCanvas("c","Test", 1000, 400);
c.Divide(2,1)
ps = r.TPostScript(psfile,112);
ps.NewPage();

c.cd(1)
l1 = r.TLegend(0.55,0.68,0.85,0.78);
l1.SetFillStyle(0)
l1.SetBorderSize(0)
h_jjmass.Draw()
h_jjmass_bb.Draw("same")
l1.AddEntry(h_jjmass_bb,"m = 0")
l1.AddEntry(h_jjmass,"m = jet mass")
l1.Draw("same")
c.cd(2)

h_genmass.Draw()
ps.Close()
