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
    parser.add_option("--predictPtBin", dest="predictPtBin", default = 'False', help="")


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
        maxIso = 10
        if  tree.iso1.at(0) > 1.5  or tree.iso2.at(0) > 1.5:
            iso_count = 1
        if  tree.iso1.at(0) > maxIso  or tree.iso2.at(0) > maxIso:
            iso_count = 3
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

def ptBin(pt1, pt2):
    pt1Bin = 0
    pt2Bin = 0
    if 120 < pt1 < 180:
        pt1Bin = 1
    elif pt1 > 180:
        pt1Bin = 2
    if 80 < pt2 < 120:
        pt2Bin = 1
    elif pt2 > 120:
        pt2Bin = 2
    return pt1Bin*3+pt2Bin

def ptBinName(i):
    if i == 0:
        return 'pt1(0,120) pt2(0,80)'
    elif i == 1:
        return 'pt1(0,120) pt2(80,120)'
    elif i == 2:
        return 'pt1(0,120) pt2(120+)'
    elif i == 3:
        return 'pt1(120,180) pt2(0,80)'
    elif i == 4:
        return 'pt1(120,180) pt2(80,120)'
    elif i == 5:
        return 'pt1(120,180) pt2(120+)'
    elif i == 6:
        return 'pt1(180+) pt2(0,80)'
    elif i == 7:
        return 'pt1(180+) pt2(80,120)'
    elif i == 8:
        return 'pt1(180+) pt2(120+)'

