#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars
import varsList

varName = 'mJJ'
bTag = True
if bTag:
    psfile="data_%s_btag_eff.pdf" %varName
else:
    psfile="data_%s_eff.pdf" %varName


r.gStyle.SetOptStat(0)

varRange = [25, 0., 500]

var1_data = r.TH1F("var1_data","", varRange[0], varRange[1], varRange[2])
var1_tt = r.TH1F("var1_tt","", varRange[0], varRange[1], varRange[2])
var1_ZZ= r.TH1F("var1_ZZ","", varRange[0], varRange[1], varRange[2])
var1_tt2 = r.TH1F("var1_tt2","", varRange[0], varRange[1], varRange[2])
var1_DYJets = r.TH1F("var1_DYJets","", varRange[0], varRange[1], varRange[2])
var1_W2JetsToLNu = r.TH1F("W2JetsToLNu","", varRange[0], varRange[1], varRange[2])
var1_signal = r.TH1F("var1_signal","", varRange[0], varRange[1], varRange[2])

var1_background = r.THStack()
# fData = r.TFile('dataTotal_all.root')
ftt = r.TFile('tt_eff_all.root')
fZZ = r.TFile('ZZ_eff_all.root')
ftt2 = r.TFile('tt_semi_eff_all.root')
fDYJets = r.TFile('DYJetsToLL_eff_all.root')
fW2JetsToLNu = r.TFile('W2JetsToLNu_eff_all.root')
fSignal = r.TFile('H2hh300_all.root')

# treeData = fData.Get('eventTree')
treett = ftt.Get('eventTree')
treett2 = ftt2.Get('eventTree')
treeZZ = fZZ.Get('eventTree')
treeDYJets = fDYJets.Get('eventTree')
treeW2JetsToLNu = fW2JetsToLNu.Get('eventTree')
treeSignal = fSignal.Get('eventTree')

for iEntry in range(treett.GetEntries()):
    treett.GetEntry(iEntry)
    if bTag and not (treett.CSVJ1 > 0.679 and treett.CSVJ2 > 0.244):
        continue
    if abs(treett.eta1.at(0))>2.1 or abs(treett.eta2.at(0))>2.1:
        continue
    var1_tt.Fill(varsList.findVar(iTree=treett, varName='mJJ'), treett.triggerEff)
    
for iEntry in range(treeZZ.GetEntries()):
    treeZZ.GetEntry(iEntry)
    if bTag and not (treeZZ.CSVJ1 > 0.679 and treeZZ.CSVJ2 > 0.244):
        continue
    if abs(treeZZ.eta1.at(0))>2.1 or abs(treeZZ.eta2.at(0))>2.1:
        continue
    var1_ZZ.Fill(treeZZ.mJJ, treeZZ.triggerEff)

for iEntry in range(treett2.GetEntries()):
    treett2.GetEntry(iEntry)
    if bTag and not (treett2.CSVJ1 > 0.679 and treett2.CSVJ2 > 0.244):
        continue
    if abs(treett2.eta1.at(0))>2.1 or abs(treett2.eta2.at(0))>2.1:
        continue
    var1_tt2.Fill(treett2.mJJ, treett2.triggerEff)

for iEntry in range(treeDYJets.GetEntries()):
    treeDYJets.GetEntry(iEntry)
    if bTag and not (treeDYJets.CSVJ1 > 0.679 and treeDYJets.CSVJ2 > 0.244):
        continue
    if abs(treeDYJets.eta1.at(0))>2.1 or abs(treeDYJets.eta2.at(0))>2.1:
        continue
    var1_DYJets.Fill(treeDYJets.mJJ, treeDYJets.triggerEff)

for iEntry in range(treeW2JetsToLNu.GetEntries()):
    treeW2JetsToLNu.GetEntry(iEntry)
    if bTag and not (treeW2JetsToLNu.CSVJ1 > 0.679 and treeW2JetsToLNu.CSVJ2 > 0.244):
        continue
    if abs(treeW2JetsToLNu.eta1.at(0))>2.1 or abs(treeW2JetsToLNu.eta2.at(0))>2.1:
        continue
    var1_W2JetsToLNu.Fill(treeW2JetsToLNu.mJJ, treeW2JetsToLNu.triggerEff)

