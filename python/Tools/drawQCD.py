#!/usr/bin/env python

import ROOT as r
import tool
import varsList
from array import array

def bTagSelection(tree, bTag):
    passCut = 0        
    if bTag == 'True' and tree.CSVJ1 >= 0.68 and tree.CSVJ2 >= 0.24:
        passCut = 1
    if bTag == 'False':
        passCut = 1
    if bTag == 'Revert' and (tree.CSVJ1 < 0.68 and tree.CSVJ2 < 0.24):
        passCut = 1
    if bTag == 'Loose' and (tree.CSVJ1 >= 0.24 and tree.CSVJ2 >= 0.24):
        passCut = 1
    return passCut

varName = 'relaxPt'
bTag = 'False'

file = r.TFile('/scratch/zmao/QCD/QCDtotal_all.root')
tree = file.Get('eventTree')
r.gStyle.SetOptStat(0)

ptBins = [0, 80, 140, 400]
bins = array('f', ptBins)

ss = r.TH1F('ss','', len(ptBins)-1, bins)
os = r.TH1F('os','', len(ptBins)-1, bins)
plus = r.TH1F('plus','', len(ptBins)-1, bins)
minus = r.TH1F('minus','', len(ptBins)-1, bins)
plus2 = r.TH1F('plus2','', len(ptBins)-1, bins)
minus2 = r.TH1F('minus2','', len(ptBins)-1, bins)

nEntries = tree.GetEntries()

for iEntry in range(nEntries):
    tree.GetEntry(iEntry)
    passCut = bTagSelection(tree, bTag)
    if not passCut:
        continue
    if tree.iso1.at(0) < 1.5 and tree.iso2.at(0) < 1.5:
        continue
    if tree.charge1.at(0) == tree.charge2.at(0):
        ss.Fill(varsList.findVar(tree, varName))
    if tree.charge1.at(0) == -tree.charge2.at(0):
        os.Fill(varsList.findVar(tree, varName))
    if tree.charge1.at(0) > 0:
        plus.Fill(varsList.findVar(tree, varName))
    if tree.charge1.at(0) < 0:
        minus.Fill(varsList.findVar(tree, varName))
    if tree.charge2.at(0) > 0:
        plus2.Fill(varsList.findVar(tree, varName))
    if tree.charge2.at(0) < 0:
        minus2.Fill(varsList.findVar(tree, varName))

ss.Sumw2()
os.Sumw2()
minus.Sumw2()
plus.Sumw2()
minus2.Sumw2()
plus2.Sumw2()
ratio = os.Clone()
ratio.Divide(ss)
ratio.SetMarkerStyle(8)
ratio.SetMarkerSize(0.9)

chargeRatio = plus.Clone()
chargeRatio.Divide(minus)
chargeRatio.SetMarkerStyle(8)
chargeRatio.SetMarkerSize(0.9)
chargeRatio2 = plus2.Clone()
chargeRatio2.Divide(minus2)
chargeRatio2.SetMarkerStyle(8)
chargeRatio2.SetMarkerSize(0.9)
chargeRatio2.SetMarkerColor(r.kRed)


c = r.TCanvas("c","Test", 800, 600)
c.Divide(2,2)
c.cd(1)
ss.SetMarkerStyle(8)
ss.SetMarkerSize(0.9)
ss.SetTitle('Same Sign QCD Events; %s; '%varName)
ss.Draw('PE')
c.cd(2)
os.SetMarkerStyle(8)
os.SetMarkerSize(0.9)
os.SetTitle('Opposite Sign QCD Events; %s; ' %varName)
os.Draw('PE')
c.cd(3)
ratio.SetTitle('Opposite Sign / Same Sign Ratio; %s; OS/SS' %varName)
ratio.Draw('PE')


flErr = r.TGraph(4)
flErr.SetPoint(0, ptBins[0],ratio.GetBinContent(1)+ratio.GetBinError(1))
flErr.SetPoint(3, ptBins[0],ratio.GetBinContent(1)-ratio.GetBinError(1))
flErr.SetPoint(1, ptBins[1],ratio.GetBinContent(1)+ratio.GetBinError(1))
flErr.SetPoint(2, ptBins[1],ratio.GetBinContent(1)-ratio.GetBinError(1))
flErr.SetFillStyle(3001)
flErr.SetFillColor(r.kRed)
fmErr = r.TGraph(4)
fmErr.SetPoint(0, ptBins[1],ratio.GetBinContent(2)+ratio.GetBinError(2))
fmErr.SetPoint(3, ptBins[1],ratio.GetBinContent(2)-ratio.GetBinError(2))
fmErr.SetPoint(1, ptBins[2],ratio.GetBinContent(2)+ratio.GetBinError(2))
fmErr.SetPoint(2, ptBins[2],ratio.GetBinContent(2)-ratio.GetBinError(2))
fmErr.SetFillStyle(3001)
fmErr.SetFillColor(r.kBlue)
fhErr = r.TGraph(4)
fhErr.SetPoint(0, ptBins[2],ratio.GetBinContent(3)+ratio.GetBinError(3))
fhErr.SetPoint(3, ptBins[2],ratio.GetBinContent(3)-ratio.GetBinError(3))
fhErr.SetPoint(1, ptBins[3],ratio.GetBinContent(3)+ratio.GetBinError(3))
fhErr.SetPoint(2, ptBins[3],ratio.GetBinContent(3)-ratio.GetBinError(3))
fhErr.SetFillStyle(3001)
fhErr.SetFillColor(r.kGreen)
flErr.Draw('fsame')
fmErr.Draw('fsame')
fhErr.Draw('fsame')
lFit1 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(flErr,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(ratio.GetBinContent(1), ratio.GetBinError(1))),
                                                 (fmErr,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(ratio.GetBinContent(2), ratio.GetBinError(2))),
                                                 (fhErr,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(ratio.GetBinContent(3), ratio.GetBinError(3)))])
lFit1.Draw('same')

c.cd(4)
chargeRatio.SetTitle('+ / - Ratio; %s; +/-' %varName)
chargeRatio.SetMaximum(2.5)
chargeRatio.Draw('PE')
lFit2 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(chargeRatio,'Scale between +/- in relaxed region: %.2f \pm %.2f' %(chargeRatio.GetBinContent(1), chargeRatio.GetBinError(1))),
                                                 (chargeRatio,'Scale between +/- in relaxed region: %.2f \pm %.2f' %(chargeRatio.GetBinContent(2), chargeRatio.GetBinError(2))),
                                                 (chargeRatio,'Scale between +/- in relaxed region: %.2f \pm %.2f' %(chargeRatio.GetBinContent(3), chargeRatio.GetBinError(3)))])

lFit2.Draw('same')
# chargeRatio2.Draw('samePE')
c.Update()
c.Print('QCDratio_%s_%s.pdf' %(bTag,varName))