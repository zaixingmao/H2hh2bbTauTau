#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="svEta"

Title = "Require "

signalEntries = enVars.signalEntries
ttEntries = enVars.ttEntries
ZZEntries = enVars.ZZEntries
signalLocation = enVars.signalLocation
ttLocation = enVars.ttLocation
ZZLocation = enVars.ZZLocation

CSVCut1 = -99999
CSVCut2 = -99999

if CSVCut1 == 0.679 and CSVCut2 < 0:
    Title = Title + "1 medium b tag"
    psfile = psfile + "_1_b_tag.eps"
if CSVCut1 == 0.679 and CSVCut2 == 0.679:
    Title = Title + "2 medium b tags"
    psfile = psfile + "_2_b_tag.eps"
if CSVCut1 < 0 and CSVCut2 < 0:
    Title = Title + "no b tags"
    psfile = psfile + "_no_b_tag.eps"

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******

iFileSig = r.TFile.Open("/scratch/zmao/H2hh260.root")
iFileBkg1 = r.TFile.Open("/scratch/zmao/tt.root")
iFileBkg2 = r.TFile.Open("/scratch/zmao/ZZ.root")
 

HTree = iFileSig.Get("eventTree")
ttTree = iFileBkg1.Get("eventTree")
ZZTree = iFileBkg2.Get("eventTree")

h_svEta_h = r.TH1F("h_svEta_h"," ", 40, -5.44392, 5.31255)
h_svEta_tt = r.TH1F("h_svEta_tt"," ", 40, -5.44392, 5.31255)
h_svEta_zz = r.TH1F("h_svEta_zz"," ", 40, -5.44392, 5.31255)
h_svEta_bkg = r.TH1F("h_svEta_bkg"," ", 40, -5.44392, 5.31255)

#for normalization
HistNameList = [h_svEta_h, h_svEta_bkg] #h_svEta_tt, h_svEta_zz]

HTree.Draw("svEta >> h_svEta_h", "fMass >= 50.0 && iso1<=1.5 && iso2<=1.5")
ttTree.Draw("svEta >> h_svEta_tt", "fMass >= 50.0 && iso1<=1.5 && iso2<=1.5")
ZZTree.Draw("svEta >> h_svEta_zz", "fMass >= 50.0 && iso1<=1.5 && iso2<=1.5")
ttTree.Draw("svEta >> h_svEta_bkg", "fMass >= 50.0 && iso1<=1.5 && iso2<=1.5")
ZZTree.Draw("svEta >> h_svEta_bkg", "fMass >= 50.0 && iso1<=1.5 && iso2<=1.5")

for iHist in HistNameList:
    for i in range(0, iHist.GetNbinsX()):
        iHist.SetBinError(i, r.sqrt(iHist.GetBinContent(i)))

intList = tool.unitNormHists(HistNameList)
            
legendPosition = (0.58, 0.78, 0.88, 0.88)
legendHistos1 = [(h_svEta_h,"H -> hh -> #tau^{+}#tau^{-} b#bar{b}"),#(%.2f events/20 fb^{-1})" %(intList[0]*xsList[0]*20/sigPreSelection)),
                (h_svEta_tt,"t#bar{t} -> b#bar{b} ll"), #(%.1f events/20 fb^{-1})" %(intList[1]*xsList[1]*20/ttPreSelection)),
                (h_svEta_zz,"ZZ + jets -> 2q 2l")]#(%.1f events/20 fb^{-1})" %(intList[2]*xsList[2]*20/ZZPreSelection))]

legendHistos1 = [(h_svEta_h,"H -> hh -> #tau^{+}#tau^{-} b#bar{b}"),
                (h_svEta_bkg,"background")]

h_svEta_h.SetTitle("%s; svEta; Unit Normalized" % (Title))
h_svEta_h.GetYaxis().SetTitleOffset(1.2)
h_svEta_bkg.SetTitle("%s; svEta; Unit Normalized" % (Title))
h_svEta_bkg.GetYaxis().SetTitleOffset(1.2)
c = r.TCanvas("c","Test", 800, 500)

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)
r.gPad.SetTickx()
r.gPad.SetTicky()
tool.setDraw2Hists(hist1=h_svEta_h, hist2=h_svEta_bkg, drawColor1=4, drawColor2=2, DrawOpt = 'E')
#tool.setDrawHists(sigHist=h_svEta_h, ttHist=h_svEta_tt, ZZHist=h_svEta_zz, DrawOpt = 'E')
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos1)
l1.Draw("same")
ps.Close()

print "Plot saved at %s" %(psfile)
