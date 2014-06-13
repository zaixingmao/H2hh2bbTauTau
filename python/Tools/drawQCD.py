#!/usr/bin/env python

import ROOT as r
import tool
import varsList


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

varName = 'tightPt'
bTag = 'False'

file = r.TFile('/scratch/zmao/QCD/QCDtotal_all.root')
tree = file.Get('eventTree')
r.gStyle.SetOptStat(0)

ss = r.TH1F('ss','', 20, 0, 400)
os = r.TH1F('os','', 20, 0, 400)
plus = r.TH1F('plus','', 20, 0, 400)
minus = r.TH1F('minus','', 20, 0, 400)
plus2 = r.TH1F('plus2','', 20, 0, 400)
minus2 = r.TH1F('minus2','', 20, 0, 400)

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


ptBins = [0, 80, 140, 400]
fit_l = r.TF1("fit_l","[0]", ptBins[0], ptBins[1])
fit_l.SetLineColor(r.kRed)
fit_l.SetLineStyle(2)
fit_m = r.TF1("fit_m","[0]", ptBins[1], ptBins[2])
fit_m.SetLineColor(r.kBlue)
fit_m.SetLineStyle(2)
fit_h = r.TF1("fit_h","[0]", ptBins[2], ptBins[3])
fit_h.SetLineColor(r.kGreen)
fit_h.SetLineStyle(2)

fit_l2 = r.TF1("fit_l2","[0]", ptBins[0], ptBins[1])
fit_l2.SetLineColor(r.kRed)
fit_l2.SetLineStyle(2)
fit_m2 = r.TF1("fit_m2","[0]", ptBins[1], ptBins[2])
fit_m2.SetLineColor(r.kBlue)
fit_m2.SetLineStyle(2)
fit_h2 = r.TF1("fit_h2","[0]", ptBins[2], ptBins[3])
fit_h2.SetLineColor(r.kGreen)
fit_h2.SetLineStyle(2)

chargeRatio.Fit('fit_l2', '0ER')
chargeRatio.Fit('fit_m2', '0ER')
chargeRatio.Fit('fit_h2', '0ER')

ratio.Fit('fit_l', '0ER')
ratio.Fit('fit_m', '0ER')
ratio.Fit('fit_h', '0ER')

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
lFit1 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fit_l,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(fit_l.GetParameter(0), fit_l.GetParError(0))),
                                                 (fit_m,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(fit_m.GetParameter(0), fit_m.GetParError(0))),
                                                 (fit_h,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(fit_h.GetParameter(0), fit_h.GetParError(0)))])
ratio.SetTitle('Opposite Sign / Same Sign Ratio; %s; OS/SS' %varName)
ratio.Draw('PE')
fit_l.Draw('same')
fit_m.Draw('same')
fit_h.Draw('same')
lFit1.Draw('same')
flErr = r.TGraph(4)
flErr.SetPoint(0, ptBins[0],fit_l.GetParameter(0)+fit_l.GetParError(0))
flErr.SetPoint(3, ptBins[0],fit_l.GetParameter(0)-fit_l.GetParError(0))
flErr.SetPoint(1, ptBins[1],fit_l.GetParameter(0)+fit_l.GetParError(0))
flErr.SetPoint(2, ptBins[1],fit_l.GetParameter(0)-fit_l.GetParError(0))
flErr.SetFillStyle(3001)
flErr.SetFillColor(r.kRed)
fmErr = r.TGraph(4)
fmErr.SetPoint(0, ptBins[1],fit_m.GetParameter(0)+fit_m.GetParError(0))
fmErr.SetPoint(3, ptBins[1],fit_m.GetParameter(0)-fit_m.GetParError(0))
fmErr.SetPoint(1, ptBins[2],fit_m.GetParameter(0)+fit_m.GetParError(0))
fmErr.SetPoint(2, ptBins[2],fit_m.GetParameter(0)-fit_m.GetParError(0))
fmErr.SetFillStyle(3001)
fmErr.SetFillColor(r.kBlue)
fhErr = r.TGraph(4)
fhErr.SetPoint(0, ptBins[2],fit_h.GetParameter(0)+fit_h.GetParError(0))
fhErr.SetPoint(3, ptBins[2],fit_h.GetParameter(0)-fit_h.GetParError(0))
fhErr.SetPoint(1, ptBins[3],fit_h.GetParameter(0)+fit_h.GetParError(0))
fhErr.SetPoint(2, ptBins[3],fit_h.GetParameter(0)-fit_h.GetParError(0))
fhErr.SetFillStyle(3001)
fhErr.SetFillColor(r.kGreen)
flErr.Draw('fsame')
fmErr.Draw('fsame')
fhErr.Draw('fsame')

c.cd(4)
chargeRatio.SetTitle('+ / - Ratio; %s; +/-' %varName)
chargeRatio.SetMaximum(2.5)
chargeRatio.Draw('PE')
lFit2 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fit_l2,'Scale between +/- in relaxed region: %.2f \pm %.2f' %(fit_l2.GetParameter(0), fit_l.GetParError(0))),
                                                 (fit_m2,'Scale between +/- in relaxed region: %.2f \pm %.2f' %(fit_m2.GetParameter(0), fit_m.GetParError(0))),
                                                 (fit_h2,'Scale between +/- in relaxed region: %.2f \pm %.2f' %(fit_h2.GetParameter(0), fit_h.GetParError(0)))])
fit_l2.Draw('same')
fit_m2.Draw('same')
fit_h2.Draw('same')
lFit2.Draw('same')
# chargeRatio2.Draw('samePE')
c.Update()
c.Print('QCDratio_%s_%s.pdf' %(bTag,varName))