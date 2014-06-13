#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars
import varsList
import optparse
import math
from array import array
import numpy

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--variable", dest="varName", default = 'test', help="")
    parser.add_option("--signal", dest="signal", default = '', help="")
    parser.add_option("--logY", dest="logy", default = True, help="")
    parser.add_option("--sigBoost", dest="sigBoost", default = 1.0, help="")
    parser.add_option("--nbins", dest="nbins", default = 0, help="")
    parser.add_option("--useData", dest="useData", default = 'True', help="")
    parser.add_option("--setMax", dest="max", default = 50, help="")
    parser.add_option("--setRangeMin", dest="rangeMin", default = 0, help="")
    parser.add_option("--setRangeMax", dest="rangeMax", default = 100, help="")
    parser.add_option("--location", dest="location", default = '.', help="")
    parser.add_option("--bTag", dest="bTag", default = 'True', help="")
    parser.add_option("--predict", dest="predict", default = 'False', help="")

    options, args = parser.parse_args()
    return options

def conditions(selection):
    if selection == 1:
        return 'OS', 'tight'
    elif selection == 2:
        return 'SS', 'tight'
    elif selection == 3:
        return 'OS', 'relaxed'
    elif selection == 4:
        return 'SS', 'relaxed'

def getCombinedError(x, x_e, y, y_e):
    if x != 0:
        x_part = math.pow(x_e/x,2)
    else:
        x_part = 0
    if x_e == 0:
        return 0
    if y != 0:
        y_part = math.pow(y_e/y,2)
    else:
        y_part = 0
    return math.sqrt(x_part + y_part)

def bTagSelection(tree, bTag):
    passCut = 0
    if bTag == 'True' and tree.CSVJ1 >= 0.68 and tree.CSVJ2 >= 0.24:
        passCut = 1
    if bTag == 'False':
        passCut = 1
    if bTag == 'Revert' and (tree.CSVJ1 < 0.68 and tree.CSVJ2 < 0.24):
        passCut = 1
    return passCut

def passCut(tree, bTag):
    if bTagSelection(tree, bTag) and abs(tree.eta1.at(0))<2.1 and abs(tree.eta2.at(0))<2.1:
        iso_count = 0
        sign_count = 0
        if tree.iso1.at(0) > 1.5 or tree.iso2.at(0) > 1.5:
            iso_count = 1
        if tree.charge1.at(0) -  tree.charge2.at(0) == 0:
            sign_count = 1
        return (iso_count<<1) + sign_count + 1
    else:
        return 0

def findBin(x, nBins, xMin, xMax):
    bin =  int(nBins*(x-xMin)/(xMax-xMin))
    if bin >= nBins:
        return nBins-1
    else:
        return bin

def estBkg2(MC, data, backgroundHist, scale):
    for i in range(data.GetNbinsX()):
        for j in range(data.GetNbinsX()):
            currentValue = backgroundHist.GetBinContent(i+1, j+1)
            backgroundHist.SetBinContent(i+1, j+1, (data.GetBinContent(i+1, j+1)-MC.GetBinContent(i+1, j+1))*scale + currentValue)
    return backgroundHist

def add2DHist(hist1, hist2, nBins):
    for i in range(nBins):
        for j in range(nBins):
            hist1.Fill(hist2.GetBinContent(i,j))
    return hist1

