#!/usr/bin/env python

import ROOT as r

psfile="match_b_zjet.eps"

#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/TempCode/analysisZjet.root")
tree = ifile.Get("ttTreeFinal/eventTree")

h_r1 = r.TH1F("r1","r1", 10, 0, 1)
h_r2 = r.TH1F("r2","r2", 10, 0, 1)
h_r1_reco = r.TH1F("r1_reco","", 10, 0, 1)
h_r2_reco = r.TH1F("r2_reco","r2", 10, 0, 1)
h_genmbb = r.TH1F("h_genmbb","gen mBB", 50, 0, 250)
h_genJJ = r.TH1F("h_genmjj","gen mjj with #DeltaR < 0.5", 50, 0, 250)
h_recoJJ = r.TH1F("h_genmjj","reco mjj", 50, 0, 250)

h_r1.SetTitle("closet gen jet to b; #DeltaR; ")
h_r1_reco.SetTitle("closet reco jet to gen jet; #DeltaR; ")

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
                    
        h_r1.Fill(dr1)   
        h_r2.Fill(dr2)

        if dr1 >= 0.5 or dr2 >= 0.5:
            continue

        j1.SetCoordinates(j1pt, j1eta, j1phi, 4.8)
        j2.SetCoordinates(j2pt, j2eta, j2phi, 4.8)

        h_genmbb.Fill((b1+b2).mass())
        h_genJJ.Fill((j1+j2).mass())  

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

        h_r1_reco.Fill(dr1)
        h_r2_reco.Fill(dr2)

        j1_reco.SetCoordinates(j1pt, j1eta, j1phi, 4.8)
        j2_reco.SetCoordinates(j2pt, j2eta, j2phi, 4.8)
        h_recoJJ.Fill((j1_reco+j2_reco).mass())




l1 = r.TLegend(0.5,0.66,0.8,0.76);
l1.SetFillStyle(0)
l1.SetBorderSize(0)
l2 = r.TLegend(0.5,0.66,0.8,0.76);
l2.SetFillStyle(0)
l2.SetBorderSize(0)

c = r.TCanvas("c","Test", 1000, 800);
c.SetBorderMode(0)
c.Divide(2,2)

ps = r.TPostScript(psfile,112);
ps.NewPage();

c.cd(1)
h_r1.Draw()
h_r2.SetLineColor(2)
h_r2.Draw("same")
l1.AddEntry(h_r1,"gen jet match for b1")
l1.AddEntry(h_r2,"gen jet match for b2")
l1.Draw("same")
c.cd(2)
h_genmbb.SetLineColor(2)
h_genJJ.Draw()
h_genmbb.Draw("same")
c.cd(3)
h_r1_reco.Draw()
h_r2_reco.SetLineColor(2)
h_r2_reco.Draw("same")
l2.AddEntry(h_r1_reco,"reco jet match for jet1")
l2.AddEntry(h_r2_reco,"reco jet match for jet2")
l2.Draw("same")
c.cd(4)
h_recoJJ.Draw()

ps.Close()
