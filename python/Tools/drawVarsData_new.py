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

def addFakeTHStack(hist, stack):
    for iHist in stack.GetHists():
        for i in range(iHist.GetNbinsX()):
            currentValue = hist.GetBinContent(i+1)
            hist.SetBinContent(i+1,currentValue + iHist.GetBinContent(i+1))
    return hist

def getHistos(varName, signalSelection, logY, sigBoost, nbins, useData, max, rangeMin, rangeMax, location, bTag, predict):
    r.gStyle.SetOptStat(0)
    fileList = [('ZZ', 'TMVARegApp_ZZ_eff_all.root', 2500, 5),
                ('tt_full_lep','TMVARegApp_tt_eff_all.root', 26197.5, r.kRed-7),
                ('tt_semi_lep','TMVARegApp_tt_semi_eff_all.root', 109281, r.kAzure+7),
                ('DYJetsToLL', 'TMVARegApp_DYJetsToLL_eff_all.root', 3504000, r.kGreen-7),
                ('W2JetsToLNu', 'TMVARegApp_W2JetsToLNu_eff_all.root', 1750000, r.kMagenta-9)]
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
        var_data.append(r.TH1F('data_%i' %(i),"", varRange[0], varRange[1], varRange[2]))
    fData = r.TFile('TMVARegApp_dataTotal_all.root')
    treeData = fData.Get('eventTree')
    print 'Adding events from: dataTotal_all.root ...'
    for iEntry in range(treeData.GetEntries()):
        treeData.GetEntry(iEntry)
        select = passCut(treeData, bTag)
        if (select == 0) or (select == 1):
            continue
        var_data[select-2].Fill(varsList.findVar(treeData, varName))
    legendHistos.append([])
    for j in range(3):
        var_data[j].SetMarkerStyle(8)
        var_data[j].SetMarkerSize(0.9)
        legendHistos.append([])
        legendHistos[j+1].append((var_data[j], 'observed (%.0f)' %var_data[j].Integral()))

    for i in range(len(fileList)): 
        for j in range(4):
            histList.append(r.TH1F('%s_%i' %(fileList[i][0],j),fileList[i][0], varRange[0], varRange[1], varRange[2]))
        print 'Adding events from: %s ...' %(fileList[i][1])
        tmpFile.append(r.TFile(fileList[i][1]))
        tmpTree.append(tmpFile[i].Get('eventTree'))
        for iEntry in range(tmpTree[i].GetEntries()):
            tmpTree[i].GetEntry(iEntry)
            select = passCut(tmpTree[i], bTag)
            if not select:
                continue
            histList[4*i+select-1].Fill(varsList.findVar(tmpTree[i], varName), tmpTree[i].triggerEff)
    
        initNEventsList.append(tmpFile[i].Get('preselection'))
        for j in range(4):
            var_background.append(r.THStack())
            histList[4*i+j].SetFillColor(fileList[i][3])
            histList[4*i+j].Scale(fileList[i][2]*Lumi/initNEventsList[i].GetBinContent(1))
            var_background[j].Add(histList[4*i+j])
            legendHistos[j].append((histList[4*i+j], '%s (%.2f)' %(fileList[i][0], histList[4*i+j].Integral())))

    data_i = []
    MC_i = []
    data_r = []
    MC_r = []
    e = []

    for i in range(3):
        QCDHistList.append(r.TH1F('QCD_%i' %(i),"", varRange[0], varRange[1], varRange[2]))
        for j in range(varRange[0]):
            dataValue = var_data[i].GetBinContent(j+1)
            dataError = var_data[i].GetBinError(j+1)
            MCValue = 0
            for k in range(len(fileList)):
                MCValue +=  histList[4*k+1+i].GetBinContent(j+1)
            if i == 0:
                data_i.append(dataValue)
                e.append(dataError)
                MC_i.append(MCValue)
            if i == 2:
                data_r.append(dataValue)
                MC_r.append(MCValue)
            if dataValue - MCValue > 0:
                QCDHistList[i].SetBinContent(j+1, dataValue - MCValue)
                QCDHistList[i].SetBinError(j+1, dataError)

    QCDDiff = r.TH1F('QCD_diff',"", varRange[0], varRange[1], varRange[2])
    QCDDiff2 = r.TH1F('QCD_diff2',"", varRange[0], varRange[1], varRange[2])

    for j in range(varRange[0]):
        SS_tight_Events = QCDHistList[0].GetBinContent(j+1)
        OS_Events = QCDHistList[1].GetBinContent(j+1)
        SS_Events = QCDHistList[2].GetBinContent(j+1)
        SS_tight_Error = QCDHistList[0].GetBinError(j+1)
        OS_Error = QCDHistList[1].GetBinError(j+1)
        SS_Error = QCDHistList[2].GetBinError(j+1)

        if SS_Events != 0:
            QCDDiff.SetBinContent(j+1, OS_Events/SS_Events)
            QCDDiff.SetBinError(j+1, OS_Events/SS_Events*getCombinedError(OS_Events, OS_Error, SS_Events, SS_Error))
            QCDDiff2.SetBinContent(j+1, SS_tight_Events/SS_Events)
            QCDDiff2.SetBinError(j+1, SS_tight_Events/SS_Events*getCombinedError(SS_tight_Events, SS_tight_Error, SS_Events, SS_Error))
    fit1 = r.TF1("fit1","[0]", varRange[1],varRange[2]);
    fit1.SetParName(0,'scale')
    QCDDiff.Fit('fit1', '0E')
    fit1.SetLineStyle(2)
    fit1.SetLineColor(r.kRed)
    fit2 = r.TF1("fit2","[0]", varRange[1],varRange[2])
    fit2.SetParName(0,'scale')
    QCDDiff2.Fit('fit2', '0E')
    fit2.SetLineStyle(2)
    fit2.SetLineColor(r.kRed)


    DrawSignal = False
    if signalSelection != '':
        var_signal = []
        for i in range(4):
            var_signal.append(r.TH1F('%s_%i' %(signalSelection,i),"", varRange[0], varRange[1], varRange[2]))
        signalDict = {'H260': ('TMVARegApp_H2hh260_all.root', 14.76),
                      'H300': ('TMVARegApp_H2hh300_all.root', 15.9),
                      'H350': ('TMVARegApp_H2hh350_all.root', 8.57)}
        if signalSelection in signalDict:
            fSignal = r.TFile(signalDict[signalSelection][0])
            treeSignal = fSignal.Get('eventTree')
            print 'Adding events from: %s ...' %(signalDict[signalSelection][0])
            for iEntry in range(treeSignal.GetEntries()):
                treeSignal.GetEntry(iEntry)
                select = passCut(treeSignal, bTag)
                if not select:
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

    if predict == 'True':
        relaxed2Tight = r.TH1F('relaxed2Tight','', varRange[0], varRange[1], varRange[2])
        SS2OS = r.TH1F('SS2OS','', varRange[0], varRange[1], varRange[2])
        relaxed2Signal = r.TH1F('relaxed2Signal','', varRange[0], varRange[1], varRange[2])
        SS2OS_signal = r.TH1F('SS2OS_signal','', varRange[0], varRange[1], varRange[2])
        scale_SS2OS = fit1.GetParameter(0)
        scale_er_SS2OS = fit1.GetParError(0)
        scale_relaxed2Tight = fit2.GetParameter(0)
        scale_er_relaxed2Tight = fit2.GetParError(0)

        for i in range(varRange[0]):

            SS_tight_Events = QCDHistList[0].GetBinContent(i+1)
            SS_tight_Error = QCDHistList[0].GetBinError(i+1)
            OS_relaxed_Events = QCDHistList[1].GetBinContent(i+1)
            OS_relaxed_Error = QCDHistList[1].GetBinError(i+1)
            SS_Events = QCDHistList[2].GetBinContent(i+1)
            SS_Error = QCDHistList[2].GetBinError(i+1)

            relaxed2Tight.SetBinContent(i+1, scale_relaxed2Tight*SS_Events)
            relaxed2Signal.SetBinContent(i+1, scale_relaxed2Tight*OS_relaxed_Events)
            SS2OS.SetBinContent(i+1, scale_SS2OS*SS_Events)
            SS2OS_signal.SetBinContent(i+1, scale_SS2OS*SS_tight_Events)

