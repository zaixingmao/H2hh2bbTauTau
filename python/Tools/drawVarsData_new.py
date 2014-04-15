#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars
import varsList
import optparse

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--variable", dest="varName", default = 'mJJ', help="")
    parser.add_option("--option", dest="option", default = 'OS', help="")
    parser.add_option("--iso", dest="iso", default = 'tight', help="")
    parser.add_option("--signal", dest="signal", default = '', help="")
    parser.add_option("--logY", dest="logy", default = True, help="")
    parser.add_option("--sigBoost", dest="sigBoost", default = 1.0, help="")
    parser.add_option("--nbins", dest="nbins", default = 0, help="")
    parser.add_option("--useData", dest="useData", default = 'True', help="")
    parser.add_option("--setMax", dest="max", default = 50, help="")
    parser.add_option("--setRangeMin", dest="rangeMin", default = 0, help="")
    parser.add_option("--setRangeMax", dest="rangeMax", default = 100, help="")
    parser.add_option("--location", dest="location", default = '.', help="")


    options, args = parser.parse_args()
    return options


def passCut(tree, signSelection, iso):
    if tree.CSVJ1 > 0.679 and tree.CSVJ2 > 0.244 and abs(tree.eta1.at(0))<2.1 and abs(tree.eta2.at(0))<2.1:
        pass_cut = 1
        if iso == 'tight':
            if tree.iso2.at(0) > 1.5:
                pass_cut = 0
        elif iso == 'relaxed':
            if tree.iso2.at(0) < 1.5:
                pass_cut = 0

        if signSelection == 'SS':
            if tree.charge1.at(0) +  tree.charge2.at(0) == 0:
                pass_cut = 0
        elif signSelection == 'OS':
            if tree.charge1.at(0) -  tree.charge2.at(0) == 0:
                pass_cut = 0
        else:
            pass_cut = 0
        return pass_cut
    else:
        return 0

def getHistos(varName, signSelection, iso, signalSelection, logY, sigBoost, nbins, useData, max, rangeMin, rangeMax, location):
    r.gStyle.SetOptStat(0)
    fileList = [('ZZ', 'ZZ_eff_all.root', 2500, 5),
                ('tt_full_lep','tt_eff_all.root', 26197.5, r.kRed-7),
                ('tt_semi_lep','tt_semi_eff_all.root', 109281, r.kAzure+7),
                ('DYJetsToLL', 'DYJetsToLL_eff_all.root', 3504000, r.kGreen-7),
                ('W2JetsToLNu', 'W2JetsToLNu_eff_all.root', 1750000, r.kMagenta-9)]
    histList = []
    varRange = [nbins, rangeMin, rangeMax]
    Lumi = 18.0
    initNEventsList = []
    legendHistos = []
    var_background = r.THStack()

    tmpFile = []
    tmpTree = []
    for i in range(len(fileList)):
        histList.append(r.TH1F(fileList[i][0],"", varRange[0], varRange[1], varRange[2]))
        print 'Adding events from: %s ...' %(fileList[i][1])
        tmpFile.append(r.TFile(fileList[i][1]))
        tmpTree.append(tmpFile[i].Get('eventTree'))
        for iEntry in range(tmpTree[i].GetEntries()):
            tmpTree[i].GetEntry(iEntry)
            if not passCut(tmpTree[i], signSelection, iso):
                continue
            histList[i].Fill(varsList.findVar(tmpTree[i], varName), tmpTree[i].triggerEff)
    
        initNEventsList.append(tmpFile[i].Get('preselection'))
        histList[i].SetFillColor(fileList[i][3])
        histList[i].Scale(fileList[i][2]*Lumi/initNEventsList[i].GetBinContent(1))
        var_background.Add(histList[i])
        legendHistos.append((histList[i], '%s (%.2f)' %(fileList[i][0], histList[i].Integral())))

    if (signSelection == 'SS' or iso == 'relaxed') and useData == 'True':
        var_data = r.TH1F(fileList[i][0],"", varRange[0], varRange[1], varRange[2])
        fData = r.TFile('dataTotal_all.root')
        treeData = fData.Get('eventTree')
        print 'Adding events from: dataTotal_all.root ...'
        for iEntry in range(treeData.GetEntries()):
            treeData.GetEntry(iEntry)
            if not passCut(treeData, signSelection, iso):
                continue
            var_data.Fill(varsList.findVar(treeData, varName))
            var_data.SetMarkerStyle(8)
            var_data.SetMarkerSize(0.9)
            var_data.SetTitle('%s %s Events 1 Medium 1 Loose b-tag (%.1f fb^{-1}); %s; events / bin' %(signSelection, iso, Lumi, varName))

    DrawSignal = False
    if signalSelection != '':
        var_signal = r.TH1F(fileList[i][0],"", varRange[0], varRange[1], varRange[2])
        signalDict = {'H260': ('H2hh260_all.root', 14.76),
                      'H300': ('H2hh300_all.root', 15.9),
                      'H350': ('H2hh350_all.root', 8.57)}
        if signalSelection in signalDict:
            fSignal = r.TFile(signalDict[signalSelection][0])
            treeSignal = fSignal.Get('eventTree')
            print 'Adding events from: %s ...' %(signalDict[signalSelection][0])
            for iEntry in range(treeSignal.GetEntries()):
                treeSignal.GetEntry(iEntry)
                if not passCut(treeSignal, signSelection, iso):
                    continue
                var_signal.Fill(varsList.findVar(treeSignal, varName), treeSignal.triggerEff)
            var_signal.SetLineStyle(7)
            var_signal.SetLineWidth(4)
            initNEventsSignal = fSignal.Get('preselection')
            var_signal.Scale(signalDict[signalSelection][1]*sigBoost*Lumi/initNEventsSignal.GetBinContent(1))
            if sigBoost != 1:
                legendHistos.append((var_signal, '%sx%0.f (%.2f)' %(signalSelection, sigBoost, var_signal.Integral())))
            else:
                legendHistos.append((var_signal, '%s (%.2f)' %(signalSelection, var_signal.Integral())))
            DrawSignal = True
        else:
            print '%s not supported, please use H260, H300 or H350' %signalSelection

    legendPosition = (0.6, 0.7, 0.90, 0.88)

#     psfile = '%s/%s_combined_%s_%s.pdf' %(location, varName, signSelection, iso)
#     c = r.TCanvas("c","Test", 800, 600)
#     ps = r.TPDF(psfile,112)

#     if logY == True:
#         r.gPad.SetLogy()
    
    var_background.SetTitle('%s %s Events 1 Medium 1 Loose b-tag (%.1f fb^{-1}); %s; events / bin' %(signSelection, iso, Lumi,varName))

    drawOpt = ''

    if (signSelection == 'SS' or iso == 'relaxed') and useData == 'True':
        var_data.Draw('PE')
        var_data.SetMaximum(max)
        var_data.SetMinimum(0.01)
        drawOpt = 'same'

    var_background.Draw(drawOpt)
    var_background.SetMaximum(max)
    var_background.SetMinimum(0.01)

    if DrawSignal:
        var_signal.Draw('same')
    l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos)
    l1.Draw("same")

#     ps.Close()
# 
#     print "Plot saved at %s" %(psfile)

op = opts()
#getHistos(op.varName, op.option, op.iso, op.signal, op.logy, float(op.sigBoost), int(op.nbins),
#          op.useData, float(op.max), float(op.rangeMin), float(op.rangeMax), op.location)

