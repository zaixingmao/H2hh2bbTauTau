#!/usr/bin/env python

import ROOT as r

psfile="match_b_both.eps"

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/TempCode/analysisZjet.root")
ifile2 = r.TFile("/Users/zmao/M-Data/School/TempCode/analysis_new.root")
tree = ifile.Get("ttTreeFinal/eventTree")
tree2 = ifile2.Get("ttTreeFinal/eventTree")

h_recoJJ_h = r.TH1F("h_genmjj_h","reco mjj from h = 125", 50, 0, 200)
h_recoJJ_Z = r.TH1F("h_genmjj_Z","reco mjj from Z", 50, 0, 200)


lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
b1 = lvClass()
b2 = lvClass()
j1 = lvClass()
j2 = lvClass()
j1_reco = lvClass()
j2_reco = lvClass()
v_tmp = lvClass()

for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)

    if tree.bPt.size():
        genBPt1 = tree.bPt.at(0)
        genBPt2 = tree.bPt.at(1)
        genBEta1 = tree.bEta.at(0)
        genBEta2 = tree.bEta.at(1)
        genBPhi1 = tree.bPhi.at(0)
        genBPhi2 = tree.bPhi.at(1)
        genBMass1 = tree.bMass.at(0)
        genBMass2 = tree.bMass.at(1)

        b1.SetCoordinates(genBPt1, genBEta1, genBPhi1, genBMass1)
        b2.SetCoordinates(genBPt2, genBEta2, genBPhi2, genBMass2)
    
        dr1 = 1000
        dr2 = 1000

    #Loop to find best matching gen jet
        for j in range(1, 5):
            v_tmp.SetCoordinates(tree.GetLeaf("J%sGenPt" %(j)).GetValue(0),
                                 tree.GetLeaf("J%sGenEta" %(j)).GetValue(0),
                                 tree.GetLeaf("J%sGenPhi" %(j)).GetValue(0),
                                 4.8)
            if dr1 > r.Math.VectorUtil.DeltaR(b1, v_tmp):
                dr1 = r.Math.VectorUtil.DeltaR(b1, v_tmp)
                j1pt = tree.GetLeaf("J%sGenPt" %(j)).GetValue(0)
                j1eta = tree.GetLeaf("J%sGenEta" %(j)).GetValue(0)
                j1phi = tree.GetLeaf("J%sGenPhi" %(j)).GetValue(0)
            if dr2 > r.Math.VectorUtil.DeltaR(b2, v_tmp):
                dr2 = r.Math.VectorUtil.DeltaR(b2, v_tmp)
                j2pt = tree.GetLeaf("J%sGenPt" %(j)).GetValue(0)
                j2eta = tree.GetLeaf("J%sGenEta" %(j)).GetValue(0)
                j2phi = tree.GetLeaf("J%sGenPhi" %(j)).GetValue(0)


        if dr1 >= 0.5 or dr2 >= 0.5:
            continue

        j1.SetCoordinates(j1pt, j1eta, j1phi, 4.8)
        j2.SetCoordinates(j2pt, j2eta, j2phi, 4.8)

        dr1 = 1000
        dr2 = 1000

    #Loop to find best matching reco jet
        for j in range(1, 5):
            v_tmp.SetCoordinates(tree.GetLeaf("J%sPt" %(j)).GetValue(0),
                                 tree.GetLeaf("J%sEta" %(j)).GetValue(0),
                                 tree.GetLeaf("J%sPhi" %(j)).GetValue(0),
                                 4.8)
            if dr1 > r.Math.VectorUtil.DeltaR(j1, v_tmp):
                dr1 = r.Math.VectorUtil.DeltaR(j1, v_tmp)
                j1pt = tree.GetLeaf("J%sPt" %(j)).GetValue(0)
                j1eta = tree.GetLeaf("J%sEta" %(j)).GetValue(0)
                j1phi = tree.GetLeaf("J%sPhi" %(j)).GetValue(0)
            if dr2 > r.Math.VectorUtil.DeltaR(j2, v_tmp):
                dr2 = r.Math.VectorUtil.DeltaR(j2, v_tmp)
                j2pt = tree.GetLeaf("J%sPt" %(j)).GetValue(0)
                j2eta = tree.GetLeaf("J%sEta" %(j)).GetValue(0)
                j2phi = tree.GetLeaf("J%sPhi" %(j)).GetValue(0)

        j1_reco.SetCoordinates(j1pt, j1eta, j1phi, 4.8)
        j2_reco.SetCoordinates(j2pt, j2eta, j2phi, 4.8)
        h_recoJJ_Z.Fill((j1_reco+j2_reco).mass())

