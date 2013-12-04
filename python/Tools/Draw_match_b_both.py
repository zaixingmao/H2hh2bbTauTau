#!/usr/bin/env python

import ROOT as r
import tool

psfile="match_b_both_mix.eps"

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******
ifile = r.TFile("/Users/zmao/M-Data/School/TempCode/analysis_zz.root")
ifile2 = r.TFile("/Users/zmao/M-Data/School/TempCode/analysis_signal.root")
ifile3 = r.TFile("/Users/zmao/M-Data/School/TempCode/analysistt.root")
tree = ifile.Get("ttTreeFinal/eventTree")
tree2 = ifile2.Get("ttTreeFinal/eventTree")
tree3 = ifile3.Get("ttTreeFinal/eventTree")

h_recoJJ_h = r.TH1F("h_genmjj_h","reco mjj from h = 125", 50, 0, 200)
h_recoJJ_Z = r.TH1F("h_genmjj_Z","reco mjj from Z", 50, 0, 200)
h_recoJJ_tt = r.TH1F("h_recoJJ_tt","reco mjj from ttbar", 50, 0, 200)
h_recoJJ_h_1tau = r.TH1F("h_recoJJ_h_1tau","reco mjj from h = 125", 50, 0, 200)
h_recoJJ_Z_1tau = r.TH1F("h_recoJJ_Z_1tau","reco mjj from Z", 50, 0, 200)
h_recoJJ_tt_1tau = r.TH1F("h_recoJJ_tt_1tau","reco mjj from ttbar", 50, 0, 200)
h_recoJJ_h_2tau = r.TH1F("h_recoJJ_h_2tau","reco mjj from h = 125", 50, 0, 200)
h_recoJJ_Z_2tau = r.TH1F("h_recoJJ_Z_2tau","reco mjj from Z", 50, 0, 200)
h_recoJJ_tt_2tau = r.TH1F("h_recoJJ_tt_2tau","reco mjj from ttbar", 50, 0, 200)


lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
j1 = lvClass()
j2 = lvClass()
for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)
    if tree.bPt.size():
        j1, j2 = tool.matchBJet(tree = tree)
        if j1 and j2:
            h_recoJJ_Z.Fill((j1+j2).mass())
            if tree.tauPt.size():
                h_recoJJ_Z_1tau.Fill((j1+j2).mass())
            if tree.tauPt.size()>1:
                h_recoJJ_Z_2tau.Fill((j1+j2).mass())

for i in range(0, tree2.GetEntries()):
    tree2.GetEntry(i)
    if tree2.bPt.size():    
        j1, j2 = tool.matchBJet(tree = tree2)
        if j1 and j2:
            h_recoJJ_h.Fill((j1+j2).mass())
            if tree2.tauPt.size():
                h_recoJJ_h_1tau.Fill((j1+j2).mass())
            if tree2.tauPt.size()>1:
                h_recoJJ_h_2tau.Fill((j1+j2).mass())

for i in range(0, tree3.GetEntries()):
    tree3.GetEntry(i)
    if tree3.bPt.size():    
        j1, j2 = tool.matchBJet(tree = tree3)
        if j1 and j2:
            h_recoJJ_tt.Fill((j1+j2).mass())
            if tree3.tauPt.size():
                h_recoJJ_tt_1tau.Fill((j1+j2).mass())
            if tree3.tauPt.size()>1:
                h_recoJJ_tt_2tau.Fill((j1+j2).mass())

legendPosition = (0.58, 0.7, 0.88, 0.85)
l1 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l1.SetFillStyle(0)
l1.SetBorderSize(0)
l2 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l2.SetFillStyle(0)
l2.SetBorderSize(0)
l3 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l3.SetFillStyle(0)
l3.SetBorderSize(0)
l4 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l4.SetFillStyle(0)
l4.SetBorderSize(0)

h_recoJJ_Z.SetLineColor(2)
h_recoJJ_tt.SetLineColor(28)
h_recoJJ_Z_1tau.SetLineColor(2)
h_recoJJ_tt_1tau.SetLineColor(28)
h_recoJJ_Z_2tau.SetLineColor(2)
h_recoJJ_tt_2tau.SetLineColor(28)
Z_xs = 2.502 * 1000.
h_xs = 15.8991453481
tt_xs =  3110.90625

Z_Scale = 1./6226. * Z_xs * 20.
h_Scale = 1./8100. * h_xs * 20.
tt_Scale = 1./10832. * tt_xs * 20.
h_recoJJ_Z.Scale(Z_Scale)
h_recoJJ_h.Scale(h_Scale)
h_recoJJ_tt.Scale(tt_Scale)
h_recoJJ_Z_1tau.Scale(Z_Scale)
h_recoJJ_h_1tau.Scale(h_Scale)
h_recoJJ_tt_1tau.Scale(tt_Scale)
h_recoJJ_Z_2tau.Scale(Z_Scale)
h_recoJJ_h_2tau.Scale(h_Scale)
h_recoJJ_tt_2tau.Scale(tt_Scale)