def getHistos(signalSelection, sigBoost, location, bTag):
    r.gStyle.SetOptStat(0)
    preFix = 'ClassApp_both_ClassApp_QCD_ClassApp_EWK_TMVARegApp_'

    fileList = [('ZZ', preFix + 'ZZ_eff_all.root', 2500, 5, r.kYellow),
                ('tt_full_lep',preFix+'tt_eff_all.root', 26197.5, r.kRed-7),
                ('tt_semi_lep',preFix+'tt_semi_eff_all.root', 109281, r.kAzure+7),
#                 ('DYJetsToLL', 'DYJetsToLL_eff_all.root', 3504000, r.kGreen-7),
                ('DY2JetsToLL', preFix+'DY2JetsToLL_eff_all.root', 181000, r.kGreen-7),
                ('DY3JetsToLL', preFix+'DY3JetsToLL_eff_all.root', 51100, r.kGreen-7),
                ('W1JetsToLNu', preFix+'W1JetsToLNu_eff_all.root', 5400000, r.kMagenta-9),
                ('W2JetsToLNu', preFix+'W2JetsToLNu_eff_all.root', 1750000, r.kMagenta-9),
                ('W3JetsToLNu', preFix+'W3JetsToLNu_eff_all.root', 519000, r.kMagenta-9)]
    histList = []
    QCDHistList = []
    varRange = [20, -1, 1, 20, -1, 1]
    Lumi = 19.0
    initNEventsList = []
    legendHistos = []

    tmpFile = []
    tmpTree = []
    var_data = []
    signal = r.TH2F('signal',"", varRange[0], varRange[1], varRange[2], varRange[0], varRange[1], varRange[2])
    EWK = r.TH2F('EWK',"", varRange[0], varRange[1], varRange[2], varRange[0], varRange[1], varRange[2])
    QCD = r.TH2F('QCD',"", varRange[0], varRange[1], varRange[2], varRange[0], varRange[1], varRange[2])
    data = r.TH2F('data',"", varRange[0], varRange[1], varRange[2], varRange[0], varRange[1], varRange[2])
    MC = r.TH2F('MC',"", varRange[0], varRange[1], varRange[2], varRange[0], varRange[1], varRange[2])

    background = r.TH2F('background',"", varRange[0], varRange[1], varRange[2], varRange[0], varRange[1], varRange[2])
    dataName = preFix + 'dataTotal_all.root'
    fData = r.TFile(dataName)
    treeData = fData.Get('eventTree')
    print 'Adding events from: %s ...' %dataName
    for iEntry in range(treeData.GetEntries()):
        treeData.GetEntry(iEntry)
        select = passCut(treeData, bTag)
        if select == 3:
            data.Fill(varsList.findVar(treeData, 'BDT_EWK'), varsList.findVar(treeData, 'BDT_QCD'))

    for i in range(len(fileList)):
        print 'Adding events from: %s ...' %(fileList[i][1])
        tmpFile.append(r.TFile(fileList[i][1]))
        tmpTree.append(tmpFile[i].Get('eventTree'))
        initNEventsList.append(tmpFile[i].Get('preselection'))
        tmpScale = fileList[i][2]*Lumi/initNEventsList[i].GetBinContent(1)
        for iEntry in range(tmpTree[i].GetEntries()):
            tmpTree[i].GetEntry(iEntry)
            select = passCut(tmpTree[i], bTag)
            if select == 1:
                background.Fill(varsList.findVar(tmpTree[i], 'BDT_EWK'), varsList.findVar(tmpTree[i], 'BDT_QCD'), tmpTree[i].triggerEff*tmpScale)
                EWK.Fill(varsList.findVar(tmpTree[i], 'BDT_EWK'), varsList.findVar(tmpTree[i], 'BDT_QCD'), tmpTree[i].triggerEff*tmpScale)
            if select == 3:
                MC.Fill(varsList.findVar(tmpTree[i], 'BDT_EWK'), varsList.findVar(tmpTree[i], 'BDT_QCD'), tmpTree[i].triggerEff*tmpScale)
    if signalSelection != '':
        var_signal = []
        for i in range(4):
            var_signal.append(r.TH1F('%s_%i' %(signalSelection,i),"", varRange[0], varRange[1], varRange[2]))
        signalDict = {'H260': (preFix+'H2hh260_all.root', 14.76),
                      'H300': (preFix+'H2hh300_all.root', 15.9),
                      'H350': (preFix+'H2hh350_all.root', 8.57)}
        if signalSelection in signalDict:
            fSignal = r.TFile(signalDict[signalSelection][0])
            treeSignal = fSignal.Get('eventTree')
            print 'Adding events from: %s ...' %(signalDict[signalSelection][0])
            initNEventsSignal = fSignal.Get('preselection')
            scaleSignal = signalDict[signalSelection][1]*sigBoost*Lumi/initNEventsSignal.GetBinContent(1)
            for iEntry in range(treeSignal.GetEntries()):
                treeSignal.GetEntry(iEntry)
                select = passCut(treeSignal, bTag)
                if select == 1:
                    signal.Fill(varsList.findVar(treeSignal, 'BDT_EWK'), varsList.findVar(treeSignal, 'BDT_QCD'), treeSignal.triggerEff)
                    background.Fill(varsList.findVar(treeSignal, 'BDT_EWK'), varsList.findVar(treeSignal, 'BDT_QCD'), treeSignal.triggerEff*scaleSignal)
            signal.Scale(scaleSignal)
        else:
            print '%s not supported, please use H260, H300 or H350' %signalSelection

    background = estBkg2(MC, data, background, 0.025)
    QCD = estBkg2(MC, data, QCD, 0.025)

    legendHistos.append((background, 'background (%.2f)' %background.Integral()))

    r.gROOT.SetBatch(True)  # to suppress canvas pop-outs
    if bTag == 'True':
        titleName = '1 Medium 1 Loose b-tag'
        fileName = 'bTag'
    elif bTag == 'False':
        titleName = ''
        fileName = 'all'
    elif bTag == 'Revert':
        titleName = 'Revert b-tag'
        fileName = 'revert_bTag'

    psfile = '%s/BDT2D_%s.pdf' %(location, fileName)
    c = r.TCanvas("c","Test", 800, 600)
    #ps = r.TPDF(psfile,112)
    drawOpt = ''
    c.Divide(2,2)
    c.cd(1)
    signSelection, iso = conditions(1)
    EWK.SetTitle('%s %s Events %s (%.1f fb^{-1}); BDT_EWK;BDT_QCD; events / bin' %(signSelection, iso, titleName, Lumi))
    EWK.Draw("CONTZ")    
    legendPosition = (0.5, 0.75, 0.75, 0.9)
    l = tool.setMyLegend(lPosition=legendPosition, lHistList=[(EWK, "EWK (%.2f)" %EWK.Integral())])
    l.Draw('same')
    c.cd(2)
    QCD.SetTitle('%s %s Events %s (%.1f fb^{-1}); BDT_EWK;BDT_QCD; events / bin' %(signSelection, iso, titleName, Lumi))
    QCD.Draw("CONTZ")    
    l2 = tool.setMyLegend(lPosition=legendPosition, lHistList=[(QCD, "QCD (%.2f)" %QCD.Integral())])
    l2.Draw('same')
    c.cd(3)
    signal.SetTitle('%s %s Events %s (%.1f fb^{-1}); BDT_EWK;BDT_QCD; events / bin' %(signSelection, iso, titleName, Lumi))
    signal.Draw("CONTZ")    
    l3 = tool.setMyLegend(lPosition=legendPosition, lHistList=[(signal, "signal x%.0f (%.2f)" %(sigBoost,signal.Integral()))])
    l3.Draw('same')
    c.cd(4)
    background.SetTitle('%s %s Events %s (%.1f fb^{-1}); BDT_EWK;BDT_QCD; events / bin' %(signSelection, iso, titleName, Lumi))
    background.Draw("CONTZ")    
    l4 = tool.setMyLegend(lPosition=legendPosition, lHistList=[(background, "total (%.2f)" %background.Integral())])
    l4.Draw('total')
    c.Update()
    c.Print('%s' %psfile)
    #ps.Close()
    print "Plot saved at %s" %(psfile)


op = opts()
getHistos("H350", 400, "/scratch/zmao/relaxed_regression2/", "True")

