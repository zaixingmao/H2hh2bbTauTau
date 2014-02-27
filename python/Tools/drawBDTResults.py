#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******


nBins = 100

eff_1 = r.TH1F("eff_1","BDT", nBins, 0, 1)
eff_2 = r.TH1F("eff_2","BDT", nBins, 0, 1)
eff_3 = r.TH1F("eff_3","BDT", nBins, 0, 1)

trainMass = '350'

psfile="BDT_test_%s.eps" %(trainMass)

iFile_1 = r.TFile('/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVA_%s.root' %(trainMass))
iFile_2 = r.TFile('/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVA_%s_noFullMass.root' %(trainMass))

eff_1 = iFile_1.Get("Method_BDT/BDT/MVA_BDT_rejBvsS")
eff_2 = iFile_2.Get("Method_BDT/BDT/MVA_BDT_rejBvsS")

legendPosition = (0.7, 0.75, 0.95, 0.85)


histList2 = [(eff_1, 'H260 with fMass'),
            (eff_2, 'H260 without fMass')]


eff_1.SetLineColor(r.kBlue)
eff_2.SetLineColor(r.kRed)
eff_1.SetLineStyle(2)
eff_2.SetLineStyle(2)
#eff_3.SetLineColor(r.kBlue)


#draw from the highest histogram


c = r.TCanvas("c","Test", 800, 600);
ps = r.TPostScript(psfile,112);
r.gPad.SetTickx()
r.gPad.SetTicky()

r.gPad.SetGrid()

eff_1.SetMaximum(1.05);
eff_1.SetTitle("Background rejection versus Signal efficiency; Signal efficiency; Background rejection")
eff_1.Draw("")
eff_2.Draw("same")
#eff_3.Draw("sameP")
l = tool.setMyLegend(lPosition=(0.2,0.35,0.5,0.45), lHistList=histList2)
l.Draw("same")

ps.Close()

print "Plot saved at: %s" %(psfile)