h_recoJJ_Z.SetTitle(";mJJ (GeV); Events / bin / 20 fb^{-1}")
h_recoJJ_h.SetTitle(";mJJ (GeV); Events / bin / 20 fb^{-1}")
h_recoJJ_tt.SetTitle(";mJJ (GeV); Events / bin / 20 fb^{-1}")
h_recoJJ_Z_1tau.SetTitle("Request 1 gen tau;mJJ (GeV); Events / bin / 20 fb^{-1}")
h_recoJJ_h_1tau.SetTitle("Request 1 gen tau;mJJ (GeV); Events / bin / 20 fb^{-1}")
h_recoJJ_tt_1tau.SetTitle("Request 1 gen tau;mJJ (GeV); Events / bin / 20 fb^{-1}")
h_recoJJ_Z_2tau.SetTitle("Request 2 gen taus;mJJ (GeV); Events / bin / 20 fb^{-1}")
h_recoJJ_h_2tau.SetTitle("Request 2 gen taus;mJJ (GeV); Events / bin / 20 fb^{-1}")
h_recoJJ_tt_2tau.SetTitle("Request 2 gen taus;mJJ (GeV); Events / bin / 20 fb^{-1}")

h_recoJJ_Z.GetYaxis().SetTitleOffset(1.2)
h_recoJJ_h.GetYaxis().SetTitleOffset(1.2)
h_recoJJ_tt.GetYaxis().SetTitleOffset(1.2)
h_recoJJ_Z_1tau.GetYaxis().SetTitleOffset(1.2)
h_recoJJ_h_1tau.GetYaxis().SetTitleOffset(1.2)
h_recoJJ_tt_1tau.GetYaxis().SetTitleOffset(1.2)

c = r.TCanvas("c","Test", 800, 600)
c.Divide(2,2)
#c.SetLogy()
ps = r.TPostScript(psfile,112)
ps.NewPage();
c.cd(1)
h_recoJJ_Z.Draw()
h_recoJJ_h.Draw("same")
l1.AddEntry(h_recoJJ_h,"reco jets matching h(125) -> bb")
l1.AddEntry(h_recoJJ_Z,"reco jets matching Z -> bb")
l1.Draw("same")
c.cd(2)
h_recoJJ_tt.Draw()
h_recoJJ_Z.Draw("same")
h_recoJJ_h.Draw("same")
l2.AddEntry(h_recoJJ_h,"reco jets matching h(125) -> bb (%s)" %(round(h_recoJJ_h.Integral(),2)))
l2.AddEntry(h_recoJJ_Z,"reco jets matching Z -> bb (%s)" %(round(h_recoJJ_Z.Integral(),2)))
l2.AddEntry(h_recoJJ_tt,"reco jets matching tt -> bb + tautau + nunu (%s)" %(round(h_recoJJ_tt.Integral(),2)))
l2.Draw("same")
c.cd(3)
h_recoJJ_tt_1tau.Draw()
h_recoJJ_Z_1tau.Draw("same")
h_recoJJ_h_1tau.Draw("same")
l3.AddEntry(h_recoJJ_h_1tau,"reco jets matching h(125) -> bb (%s)" %(round(h_recoJJ_h_1tau.Integral(),2)))
l3.AddEntry(h_recoJJ_Z_1tau,"reco jets matching Z -> bb (%s)" %(round(h_recoJJ_Z_1tau.Integral(),2)))
l3.AddEntry(h_recoJJ_tt_1tau,"reco jets matching tt -> bb + tautau + nunu (%s)" %(round(h_recoJJ_tt_1tau.Integral(),2)))
l3.Draw("same")
c.cd(4)
h_recoJJ_Z_2tau.Draw("same")
h_recoJJ_tt_2tau.Draw("same")
h_recoJJ_h_2tau.Draw("same")
l4.AddEntry(h_recoJJ_h_2tau,"reco jets matching h(125) -> bb (%s)" %(round(h_recoJJ_h_2tau.Integral(),2)))
l4.AddEntry(h_recoJJ_Z_2tau,"reco jets matching Z -> bb (%s)" %(round(h_recoJJ_Z_2tau.Integral(),2)))
l4.AddEntry(h_recoJJ_tt_2tau,"reco jets matching tt -> bb + tautau + nunu (%s)" %(round(h_recoJJ_tt_2tau.Integral(),2)))
l4.Draw("same")
ps.Close()
