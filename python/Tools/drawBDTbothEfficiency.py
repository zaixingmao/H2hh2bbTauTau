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
    parser.add_option("--tail", dest="tail", default = 'test', help="")

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

def estBkg(MC, data, backgroundHist, scale):
    for i in range(data.GetNbinsX()):
        currentValue = backgroundHist.GetBinContent(i+1)
        backgroundHist.SetBinContent(i+1, (data.GetBinContent(i+1)-MC.GetBinContent(i+1))*scale + currentValue)
    return backgroundHist

def estBkg2(MC, data, backgroundHist, scale):
    for i in range(data.GetNbinsX()):
        for j in range(data.GetNbinsX()):
            currentValue = backgroundHist.GetBinContent(i+1, j+1)
            if (data.GetBinContent(i+1, j+1)-MC.GetBinContent(i+1, j+1))> 0:
                backgroundHist.SetBinContent(i+1, j+1, (data.GetBinContent(i+1, j+1)-MC.GetBinContent(i+1, j+1))*scale + currentValue)
            else:
                backgroundHist.SetBinContent(i+1, j+1, currentValue)
    return backgroundHist

def combineSigBkg2(sig, bkg, combine):
    for i in range(bkg.GetNbinsX()):
        for j in range(bkg.GetNbinsY()):
            combine.Fill(sig.GetXaxis().GetBinCenter(i+1), sig.GetXaxis().GetBinCenter(j+1), sig.GetBinContent(i+1, j+1) + bkg.GetBinContent(i+1, j+1))
    return combine

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
    bin = int(nBins*(x-xMin)/(xMax-xMin))
    if x == -0.9 or x == -0.8:
        bin = bin+1
    if bin >= nBins:
        return nBins-1
    else:
        return bin

def calcBDTEff(signal, background, eff):
    sigTotal = signal.Integral()
    bkgTotal = background.Integral()
    nBins = eff.GetNbinsX()
    for i in range(signal.GetNbinsX()):
        xBin = findBin(background.Integral(1,i+1)/bkgTotal, nBins, 0, 1)
        sigEff = 1-signal.Integral(1,i+1)/sigTotal
        eff.SetBinContent(xBin+1, sigEff)
    return eff

def calcBDTLikelyhoodRatio2D(signal, background, lkR):
    nBinsX = signal.GetNbinsX()
    nBinsY = signal.GetNbinsY()
    lkRnBinsX = lkR.GetNbinsX()
    lkRnBinsY = lkR.GetNbinsY()
    for i in range(nBinsX):
        for j in range(nBinsY):
            sigContent = signal.GetBinContent(i+1, j+1)
            bkgContent = background.GetBinContent(i+1, j+1)
            x = signal.GetXaxis().GetBinCenter(i+1)
            y = signal.GetYaxis().GetBinCenter(j+1)
            if bkgContent > 0:
                lkR.Fill(x,y, sigContent/bkgContent)
            elif sigContent > 0:
                lkR.Fill(x,y, 1000)
    return lkR

def calcEffFromLKR(signal, background, lkR, eff):
    nBinsSig = signal.GetNbinsX()
    nBinsX = lkR.GetNbinsX()
    nBinsY = lkR.GetNbinsY()
    nBins = eff.GetNbinsX()
    sigTotal = signal.Integral()
    bkgTotal = background.Integral()
    cutRange = []
    for i in range(200):
        cutRange.append(40*i)
    for cut in cutRange:
        sigEvents = 0
        bkgEvents = 0
        pointCounter = 0
        for i in range(nBinsX):
            for j in range(nBinsY):
                if lkR.GetBinContent(i+1,j+1) >= cut:
                    x_low = findBin(lkR.GetXaxis().GetBinLowEdge(i+1), nBinsSig, -1, 1)
                    x_high = x_low+int(nBinsSig/nBinsX)
                    y_low = findBin(lkR.GetYaxis().GetBinLowEdge(j+1), nBinsSig, -1, 1)
                    y_high = y_low+int(nBinsSig/nBinsX)
                    sigEvents += signal.Integral(x_low+1,x_high, y_low+1,y_high)
                    bkgEvents += background.Integral(x_low+1,x_high, y_low+1,y_high)

        xBin = findBin(1-bkgEvents/bkgTotal, nBins, 0, 1)
        eff.SetBinContent(xBin+1, sigEvents/sigTotal)
    return eff

def calcBDTEff2(signal, background, eff, cutContor):
    sigTotal = signal.Integral()
    bkgTotal = background.Integral()
    nBins = eff.GetNbinsX()
    nEntries = signal.GetNbinsX()
    nEntriesY = signal.GetNbinsY()
    for i in range(nEntries):
        tool.printProcessStatus(i, nEntries, 'Calcuation')
        bkgRejXsigEff = 0
        bkgRejSave = 0
        sigEffSave = 1
        jSave = 0
        for j in range(nEntriesY):
            bkgRej = background.Integral(1,i+1, 1, j+1)/bkgTotal
            sigEff = 1-signal.Integral(1,i+1, 1, j+1)/sigTotal
            if bkgRej*sigEff > bkgRejXsigEff:
                bkgRejSave = bkgRej
                sigEffSave = sigEff
                bkgRejXsigEff = bkgRej*sigEff
                jSave = j
        xBin = findBin(bkgRejSave, nBins, 0, 1)
        eff.SetBinContent(xBin+1, sigEffSave)
        cutContor.SetBinContent(i+1,jSave+1, 10)
    return eff, cutContor