def getHistos(varName, signalSelection, logY, sigBoost, nbins, useData, max, rangeMin, rangeMax, location, bTag, predict, predictPtBin):
    r.gStyle.SetOptStat(0)
    preFix = 'ClassApp_both_ClassApp_QCD_ClassApp_EWK_TMVARegApp_'

    fileList = [('ZZ', preFix + 'ZZ_eff_all.root', 2500, 5),
                ('tt_full_lep',preFix + 'tt_eff_all.root', 26197.5, r.kRed-7),
                ('tt_semi_lep',preFix + 'tt_semi_eff_all.root', 109281, r.kAzure+7),
                #('DYJetsToLL', 'TMVARegApp_DYJetsToLL_eff_all.root', 3504000, r.kGreen-7),
                ('DY1JetsToLL', preFix + 'DY1JetsToLL_eff_all.root', 561000, r.kGreen-7),
                ('DY2JetsToLL', preFix + 'DY2JetsToLL_eff_all.root', 181000, r.kGreen-7),
                ('DY3JetsToLL', preFix + 'DY3JetsToLL_eff_all.root', 51100, r.kGreen-7),
                ('W1JetsToLNu', preFix + 'W1JetsToLNu_eff_all.root', 5400000, r.kMagenta-9),
                ('W2JetsToLNu', preFix + 'W2JetsToLNu_eff_all.root', 1750000, r.kMagenta-9),
                ('W3JetsToLNu', preFix + 'W3JetsToLNu_eff_all.root', 519000, r.kMagenta-9)]
    histList = []
    QCDHistList = []
    varRange = [nbins, rangeMin, rangeMax]
    Lumi = 19.0
    initNEventsList = []
    legendHistos = []
    var_background = []

    tmpFile = []
    tmpTree = []
    var_data = []

    for i in range(3):
        var_data.append([])
        for j in range(10):
            var_data[i].append(r.TH1F('data_%i_%i' %(i,j),"", varRange[0], varRange[1], varRange[2]))

    dataName = preFix + 'dataTotal_all.root'
    fData = r.TFile(dataName)
    treeData = fData.Get('eventTree')
    print 'Adding events from: %s ...' %dataName
    for iEntry in range(treeData.GetEntries()):
        treeData.GetEntry(iEntry)
        select = passCut(treeData, bTag)
        if (select == 0) or (select == 1) or (select > 4):
            continue
        ptBinCount = ptBin(treeData.pt1.at(0), treeData.pt2.at(0))
        var_data[select-2][ptBinCount].Fill(varsList.findVar(treeData, varName))
        var_data[select-2][9].Fill(varsList.findVar(treeData, varName))
    legendHistos.append([])
    for j in range(3):
        var_data[j][9].SetMarkerStyle(8)
        var_data[j][9].SetMarkerSize(0.9)
        legendHistos.append([])
        legendHistos[j+1].append((var_data[j][9], 'observed (%.0f)' %var_data[j][9].Integral()))

    for i in range(len(fileList)):
        tmpFile.append(r.TFile(fileList[i][1]))
        tmpTree.append(tmpFile[i].Get('eventTree'))
        initNEventsList.append(tmpFile[i].Get('preselection'))
        scale = fileList[i][2]*Lumi/initNEventsList[i].GetBinContent(1)
        for j in range(4):
            histList.append([])
            for k in range(10):
                histList[j].append(r.TH1F('%s_%i_%i' %(fileList[i][0],j, k),fileList[i][0], varRange[0], varRange[1], varRange[2]))
        print 'Adding events from: %s ...' %(fileList[i][1])
        for iEntry in range(tmpTree[i].GetEntries()):
            tmpTree[i].GetEntry(iEntry)
            select = passCut(tmpTree[i], bTag)
            if (not select) or (select > 4):
                continue
            ptBinCount = ptBin(tmpTree[i].pt1.at(0),tmpTree[i].pt2.at(0))
            histList[select-1][ptBinCount+i*10].Fill(varsList.findVar(tmpTree[i], varName), tmpTree[i].triggerEff*scale)
            histList[select-1][9+i*10].Fill(varsList.findVar(tmpTree[i], varName), tmpTree[i].triggerEff)

        for j in range(4):
            var_background.append(r.THStack())
            histList[j][9+i*10].SetFillColor(fileList[i][3])
            histList[j][9+i*10].Scale(fileList[i][2]*Lumi/initNEventsList[i].GetBinContent(1))
            var_background[j].Add(histList[j][9+i*10])
            legendHistos[j].append((histList[j][9+i*10], '%s (%.2f)' %(fileList[i][0], histList[j][9+i*10].Integral())))

    data_i = []
    MC_i = []
    data_r = []
    MC_r = []
    e = []
    QCDDiff = []
    QCDDiff2 = []

    for i in range(3):
        QCDHistList.append([])
        for m in range(9):
            QCDHistList[i].append(r.TH1F('QCD_%i_%i' %(i,m),"", varRange[0], varRange[1], varRange[2]))
            for j in range(varRange[0]):
                dataValue = var_data[i][m].GetBinContent(j+1)
                dataError = var_data[i][m].GetBinError(j+1)
                MCValue = 0
                for k in range(len(fileList)):
                    MCValue +=  histList[i+1][10*k+m].GetBinContent(j+1)
                if i == 0:
                    data_i.append(dataValue)
                    e.append(dataError)
                    MC_i.append(MCValue)
                if i == 2:
                    data_r.append(dataValue)
                    MC_r.append(MCValue)
                print dataValue, MCValue

                if dataValue - MCValue > 0:
                    QCDHistList[i][m].SetBinContent(j+1, dataValue - MCValue)
                    QCDHistList[i][m].SetBinError(j+1, dataError)

    for k in range(9):
        QCDDiff.append(QCDHistList[1][k].Clone())
        QCDDiff[k].Divide(QCDHistList[2][k])
        QCDDiff[k].Sumw2()
        QCDDiff2.append(QCDHistList[0][k].Clone())
        QCDDiff2[k].Divide(QCDHistList[2][k])
        QCDDiff2[k].Sumw2()


    fit1 = []
    fit2 = []
    for i in range(9):
        fit1.append(r.TF1("fit1_%i" %i,"[0]", varRange[1],varRange[2]))
        fit1[i].SetParName(0,'scale')
        QCDDiff[i].Fit('fit1_%i' %i, '0E')
        fit1[i].SetLineStyle(2)
        fit1[i].SetLineColor(r.kRed)
        fit2.append(r.TF1("fit2_%i" %i,"[0]", varRange[1],varRange[2]))
        fit2[i].SetParName(0,'scale')
        QCDDiff2[i].Fit('fit2_%i' %i, '0E')
        fit2[i].SetLineStyle(2)
        fit2[i].SetLineColor(r.kRed)

    DrawSignal = False
    if signalSelection != '':
        var_signal = []
        for i in range(4):
            var_signal.append(r.TH1F('%s_%i' %(signalSelection,i),"", varRange[0], varRange[1], varRange[2]))
        signalDict = {'H260': (preFix + 'H2hh260_all.root', 14.76),
                      'H300': (preFix + 'H2hh300_all.root', 15.9),
                      'H350': (preFix + 'H2hh350_all.root', 8.57)}
        if signalSelection in signalDict:
            fSignal = r.TFile(signalDict[signalSelection][0])
            treeSignal = fSignal.Get('eventTree')
            print 'Adding events from: %s ...' %(signalDict[signalSelection][0])
            for iEntry in range(treeSignal.GetEntries()):
                treeSignal.GetEntry(iEntry)
                select = passCut(treeSignal, bTag)
                if (not select) or (select > 4):
                    continue
                var_signal[select-1].Fill(varsList.findVar(treeSignal, varName), treeSignal.triggerEff)
            initNEventsSignal = fSignal.Get('preselection')
            for i in range(4):
                var_signal[i].SetLineStyle(7)
                var_signal[i].SetLineWidth(4)
                var_signal[i].Scale(signalDict[signalSelection][1]*sigBoost*Lumi/initNEventsSignal.GetBinContent(1))
                if sigBoost != 1:
                    legendHistos[i].append((var_signal[i], '%sx%0.f (%.2f)' %(signalSelection, sigBoost, var_signal[i].Integral())))
                else:
                    legendHistos[i].append((var_signal[i], '%s (%.2f)' %(signalSelection, var_signal[i].Integral())))
            DrawSignal = True
        else:
            print '%s not supported, please use H260, H300 or H350' %signalSelection

    relaxed2Tight = r.TH1F('relaxed2Tight','', varRange[0], varRange[1], varRange[2])
    SS2OS = r.TH1F('SS2OS','', varRange[0], varRange[1], varRange[2])
    relaxed2Signal = r.TH1F('relaxed2Signal','', varRange[0], varRange[1], varRange[2])
    SS2OS_signal = r.TH1F('SS2OS_signal','', varRange[0], varRange[1], varRange[2])
    fullHistTranslate = r.TH1F('fullHistTranslate','', varRange[0], varRange[1], varRange[2])


    for i in range(varRange[0]):
        relaxed2TightCount = 0
        relaxed2SignalCount = 0
        SS2OSCount = 0
        SS2OS_signalCount = 0
        for j in range(9):
            SS_tight_Events = QCDHistList[0][j].GetBinContent(i+1)
            SS_tight_Error = QCDHistList[0][j].GetBinError(i+1)
            OS_relaxed_Events = QCDHistList[1][j].GetBinContent(i+1)
            OS_relaxed_Error = QCDHistList[1][j].GetBinError(i+1)
            SS_Events = QCDHistList[2][j].GetBinContent(i+1)
            SS_Error = QCDHistList[2][j].GetBinError(i+1)

            relaxed2TightCount += fit2[j].GetParameter(0)*SS_Events
            relaxed2SignalCount += fit2[j].GetParameter(0)*OS_relaxed_Events
            SS2OSCount += fit1[j].GetParameter(0)*SS_Events
            SS2OS_signalCount += fit1[j].GetParameter(0)*SS_tight_Events

        relaxed2Tight.SetBinContent(i+1, relaxed2TightCount)
        relaxed2Signal.SetBinContent(i+1, relaxed2SignalCount)
        SS2OS.SetBinContent(i+1, SS2OSCount)
        SS2OS_signal.SetBinContent(i+1, SS2OS_signalCount)



