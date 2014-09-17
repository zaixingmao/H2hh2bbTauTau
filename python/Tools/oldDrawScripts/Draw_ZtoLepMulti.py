#!/usr/bin/env python

import ROOT as r
import tool

psfile="ZtoLepMulti.eps"



r.gStyle.SetOptStat(0)
#*******Open input file and find associated tree*******
ifile = [r.TFile("/Users/zmao/M-Data/School/TempCode/1DiTau.root"),
         r.TFile("/Users/zmao/M-Data/School/TempCode/1DiTau_PtEta1.root"),
         r.TFile("/Users/zmao/M-Data/School/TempCode/1DiTau_PtEta1_PtEta2.root"),
         r.TFile("/Users/zmao/M-Data/School/TempCode/1DiTau_PtEta1_PtEta2_OS.root"),
         ]

plotsNames = ["1 DiTau" , "1 DiTau + PtEtaCut1", "1 DiTau + PtEtaCut1 + PtEtaCut2", "1 DiTau + PtEtaCut1 + PtEtaCut2 + OC"]
ZtoTau = [r.TH1F("ZtoTau"," ", 3, -0.5, 2.5), r.TH1F("ZtoTau"," ", 3, -0.5, 2.5),
          r.TH1F("ZtoTau"," ", 3, -0.5, 2.5), r.TH1F("ZtoTau"," ", 3, -0.5, 2.5)]
ZtoEle = [r.TH1F("ZtoEle"," ", 3, -0.5, 2.5), r.TH1F("ZtoEle"," ", 3, -0.5, 2.5),
          r.TH1F("ZtoEle"," ", 3, -0.5, 2.5), r.TH1F("ZtoEle"," ", 3, -0.5, 2.5)]
ZtoMu = [r.TH1F("ZtoMu"," ", 3, -0.5, 2.5), r.TH1F("ZtoMu"," ", 3, -0.5, 2.5),
         r.TH1F("ZtoMu"," ", 3, -0.5, 2.5), r.TH1F("ZtoMu"," ", 3, -0.5, 2.5)]

legendPosition = (0.65, 0.7, 0.93, 0.85)

l1 = [r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3]),
      r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3]),
      r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3]),
      r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])]

c = r.TCanvas("c","Test", 800, 600)
c.Divide(2,2)
ps = r.TPostScript(psfile,112)
ps.NewPage()

for j in range(0, len(ifile)):
    tree = ifile[j].Get("ttTreeFinal/eventTree")

    for i in range(0, tree.GetEntries()):
        tree.GetEntry(i)
        ZtoTau[j].Fill(tree.genK0toTauPt.size())
        ZtoEle[j].Fill(tree.genK0toElePt.size())
        ZtoMu[j].Fill(tree.genK0toMuPt.size())

    l1[j].SetFillStyle(0)
    l1[j].SetBorderSize(0)
 
    ZtoTau[j].SetTitle("%s; Z to lepton multiplicity; Events" %(plotsNames[j]))
    ZtoTau[j].GetYaxis().SetTitleOffset(1.2)

    c.cd(j+1)
    l1[j].AddEntry(ZtoTau[j],"Z -> tau")
    l1[j].AddEntry(ZtoEle[j],"Z -> e")
    l1[j].AddEntry(ZtoMu[j],"Z -> mu")

    ZtoTau[j].SetFillStyle(3001)
    ZtoTau[j].SetFillColor(4)
    ZtoTau[j].SetLineWidth(2)
    ZtoTau[j].Draw()

    ZtoEle[j].SetLineWidth(2)
    ZtoEle[j].SetLineColor(2)
    ZtoEle[j].SetFillStyle(3001)
    ZtoEle[j].SetFillColor(2)
    ZtoEle[j].Draw("same")

    ZtoMu[j].SetLineColor(1)
    ZtoMu[j].SetLineWidth(2)
    ZtoMu[j].SetLineStyle(2)
    ZtoMu[j].Draw("same")
    ZtoTau[j].Draw("same")
    l1[j].Draw("same")
    c.Update()

ps.Close()