def add2DHist(hist1, hist2, nBins):
    for i in range(nBins):
        for j in range(nBins):
            hist1.Fill(hist2.GetBinContent(i,j))
    return hist1

def getHistos(signalSelection, sigBoost, location, bTag, tail):
    r.gStyle.SetOptStat(0)
    preFix = 'ClassApp_both_TMVARegApp_'

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
    varRange = [100, -1, 1]
    varRange2 = [20, -1, 1]
    varRange3 = [100, 0, 1]
    varRange4 = [20, -1, 1]

    Lumi = 19.0
    initNEventsList = []
    legendHistos = []

    rootFileName = '%s/BDTEfficiency_%s.root' %(location, tail)
    oFile = r.TFile(rootFileName,"RECREATE")

    tmpFile = []
    tmpTree = []
    var_data = []
    signal_EWK = r.TH1F('signal_EWK',"", varRange[0], varRange[1], varRange[2])
    signal_QCD = r.TH1F('signal_QCD',"", varRange[0], varRange[1], varRange[2])
    signal_both = r.TH1F('signal_both',"", varRange[0], varRange[1], varRange[2])
    signal_2D = r.TH2F('signal_2D',"", varRange[0], varRange[1], varRange[2], varRange[0], varRange[1], varRange[2])
    lkr_2D = r.TH2F('lkr_2D',"", varRange2[0], varRange2[1], varRange2[2], varRange2[0], varRange2[1], varRange2[2])

    eff_QCD = r.TH1F('eff_QCD', '', varRange3[0], varRange3[1], varRange3[2])
    eff_EWK = r.TH1F('eff_EWK', '', varRange3[0], varRange3[1], varRange3[2])
    eff_both = r.TH1F('eff_both', '', varRange3[0], varRange3[1], varRange3[2])
    eff_2D = r.TH1F('eff_2D', '', varRange3[0], varRange3[1], varRange3[2])

    background_EWK = r.TH1F('background_EWK',"", varRange[0], varRange[1], varRange[2])
    background_QCD = r.TH1F('background_QCD',"", varRange[0], varRange[1], varRange[2])
    background_both = r.TH1F('background_both',"", varRange[0], varRange[1], varRange[2])
    background_2D = r.TH2F('background_2D',"", varRange[0], varRange[1], varRange[2], varRange[0], varRange[1], varRange[2])
    total_2D = r.TH2F('total_2D',"", varRange4[0], varRange4[1], varRange4[2], varRange4[0], varRange4[1], varRange4[2])

    MC_EWK = r.TH1F('MC_EWK',"", varRange[0], varRange[1], varRange[2])
    MC_QCD = r.TH1F('MC_QCD',"", varRange[0], varRange[1], varRange[2])
    MC_both = r.TH1F('MC_both',"", varRange[0], varRange[1], varRange[2])
    MC_2D = r.TH2F('MC_2D',"", varRange[0], varRange[1], varRange[2], varRange[0], varRange[1], varRange[2])

    data_EWK = r.TH1F('data_EWK',"", varRange[0], varRange[1], varRange[2])
    data_QCD = r.TH1F('data_QCD',"", varRange[0], varRange[1], varRange[2])
    data_both = r.TH1F('data_both',"", varRange[0], varRange[1], varRange[2])
    data_2D = r.TH2F('data_2D',"", varRange[0], varRange[1], varRange[2], varRange[0], varRange[1], varRange[2])

    dataName = preFix + 'dataTotal_all.root'
    fData = r.TFile(dataName)
    treeData = fData.Get('eventTree')
    print 'Adding events from: %s ...' %dataName
    for iEntry in range(treeData.GetEntries()):
        treeData.GetEntry(iEntry)
        select = passCut(treeData, bTag)
        if select == 3:
            data_both.Fill(treeData.BDT_both)
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
                background_both.Fill(tmpTree[i].BDT_both, tmpTree[i].triggerEff*tmpScale)
            if select == 3:
                MC_both.Fill(tmpTree[i].BDT_both, tmpTree[i].triggerEff*tmpScale)

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
                    signal_both.Fill(treeSignal.BDT_both, treeSignal.triggerEff)
            signal_both.Scale(scaleSignal)
        else:
            print '%s not supported, please use H260, H300 or H350' %signalSelection

    background_both = estBkg(MC_both, data_both, background_both, 0.025)

    eff_both = calcBDTEff(signal_both, background_both, eff_both)

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

    eff_both.SetTitle('Background Rejection VS Signal Efficiency ; Background Rejection; Signal Efficiency')

    oFile.cd()
   
    eff_both.Write()

    oFile.Close()
    print "ROOT file saved at %s" %(rootFileName)

op = opts()
getHistos("H350", 400, "/scratch/zmao/BDT_4/", "True", op.tail)

