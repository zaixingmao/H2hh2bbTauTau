#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******
BDT_1 = r.TH1F()
BDT_2 = r.TH1F()
BDT_3 = r.TH1F()
# 
# nBins = 10000000
# 
# eff_1 = r.TH1F("eff_1","BDT", nBins, 0, 0.99)
# eff_2 = r.TH1F("eff_2","BDT", nBins, 0, 0.99)
# eff_3 = r.TH1F("eff_3","BDT", nBins, 0, 0.99)

trainMass = '350'

oldStatsList = {'260': 6039, '300': 4708, '350': 12597, 'ZZ': 3978, 'tt': 22182}
statsList = {'260': 920, '300': 1066, '350': 3885, 'ZZ': 905, 'tt': 6910}
statsList = {'260': 5843, '300': 4651, '350': 12485, 'ZZ': 3902, 'tt': 21840}

psfile="BDT_%s.pdf" %(trainMass)

iFile_1 = r.TFile('/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/oldROOT/TMVA_H2hh%s_new.root' %(trainMass))
iFile_2 = r.TFile('/scratch/zmao/test_ptJet/TMVA%s_%s_new.root' %(trainMass, statsList[trainMass]))
#iFile_3 = r.TFile('/scratch/zmao/test_pt/TMVA%s_%i_old.root' %(trainMass, statsList[trainMass]))

BDT_1 = iFile_1.Get("Method_BDT/BDT/MVA_BDT_rejBvsS")
BDT_2 = iFile_2.Get("Method_BDT/BDT/MVA_BDT_rejBvsS")
#BDT_3 = iFile_3.Get("Method_BDT/BDT/MVA_BDT_rejBvsS")

legendPosition = (0.2, 0.4, 0.75, 0.5)
histList = [(BDT_1, '%s_old: %i events, tt %i events, ZZ %i events' %(trainMass, oldStatsList[trainMass], oldStatsList['tt'], oldStatsList['ZZ'])),
            (BDT_2, '%s_pt30Jet30: %i events, tt %i events, ZZ %i events' %(trainMass, statsList[trainMass], statsList['tt'], statsList['ZZ'])),
            ]#(BDT_3, '%s_old: %i events, tt %i events, ZZ %i events' %(trainMass, statsList[trainMass], statsList['tt'], statsList['ZZ']))]

BDT_1.SetLineWidth(2)
BDT_1.SetLineStyle(2)
BDT_1.SetLineColor(6)

BDT_2.SetLineWidth(2)
BDT_2.SetLineStyle(2)
BDT_2.SetLineColor(r.kBlue)

# BDT_3.SetLineWidth(2)
# BDT_3.SetLineColor(r.kBlue)
# BDT_3.SetLineStyle(2)

BDT_1.SetTitle("Background Rejection vs Signal Effeciency; Signal; Background Rejection")

#draw from the highest histogram


c = r.TCanvas("c","Test", 800, 600);
ps = r.TPDF(psfile,112);
r.gPad.SetGrid()
r.gPad.SetTickx()
r.gPad.SetTicky()

BDT_1.Draw()
BDT_2.Draw("same")
# BDT_3.Draw("same")

l = tool.setMyLegend(lPosition=legendPosition, lHistList=histList)
l.Draw("same")


ps.Close()
