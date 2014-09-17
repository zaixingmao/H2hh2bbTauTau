#!/usr/bin/env python
import ROOT as r

Choose = 0

titles = ["H -> hh", "ZZ", "tt"]
Names = ["signal", "zz", "tt"]

title = titles[Choose]

psfile = Names[Choose] + "_pdg.eps"

#textPosition = [-10, 760, -8, 720, 80] #tt
textPosition = [-10, 2000, -8, 1900, 200] #h
#textPosition = [-10, 800, -8, 760, 80]  #zz
r.gStyle.SetOptStat(0)

ifile = r.TFile("/Users/zmao/M-Data/School/TempCode/analysis_%s.root" %(Names[Choose]))
tree = ifile.Get("ttTreeFinal/eventTree")
pdg_all = r.TH1F("pdg_all","",50, -25, 25)
pdg_all_full = r.TH1F("pdg_all_full","", 19998, -9999, 9999)
pdg_eleVeto1 = r.TH1F("pdg_eleVeto1","", 19998, -9999, 9999)
pdg_eleVeto2 = r.TH1F("pdg_eleVeto2","", 19998, -9999, 9999)
pdg_emVeto1 = r.TH1F("pdg_emVeto1","", 19998, -9999, 9999)
pdg_emVeto2 = r.TH1F("pdg_emVeto2","", 19998, -9999, 9999)

all = 0.
eleVeto1 = 0.
eleVeto2 = 0.
emVeto1 = 0.
emVeto2 = 0.
for i in range(0, tree.GetEntries()):
    tree.GetEntry(i)

    pdg_all.Fill(tree.pdg1)
    pdg_all_full.Fill(tree.pdg1)
    if abs(tree.pdg1) == 15:
        all+=1
    if tree.tauElectronLMVAPass1:
        pdg_eleVeto1.Fill(tree.pdg1)
        if abs(tree.pdg1) == 15:
            eleVeto1+=1
        if tree.tauElectronLMVAPass2:
            pdg_eleVeto2.Fill(tree.pdg1)
            if abs(tree.pdg1) == 15:
                eleVeto2+=1
        if tree.againstMuonLoose1:
            pdg_emVeto1.Fill(tree.pdg1)
            if abs(tree.pdg1) == 15:
                emVeto1+=1
            if tree.againstMuonLoose2 and tree.tauElectronLMVAPass2:
                pdg_emVeto2.Fill(tree.pdg1)
                if abs(tree.pdg1) == 15:
                    emVeto2+=1

ratio1 = pdg_eleVeto1.Integral()/pdg_all_full.Integral()*100
ratio2 = pdg_emVeto1.Integral()/pdg_all_full.Integral()*100
ratio3 = pdg_eleVeto2.Integral()/pdg_all_full.Integral()*100
ratio4 = pdg_emVeto2.Integral()/pdg_all_full.Integral()*100

sigRatio1 = eleVeto1/all*100
sigRatio2 = emVeto1/all*100
sigRatio3 = eleVeto2/all*100
sigRatio4 = emVeto2/all*100


pdg_all.SetTitle("%s; Leg1 Matched Gen PDG; " %(title))
pdg_eleVeto1.SetLineColor(2)
pdg_eleVeto1.SetLineStyle(2)
pdg_emVeto1.SetLineColor(2)
pdg_emVeto1.SetLineStyle(2)
pdg_eleVeto2.SetLineColor(2)
pdg_eleVeto2.SetLineStyle(2)
pdg_emVeto2.SetLineColor(2)
pdg_emVeto2.SetLineStyle(2)

text = r.TLatex()
text.SetTextFont(42)
text.SetTextSize(0.03)
c = r.TCanvas("c","Test", 1000, 800)
ps = r.TPostScript(psfile,112)
c.Divide(2,2)
c.cd(1)
pdg_all.Draw()
pdg_eleVeto1.SetFillStyle(3001)
pdg_eleVeto1.SetFillColor(2)
pdg_eleVeto1.Draw("same")
text.DrawLatex(textPosition[0], textPosition[1], "Signal (|pdg|=15) Remaining: %s" %(round(sigRatio1,1)) + "%")
text.DrawLatex(textPosition[2], textPosition[3], "Total Remaining: %s" %(round(ratio1,1)) + "%")
text.DrawLatex(textPosition[0]+5, textPosition[1] - textPosition[4], "EleLooseVeto on Leg1")
c.cd(2)
pdg_all.Draw()
pdg_emVeto1.SetFillStyle(3001)
pdg_emVeto1.SetFillColor(2)
pdg_emVeto1.Draw("same")
text.DrawLatex(textPosition[0], textPosition[1], "Signal (|pdg|=15) Remaining: %s" %(round(sigRatio2,1)) + "%")
text.DrawLatex(textPosition[2], textPosition[3], "Total Remaining: %s" %(round(ratio2,1)) + "%")
text.DrawLatex(textPosition[0]+4, textPosition[1] - textPosition[4], "EleMuLooseVeto on Leg1")
c.cd(3)
pdg_all.Draw()
pdg_eleVeto2.SetFillStyle(3001)
pdg_eleVeto2.SetFillColor(2)
pdg_eleVeto2.Draw("same")
text.DrawLatex(textPosition[0], textPosition[1], "Signal (|pdg|=15) Remaining: %s" %(round(sigRatio3,1)) + "%")
text.DrawLatex(textPosition[2], textPosition[3], "Total Remaining: %s" %(round(ratio3,1)) + "%")
text.DrawLatex(textPosition[0]+2, textPosition[1] - textPosition[4], "EleLooseVeto on Leg1 and Leg2")
c.cd(4)
pdg_all.Draw()
pdg_emVeto2.SetFillStyle(3001)
pdg_emVeto2.SetFillColor(2)
pdg_emVeto2.Draw("same")
text.DrawLatex(textPosition[0], textPosition[1], "Signal (|pdg|=15) Remaining: %s" %(round(sigRatio4,1)) + "%")
text.DrawLatex(textPosition[2], textPosition[3], "Total Remaining: %s" %(round(ratio4,1)) + "%")
text.DrawLatex(textPosition[0], textPosition[1] - textPosition[4], "EleMuLooseVeto on Leg1 and Leg2")

ps.Close()