for iEntry in range(treeSignal.GetEntries()):
    treeSignal.GetEntry(iEntry)
    if bTag and not (treeSignal.CSVJ1 > 0.679 and treeSignal.CSVJ2 > 0.244):
        continue
    if abs(treeSignal.eta1.at(0))>2.1 or abs(treeSignal.eta2.at(0))>2.1:
        continue
    var1_signal.Fill(treeSignal.mJJ, treeSignal.triggerEff)

# for iEntry in range(treeData.GetEntries()):
#     treeData.GetEntry(iEntry)
#     if bTag and not (treeData.CSVJ1 > 0.679 and treeData.CSVJ2 > 0.244):
#         continue
#     if abs(treeData.eta1.at(0))>2.1 or abs(treeData.eta2.at(0))>2.1:
#         continue
#     var1_data.Fill(treeData.mJJ)
#     if treeData.charge1.at(0) != treeData.charge2.at(0):
#         print 'not same sign!!!'


scale1_tt = ftt.Get('preselection')
scale1_tt2 = ftt2.Get('preselection')
scale1_ZZ = fZZ.Get('preselection')
scale1_DYJets = fDYJets.Get('preselection')
scale1_W2JetsToLNu = fW2JetsToLNu.Get('preselection')
scale1_signal = fSignal.Get('preselection')


var1_data.SetMarkerStyle(8)
var1_data.SetMarkerSize(0.9)
var1_tt.SetFillColor(r.kRed-7)
var1_ZZ.SetFillColor(5)
var1_tt2.SetFillColor(r.kAzure+7)
var1_DYJets.SetFillColor(r.kGreen-7)
var1_W2JetsToLNu.SetFillColor(r.kMagenta-9)

#Scaling
var1_tt.Scale(26197.5*18/scale1_tt.GetBinContent(1))
var1_tt2.Scale(109281 *18/scale1_tt2.GetBinContent(1))
var1_ZZ.Scale(2500 *18/scale1_ZZ.GetBinContent(1))
var1_DYJets.Scale(3504000 *18/scale1_DYJets.GetBinContent(1))
var1_W2JetsToLNu.Scale(1750000 *18/scale1_W2JetsToLNu.GetBinContent(1))
var1_signal.Scale(15.9*18/scale1_signal.GetBinContent(1))

var1_background.Add(var1_ZZ)
var1_background.Add(var1_tt)
var1_background.Add(var1_DYJets)
var1_background.Add(var1_tt2)
var1_background.Add(var1_W2JetsToLNu)


legendPosition = (0.7, 0.7, 0.90, 0.88)
legendHistos1 = [#(var1_data,"data (2012)"),#(%.2f events/20 fb^{-1})" %(intList[0]*xsList[0]*20/sigPreSelection)),
                (var1_tt,"t#bar{t} full lep"), #(%.1f events/20 fb^{-1})" %(intList[1]*xsList[1]*20/ttPreSelection)),
                (var1_tt2,"t#bar{t} semi lep"),
                (var1_ZZ,"ZZJetsTo2L2Q"),
                (var1_DYJets, 'DYJetsToLL'),
                (var1_W2JetsToLNu, 'W2JetsToLNu'),
                (var1_signal, 'H2hh300'),
                ]

ps = r.TPDF(psfile,112)
c = r.TCanvas("c","Test", 800, 600)
r.gPad.SetLogy()
if bTag:
    var1_data.SetTitle('Same Sign Events 1 Medium 1 Loose b-tag (18 fb^{-1}); %s; events / 20 GeV' %varName)
    var1_background.SetTitle('Same Sign Events 1 Medium 1 Loose b-tag (18 fb^{-1}); %s; events / 20 GeV' %varName)
else:
    var1_data.SetTitle('Same Sign Events (18 fb^{-1}); %s; events / 20 GeV' %varName)
    var1_background.SetTitle('Same Sign Events (18 fb^{-1}); %s; events / 20 GeV' %varName)
# var1_data.Draw('PE')
# var1_data.SetMaximum(1000)
# var1_data.SetMinimum(0.001)
var1_background.Draw()
var1_background.SetMaximum(500)
var1_background.SetMinimum(0.0035)
var1_signal.SetLineStyle(7)
var1_signal.SetLineWidth(4)
var1_signal.Draw('same')
var1_signal.SetMaximum(1000)
var1_signal.SetMinimum(0.001)
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos1)
l1.Draw("same")

ps.Close()

print "Plot saved at %s" %(psfile)
