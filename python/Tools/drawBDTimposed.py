#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******
BDT_bkg = r.TH1F("BDT_bkg","BDT", 100, -0.8, 0.8)
BDT_1 = r.TH1F("BDT_1","BDT", 100, -0.8, 0.8)
BDT_2 = r.TH1F("BDT_2","BDT", 100, -0.8, 0.8)
BDT_3 = r.TH1F("BDT_3","BDT", 100, -0.8, 0.8)

nBins = 10000000

eff_1 = r.TH1F("eff_1","BDT", nBins, 0, 0.99)
eff_2 = r.TH1F("eff_2","BDT", nBins, 0, 0.99)
eff_3 = r.TH1F("eff_3","BDT", nBins, 0, 0.99)

trainMass = 'H260'

psfile="BDT_%s.eps" %(trainMass)


iFile_bkg = r.TFile('/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVApp_%s_bkg.root' %(trainMass))
iFile_1 = r.TFile('/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVApp_%s_sig260.root' %(trainMass))
iFile_2 = r.TFile('/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVApp_%s_sig300.root' %(trainMass))
iFile_3 = r.TFile('/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVApp_%s_sig350.root' %(trainMass))

BDT_bkg = iFile_bkg.Get("MVA_BDT")
BDT_1 = iFile_1.Get("MVA_BDT")
BDT_2 = iFile_2.Get("MVA_BDT")
BDT_3 = iFile_3.Get("MVA_BDT")

legendPosition = (0.7, 0.75, 0.95, 0.85)
histList = [(BDT_bkg, 'background'),
            (BDT_1, 'H260'),
            (BDT_2, 'H300'),
            (BDT_3, 'H350')]
histList2 = [(eff_1, 'H260'),
            (eff_2, 'H300'),
            (eff_3, 'H350')]

BDT_bkg.SetLineWidth(2)
BDT_bkg.SetFillStyle(3006)
BDT_bkg.SetFillColor(2)
BDT_bkg.SetLineColor(2)

BDT_1.SetLineWidth(2)
BDT_1.SetLineStyle(2)
BDT_1.SetLineColor(6)
eff_1.SetLineColor(6)

BDT_2.SetLineWidth(2)
BDT_2.SetLineStyle(2)
BDT_2.SetLineColor(8)
eff_2.SetLineColor(8)

BDT_3.SetLineWidth(2)
BDT_3.SetLineColor(r.kBlue)
BDT_3.SetLineStyle(2)
eff_3.SetLineColor(r.kBlue)

tool.unitNormHists([BDT_bkg, BDT_1, BDT_2, BDT_3])

HistMaxList=[(BDT_bkg.GetMaximum(), BDT_bkg),
             (BDT_1.GetMaximum(), BDT_1),
             (BDT_2.GetMaximum(), BDT_2),
             (BDT_3.GetMaximum(), BDT_3)]
HistMaxList = sorted(HistMaxList, key=itemgetter(0), reverse=True)
HistMaxList[0][1].SetTitle("BDT training at %s; BDT; " %(trainMass))

#draw from the highest histogram


c = r.TCanvas("c","Test", 800, 600);
ps = r.TPostScript(psfile,112);
r.gPad.SetTickx()
r.gPad.SetTicky()

ps.NewPage()
HistMaxList[0][1].Draw()
HistMaxList[1][1].Draw("same")
HistMaxList[2][1].Draw("same")
HistMaxList[3][1].Draw("same")
l = tool.setMyLegend(lPosition=legendPosition, lHistList=histList)
l.Draw("same")
c.Update()
ps.NewPage()
c.cd()
r.gPad.SetGrid()
for i in range(49):
    bkgRejection = 1 - BDT_bkg.Integral(98-i*2,99)
    sigEff1 = BDT_1.Integral(98-i*2,99)
    sigEff2 = BDT_2.Integral(98-i*2,99)
    sigEff3 = BDT_3.Integral(98-i*2,99)
    if bkgRejection == 1.0 or sigEff1 >= 1.0 or sigEff2 >= 1.0 or sigEff3 >= 1.0:
        continue
    
    eff_1.Fill(sigEff1, bkgRejection)
    eff_2.Fill(sigEff2, bkgRejection)
    eff_3.Fill(sigEff3, bkgRejection)

eff_1.SetMaximum(1.0);
eff_1.SetTitle("Background rejection versus Signal efficiency; Signal efficiency; Background rejection")
eff_1.Draw("P")
eff_2.Draw("sameP")
eff_3.Draw("sameP")
l = tool.setMyLegend(lPosition=(0.2,0.35,0.5,0.45), lHistList=histList2)
l.Draw("same")

ps.Close()