#             relaxed2Tight.SetBinError(i+1, getCombinedError(scale_relaxed2Tight, scale_er_relaxed2Tight, SS_Events, SS_Error))
#             SS2OS.SetBinError(i+1, getCombinedError(scale_SS2OS, scale_er_SS2OS, SS_Events, SS_Error))
#             relaxed2Tight.SetLineColor(r.kSpring+8)
        relaxed2Tight.SetFillColor(r.kSpring+1)
#             SS2OS.SetLineColor(r.kOrange)
        SS2OS.SetFillColor(r.kOrange-4)
        SS2OS_signal.SetLineColor(r.kOrange-4)
        SS2OS_signal.SetLineStyle(2)
        SS2OS_signal.SetLineWidth(2)
        relaxed2Signal.SetLineColor(r.kSpring+1)
        relaxed2Signal.SetLineWidth(2)
        legendHistos[0].append((SS2OS_signal, 'From SS/Tight (%.0f)' %SS2OS_signal.Integral()))
        legendHistos[0].append((relaxed2Signal, 'From OS/Relax (%.0f)' %relaxed2Signal.Integral()))
        var_background[1].Add(relaxed2Tight)
        var_background[2].Add(SS2OS)
        legendHistos[1].append((relaxed2Tight, 'From SS/Relax (%.0f)' %relaxed2Tight.Integral()))
        legendHistos[2].append((SS2OS, 'From SS/Relax (%.0f)' %SS2OS.Integral()))
        relaxed2Signal = addFakeTHStack(relaxed2Signal,var_background[0])
        var_background[0].Add(SS2OS_signal)





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
            relaxed2Signal.Draw('same')
        if k != 0:
            var_data[k-1].Draw('PE same')
        legendPosition = (0.63, 0.93 - 0.035*len(legendHistos[k]), 0.93, 0.9)
        l.append(tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos[k]))
        l[k].Draw('same')
        var_signal[k].Draw('same')
    c.Update()
    c.Print('%s(' %psfile)
    c.cd(1)
    r.gPad.SetLogy(0)
    QCDDiff.SetTitle('OS/SS MultiJet Relaxed Events %s (%.1f fb^{-1}); %s; OS/SS' %(titleName, Lumi,varName))
    QCDDiff.SetMarkerStyle(8)
    QCDDiff.SetMarkerSize(0.9)
    QCDDiff.SetMaximum(2)
    QCDDiff.SetMinimum(0)
    QCDDiff.Draw('PE')
    fit1.Draw('same')
    lFit1 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fit1,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(fit1.GetParameter(0), fit1.GetParError(0)))])
    lFit1.Draw('same')
    for k in range(3):
        c.cd(k+2)
        if logY == 'True':
            r.gPad.SetLogy()
        signSelection, iso = conditions(k+2)
        QCDHistList[k].SetTitle('%s %s Data - MC Events %s (%.1f fb^{-1}); %s; events / bin' %(signSelection, iso, titleName, Lumi,varName))
        QCDHistList[k].SetMarkerStyle(8)
        QCDHistList[k].SetMarkerSize(0.9)
        QCDHistList[k].SetMaximum(max)
        QCDHistList[k].SetMinimum(1)
        QCDHistList[k].Draw('PE')
    c.Update()
    c.Print('%s' %psfile)
    c.cd(1)
    r.gPad.SetLogy(0)
    QCDDiff2.SetTitle('tight/relaxed MultiJet SS Events %s (%.1f fb^{-1}); %s; tight/relaxed' %(titleName, Lumi,varName))
    QCDDiff2.SetMarkerStyle(8)
    QCDDiff2.SetMarkerSize(0.9)
    QCDDiff2.SetMinimum(0)
    QCDDiff2.SetMaximum(0.1)
    QCDDiff2.Draw('PE')
    fit2.Draw('same')
    lFit2 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fit2,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(fit2.GetParameter(0), fit2.GetParError(0)))])
    lFit2.Draw('same')
    c.Print('%s)' %psfile)
    #ps.Close()
    print "Plot saved at %s" %(psfile)

op = opts()
if op.varName != 'test':
    getHistos(op.varName, op.signal, op.logy, float(op.sigBoost), int(op.nbins),
           op.useData, float(op.max), float(op.rangeMin), float(op.rangeMax), op.location, op.bTag, op.predict)