for i in range(0, tree2.GetEntries()):
    tree2.GetEntry(i)

    if tree2.bPt.size():
        genBPt1 = tree2.bPt.at(0)
        genBPt2 = tree2.bPt.at(1)
        genBEta1 = tree2.bEta.at(0)
        genBEta2 = tree2.bEta.at(1)
        genBPhi1 = tree2.bPhi.at(0)
        genBPhi2 = tree2.bPhi.at(1)
        genBMass1 = tree2.bMass.at(0)
        genBMass2 = tree2.bMass.at(1)

        b1.SetCoordinates(genBPt1, genBEta1, genBPhi1, genBMass1)
        b2.SetCoordinates(genBPt2, genBEta2, genBPhi2, genBMass2)
    
        dr1 = 1000
        dr2 = 1000

    #Loop to find best matching gen jet
        for j in range(1, 5):
            v_tmp.SetCoordinates(tree2.GetLeaf("J%sGenPt" %(j)).GetValue(0),
                                 tree2.GetLeaf("J%sGenEta" %(j)).GetValue(0),
                                 tree2.GetLeaf("J%sGenPhi" %(j)).GetValue(0),
                                 4.8)
            if dr1 > r.Math.VectorUtil.DeltaR(b1, v_tmp):
                dr1 = r.Math.VectorUtil.DeltaR(b1, v_tmp)
                j1pt = tree2.GetLeaf("J%sGenPt" %(j)).GetValue(0)
                j1eta = tree2.GetLeaf("J%sGenEta" %(j)).GetValue(0)
                j1phi = tree2.GetLeaf("J%sGenPhi" %(j)).GetValue(0)
            if dr2 > r.Math.VectorUtil.DeltaR(b2, v_tmp):
                dr2 = r.Math.VectorUtil.DeltaR(b2, v_tmp)
                j2pt = tree2.GetLeaf("J%sGenPt" %(j)).GetValue(0)
                j2eta = tree2.GetLeaf("J%sGenEta" %(j)).GetValue(0)
                j2phi = tree2.GetLeaf("J%sGenPhi" %(j)).GetValue(0)


        if dr1 >= 0.5 or dr2 >= 0.5:
            continue

        j1.SetCoordinates(j1pt, j1eta, j1phi, 4.8)
        j2.SetCoordinates(j2pt, j2eta, j2phi, 4.8)

        dr1 = 1000
        dr2 = 1000

    #Loop to find best matching reco jet
        for j in range(1, 5):
            v_tmp.SetCoordinates(tree2.GetLeaf("J%sPt" %(j)).GetValue(0),
                                 tree2.GetLeaf("J%sEta" %(j)).GetValue(0),
                                 tree2.GetLeaf("J%sPhi" %(j)).GetValue(0),
                                 4.8)
            if dr1 > r.Math.VectorUtil.DeltaR(j1, v_tmp):
                dr1 = r.Math.VectorUtil.DeltaR(j1, v_tmp)
                j1pt = tree2.GetLeaf("J%sPt" %(j)).GetValue(0)
                j1eta = tree2.GetLeaf("J%sEta" %(j)).GetValue(0)
                j1phi = tree2.GetLeaf("J%sPhi" %(j)).GetValue(0)
            if dr2 > r.Math.VectorUtil.DeltaR(j2, v_tmp):
                dr2 = r.Math.VectorUtil.DeltaR(j2, v_tmp)
                j2pt = tree2.GetLeaf("J%sPt" %(j)).GetValue(0)
                j2eta = tree2.GetLeaf("J%sEta" %(j)).GetValue(0)
                j2phi = tree2.GetLeaf("J%sPhi" %(j)).GetValue(0)

        j1_reco.SetCoordinates(j1pt, j1eta, j1phi, 4.8)
        j2_reco.SetCoordinates(j2pt, j2eta, j2phi, 4.8)
        h_recoJJ_h.Fill((j1_reco+j2_reco).mass())

l1 = r.TLegend(0.55,0.70,0.9,0.85)
l1.SetFillStyle(0)
l1.SetBorderSize(0)
h_recoJJ_Z.SetLineColor(2)
Z_Scale = 1./6226. * 0.776524 * 20000.
h_Scale = 1./9450. * 15.8991453481 * 20.
print Z_Scale, h_Scale
h_recoJJ_Z.Scale(Z_Scale)
h_recoJJ_h.Scale(h_Scale)
h_recoJJ_Z.SetTitle(";mJJ (GeV); Events / bin / 20 fb^{-1}")
h_recoJJ_Z.GetYaxis().SetTitleOffset(1.2)

c = r.TCanvas("c","Test", 800, 600);
#c.SetLogy()
ps = r.TPostScript(psfile,112)
ps.NewPage();
h_recoJJ_Z.Draw()
h_recoJJ_h.Draw("same")
l1.AddEntry(h_recoJJ_h,"reco jets matching h(125) -> bb")
l1.AddEntry(h_recoJJ_Z,"reco jets matching Z -> bb")
l1.Draw("same")

ps.Close()