#             relaxed2Tight.SetBinError(i+1, getCombinedError(scale_relaxed2Tight, scale_er_relaxed2Tight, SS_Events, SS_Error))
#             SS2OS.SetBinError(i+1, getCombinedError(scale_SS2OS, scale_er_SS2OS, SS_Events, SS_Error))
#             relaxed2Tight.SetLineColor(r.kSpring+8)
    relaxed2Tight.SetFillColor(r.kSpring+1)
#             SS2OS.SetLineColor(r.kOrange)
    SS2OS.SetFillColor(r.kOrange-4)
    SS2OS_signal.SetLineColor(r.kSpring+1)
    SS2OS_signal.SetLineWidth(2)
    relaxed2Signal.SetLineStyle(2)
    relaxed2Signal.SetLineColor(r.kOrange-4)
    relaxed2Signal.SetLineWidth(2)

    legendHistos[0].append((SS2OS_signal, 'From SS/Tight (%.0f)' %SS2OS_signal.Integral()))
    legendHistos[0].append((relaxed2Signal, 'From OS/Relax (%.0f)' %relaxed2Signal.Integral()))

    var_background[1].Add(relaxed2Tight)
    var_background[2].Add(SS2OS)
    legendHistos[1].append((relaxed2Tight, 'From SS/Relax (%.0f)' %relaxed2Tight.Integral()))
    legendHistos[2].append((SS2OS, 'From SS/Relax (%.0f)' %SS2OS.Integral()))
    relaxed2Signal = tool.addFakeTHStack(relaxed2Signal,var_background[0])
    SS2OS_signal = tool.addFakeTHStack(SS2OS_signal,var_background[0])


    legendPosition = (0.6, 0.7, 0.90, 0.88)
    l = []
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

    psfile = '%s/%s_%s.pdf' %(location, varName, fileName)
    c = r.TCanvas("c","Test", 800, 600)
    #ps = r.TPDF(psfile,112)
    c.Divide(2,2)
    drawOpt = ''
    for k in range(4):
        c.cd(k+1)
        if logY == 'True':
            r.gPad.SetLogy()
        signSelection, iso = conditions(k+1)
        var_background[k].SetTitle('%s %s Events %s (%.1f fb^{-1}); %s; events / bin' %(signSelection, iso, titleName, Lumi,varName))
        var_background[k].SetMaximum(max)
        var_background[k].SetMinimum(0.01)
        var_background[k].Draw()
        if predict == 'True' and k == 0:
            SS2OS_signal.Draw('same')
            relaxed2Signal.Draw('same')
            #fullHistTranslate.Draw('same')
        if k != 0 and useData == 'True':
            var_data[k-1][9].Draw('PE same')
        legendPosition = (0.63, 0.93 - 0.035*len(legendHistos[k]), 0.93, 0.9)
        l.append(tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos[k]))
        l[k].Draw('same')
        var_signal[k].Draw('same')
    c.Update()
    c.Print('%s(' %psfile)

    c.Clear()
    c.Divide(3,3)
    legendPosition = (0.63, 0.8, 0.93, 0.9)
    l1 = []
    l2 = []
    for i in range(9):
        c.cd(i+1)
        r.gPad.SetLogy(0)
        QCDDiff[i].SetTitle('OS/SS Relaxed %s %s (%.1f fb^{-1}); %s; tight/relaxed' %(ptBinName(i), titleName, Lumi,varName))
        QCDDiff[i].Draw()
        fit1[i].SetLineColor(r.kRed)
        fit1[i].SetLineStyle(2)
        fit1[i].Draw('same')
        l1.append(tool.setMyLegend(lPosition=legendPosition, lHistList=[(fit1[i],'%.3f \pm %.3f' %(fit1[i].GetParameter(0), fit1[i].GetParError(0)))]))
        l1[i].Draw('same')
    c.Update()
    c.Print('%s' %psfile)
    for i in range(9):
        c.cd(i+1)
        r.gPad.SetLogy(0)
        QCDDiff2[i].SetTitle('tight/relaxed SS %s %s (%.1f fb^{-1}); %s; tight/relaxed' %(ptBinName(i), titleName, Lumi,varName))
        QCDDiff2[i].Draw() 
        fit2[i].SetLineColor(r.kRed)
        fit2[i].SetLineStyle(2)
        fit2[i].Draw('same')
        l2.append(tool.setMyLegend(lPosition=legendPosition, lHistList=[(fit2[i],'%.3f \pm %.3f' %(fit2[i].GetParameter(0), fit2[i].GetParError(0)))]))
        l2[i].Draw('same')
    c.Print('%s)' %psfile)
    #ps.Close()
    print "Plot saved at %s" %(psfile)

op = opts()
if op.varName != 'test':
    getHistos(op.varName, op.signal, op.logy, float(op.sigBoost), int(op.nbins),
           op.useData, float(op.max), float(op.rangeMin), float(op.rangeMax), op.location, op.bTag, op.predict, 'True')

