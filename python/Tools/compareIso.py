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
    elif selection == 5:
        return 'OS', 'relaxed2'
    elif selection == 6:
        return 'SS', 'relaxed2'

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
        maxIso = 4
        if  tree.iso1.at(0) > 1.5  or tree.iso2.at(0) > 1.5:
            iso_count = 1
        if  tree.iso1.at(0) > maxIso  or tree.iso2.at(0) > maxIso:
            iso_count = 2
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


def getHistos(varName, signalSelection, logY, sigBoost, nbins, useData, max, rangeMin, rangeMax, location, bTag, predict, predictPtBin):
    r.gStyle.SetOptStat(0)
    preFix = 'ClassApp_both_ClassApp_QCD_ClassApp_EWK_TMVARegApp_'

    fileList = [('ZZ', preFix + 'ZZ_eff_all.root', 2500, 5),
                ('tt_full_lep',preFix + 'tt_eff_all.root', 26197.5, r.kRed-7),
                ('tt_semi_lep',preFix + 'tt_semi_eff_all.root', 109281, r.kAzure+7),
                #('DYJetsToLL', 'TMVARegApp_DYJetsToLL_eff_all.root', 3504000, r.kGreen-7),
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
    fitList = []
    for i in range(6):
        fitList.append(r.TF1("Fit%i" %i,"[0]+[1]*x", rangeMin, rangeMax))
        fitList[i].SetLineColor(r.kRed)
        fitList[i].SetLineStyle(2)
        fitList[i].SetParameter(0,0)
        fitList[i].SetParameter(1,0)

    tmpFile = []
    tmpTree = []
    var_data = []

    for i in range(5):
        var_data.append(r.TH1F('data_%i' %(i),"", varRange[0], varRange[1], varRange[2]))
    dataName = preFix + 'dataTotal_all.root'
    fData = r.TFile(dataName)
    treeData = fData.Get('eventTree')
    print 'Adding events from: %s ...' %dataName
    for iEntry in range(treeData.GetEntries()):
        treeData.GetEntry(iEntry)
        select = passCut(treeData, bTag)
        if (select == 0) or (select == 1):
            continue
        var_data[select-2].Fill(varsList.findVar(treeData, varName))
    legendHistos.append([])
    for j in range(5):
        var_data[j].SetMarkerStyle(8)
        var_data[j].SetMarkerSize(0.9)
        legendHistos.append([])
        legendHistos[j+1].append((var_data[j], 'observed (%.0f)' %var_data[j].Integral()))

    for i in range(len(fileList)): 
        for j in range(6):
            histList.append(r.TH1F('%s_%i' %(fileList[i][0],j),fileList[i][0], varRange[0], varRange[1], varRange[2]))
        print 'Adding events from: %s ...' %(fileList[i][1])
        tmpFile.append(r.TFile(fileList[i][1]))
        tmpTree.append(tmpFile[i].Get('eventTree'))
        for iEntry in range(tmpTree[i].GetEntries()):
            tmpTree[i].GetEntry(iEntry)
            select = passCut(tmpTree[i], bTag)
            if not select:
                continue
            histList[6*i+select-1].Fill(varsList.findVar(tmpTree[i], varName), tmpTree[i].triggerEff)
    
        initNEventsList.append(tmpFile[i].Get('preselection'))
        for j in range(6):
            var_background.append(r.THStack())
            histList[6*i+j].SetFillColor(fileList[i][3])
            histList[6*i+j].Scale(fileList[i][2]*Lumi/initNEventsList[i].GetBinContent(1))
            var_background[j].Add(histList[6*i+j])
            legendHistos[j].append((histList[6*i+j], '%s (%.2f)' %(fileList[i][0], histList[6*i+j].Integral())))

    data_i = []
    MC_i = []
    data_r = []
    MC_r = []
    e = []

    for i in range(5):
        QCDHistList.append(r.TH1F('QCD_%i' %(i),"", varRange[0], varRange[1], varRange[2]))
        for j in range(varRange[0]):
            dataValue = var_data[i].GetBinContent(j+1)
            dataError = var_data[i].GetBinError(j+1)
            MCValue = 0
            for k in range(len(fileList)):
                MCValue +=  histList[6*k+1+i].GetBinContent(j+1)
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
    fit1 = r.TF1("fit1","[0]", varRange[1],varRange[2])
    fit1.SetParName(0,'scale')
    QCDDiff.Fit('fit1', '0E')
    fit1.SetLineStyle(2)
    fit1.SetLineColor(r.kRed)
    fit2 = r.TF1("fit2","[0]", varRange[1],varRange[2])
    fit2.SetParName(0,'scale')
    QCDDiff2.Fit('fit2', '0E')
    fit2.SetLineStyle(2)
    fit2.SetLineColor(r.kRed)
    ptBins = [varRange[1], 100, 200, varRange[2]]
    if predictPtBin == 'True':
        fit_l = r.TF1("fit_l","[0]", ptBins[0], ptBins[1])
        fit_l.SetLineColor(r.kRed)
        fit_m = r.TF1("fit_m","[0]", ptBins[1], ptBins[2])
        fit_m.SetLineColor(r.kBlue)
        fit_h = r.TF1("fit_h","[0]", ptBins[2], ptBins[3])
        fit_h.SetLineColor(r.kGreen)
        QCDDiff.Fit('fit_l', '0ER')
        QCDDiff.Fit('fit_m', '0ER')
        QCDDiff.Fit('fit_h', '0ER')
        fit2_l = r.TF1("fit2_l","[0]", ptBins[0], ptBins[1])
        fit2_m = r.TF1("fit2_m","[0]", ptBins[1], ptBins[2])
        fit2_h = r.TF1("fit2_h","[0]", ptBins[2], ptBins[3])
        fit2_l.SetLineColor(r.kRed)
        fit2_m.SetLineColor(r.kBlue)
        fit2_h.SetLineColor(r.kGreen)
        fit2_l.SetLineStyle(2)
        fit2_m.SetLineStyle(2)
        fit2_h.SetLineStyle(2)
        fit_l.SetLineStyle(2)
        fit_m.SetLineStyle(2)
        fit_h.SetLineStyle(2)
        QCDDiff2.Fit('fit2_l', '0ER')
        QCDDiff2.Fit('fit2_m', '0ER')
        QCDDiff2.Fit('fit2_h', '0ER')

    DrawSignal = False
    if signalSelection != '':
        var_signal = []
        for i in range(6):
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
                if not select:
                    continue
                var_signal[select-1].Fill(varsList.findVar(treeSignal, varName), treeSignal.triggerEff)
            initNEventsSignal = fSignal.Get('preselection')
            for i in range(6):
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
        fullHistTranslate = r.TH1F('fullHistTranslate','', varRange[0], varRange[1], varRange[2])

        scale_SS2OS = fit1.GetParameter(0)
        scale_er_SS2OS = fit1.GetParError(0)
        scale_relaxed2Tight = fit2.GetParameter(0)
        scale_er_relaxed2Tight = fit2.GetParError(0)

        if predictPtBin == 'True':
            scale_SS2OS_l = fit_l.GetParameter(0)
            scale_er_SS2OS_l = fit_l.GetParError(0)
            scale_relaxed2Tight_l = fit2_l.GetParameter(0)
            scale_er_relaxed2Tight_l = fit2_l.GetParError(0)
            scale_SS2OS_m = fit_m.GetParameter(0)
            scale_er_SS2OS_m = fit_m.GetParError(0)
            scale_relaxed2Tight_m = fit2_m.GetParameter(0)
            scale_er_relaxed2Tight_m = fit2_m.GetParError(0)
            scale_SS2OS_h = fit_h.GetParameter(0)
            scale_er_SS2OS_h = fit_h.GetParError(0)
            scale_relaxed2Tight_h = fit2_h.GetParameter(0)
            scale_er_relaxed2Tight_h = fit2_h.GetParError(0)

        for i in range(varRange[0]):

            SS_tight_Events = QCDHistList[0].GetBinContent(i+1)
            SS_tight_Error = QCDHistList[0].GetBinError(i+1)
            OS_relaxed_Events = QCDHistList[1].GetBinContent(i+1)
            OS_relaxed_Error = QCDHistList[1].GetBinError(i+1)
            SS_Events = QCDHistList[2].GetBinContent(i+1)
            SS_Error = QCDHistList[2].GetBinError(i+1)

            scale_1 = scale_relaxed2Tight
            scale_2 = scale_SS2OS

            if predictPtBin == 'True':
                ptValue = QCDHistList[0].GetBinCenter(i+1)
                if ptValue <= ptBins[1]:
                    scale_1 = scale_relaxed2Tight_l
                    scale_2 = scale_SS2OS_l
                elif ptValue <= ptBins[2]:
                    scale_1 = scale_relaxed2Tight_m
                    scale_2 = scale_SS2OS_m
                else:
                    scale_1 = scale_relaxed2Tight_h
                    scale_2 = scale_SS2OS_h

            relaxed2Tight.SetBinContent(i+1, scale_1*SS_Events)
            relaxed2Signal.SetBinContent(i+1, scale_1*OS_relaxed_Events)
            SS2OS.SetBinContent(i+1, scale_2*SS_Events)
            SS2OS_signal.SetBinContent(i+1, scale_2*SS_tight_Events)

            if SS_Events > 0:
                fullHistTranslate.SetBinContent(i+1, SS_tight_Events*OS_relaxed_Events/SS_Events)

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
        fullHistTranslate.SetLineColor(r.kPink+1)
        fullHistTranslate.SetLineWidth(2)
        fullHistTranslate.SetLineStyle(2)

        legendHistos[0].append((SS2OS_signal, 'From SS/Tight (%.0f)' %SS2OS_signal.Integral()))
        legendHistos[0].append((relaxed2Signal, 'From OS/Relax (%.0f)' %relaxed2Signal.Integral()))
        #legendHistos[0].append((fullHistTranslate, 'full hist (%.0f)' %fullHistTranslate.Integral()))

        var_background[1].Add(relaxed2Tight)
        var_background[2].Add(SS2OS)
        legendHistos[1].append((relaxed2Tight, 'From SS/Relax (%.0f)' %relaxed2Tight.Integral()))
        legendHistos[2].append((SS2OS, 'From SS/Relax (%.0f)' %SS2OS.Integral()))
        relaxed2Signal = tool.addFakeTHStack(relaxed2Signal,var_background[0])
        SS2OS_signal = tool.addFakeTHStack(SS2OS_signal,var_background[0])
        fullHistTranslate = tool.addFakeTHStack(fullHistTranslate,var_background[0])



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

    psfile = '%s/%s_%s_IsoRatio.pdf' %(location, varName, fileName)
    c = r.TCanvas("c","Test", 800, 1000)
    #ps = r.TPDF(psfile,112)
    c.Divide(2,3)
    drawOpt = ''
    for k in range(6):
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
            var_data[k-1].Draw('PE same')
        legendPosition = (0.63, 0.93 - 0.035*len(legendHistos[k]), 0.93, 0.9)
        l.append(tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos[k]))
        l[k].Draw('same')
        var_signal[k].Draw('same')
    c.Update()
    c.Print('%s(' %psfile)
    c.Clear()
    c.Divide(2,3)

    c.cd(1)
    r.gPad.SetLogy(0)
    QCDDiff.SetTitle('OS/SS MultiJet Relaxed Events %s (%.1f fb^{-1}); %s; OS/SS' %(titleName, Lumi,varName))
    QCDDiff.SetMarkerStyle(8)
    QCDDiff.SetMarkerSize(0.9)
    QCDDiff.SetMaximum(2)
    QCDDiff.SetMinimum(0)
    QCDDiff.Draw('PE')
    if predictPtBin == 'True':
        lFit1 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fit_l,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(fit_l.GetParameter(0), fit_l.GetParError(0))),
                                                         (fit_m,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(fit_m.GetParameter(0), fit_m.GetParError(0))),
                                                         (fit_h,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(fit_h.GetParameter(0), fit_h.GetParError(0)))])
        fit_l.Draw('same')
        fit_m.Draw('same')
        fit_h.Draw('same')
    else:
        fit1.Draw('same')
        lFit1 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fit1,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(fit1.GetParameter(0), fit1.GetParError(0)))])
    lFit1.Draw('same')
    for k in range(5):
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
    c.Clear()
    c.Divide(2,3)
    c.cd(1)
    r.gPad.SetLogy(0)
    QCDDiff2.SetTitle('tight/relaxed MultiJet SS Events %s (%.1f fb^{-1}); %s; tight/relaxed' %(titleName, Lumi,varName))
    QCDDiff2.SetMarkerStyle(8)
    QCDDiff2.SetMarkerSize(0.9)
    QCDDiff2.SetMinimum(0)
    QCDDiff2.SetMaximum(1)
    QCDDiff2.Draw('PE')
    if predictPtBin == 'True':
        lFit2 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fit2_l,'Scale between relaxed/tight in SS region: %.3f \pm %.3f' %(fit2_l.GetParameter(0), fit2_l.GetParError(0))),
                                                         (fit2_m,'Scale between relaxed/tight in SS region: %.3f \pm %.3f' %(fit2_m.GetParameter(0), fit2_m.GetParError(0))),
                                                         (fit2_h,'Scale between relaxed/tight in SS region: %.3f \pm %.3f' %(fit2_h.GetParameter(0), fit2_h.GetParError(0)))])
        fit2_l.Draw('same')
        fit2_m.Draw('same')
        fit2_h.Draw('same')
    else:
        fit2.Draw('same')
        lFit2 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fit2,'Scale between relaxed/tight in SS region: %.3f \pm %.3f' %(fit2.GetParameter(0), fit2.GetParError(0)))])
    lFit2.Draw('same')

    c.Print('%s' %psfile)
    c.Clear()
    c.Divide(2,3)

    lineInfoList = []
    i = 0
    tmpQCDHist2 = QCDHistList[2].Clone()
    tmpQCDHist2.Divide(QCDHistList[4])
    tmpQCDHist1 = QCDHistList[1].Clone()
    tmpQCDHist1.Divide(QCDHistList[3])
    c.cd(1)
    tmpQCDHist1.SetTitle('1.5<iso<4/4<iso<10 OS QCD Events %s (%.1f fb^{-1}); %s; relaxed1/relaxed2' %(titleName, Lumi,varName))
    tmpQCDHist1.GetXaxis().SetTitleOffset(1.2)
    tmpQCDHist1.SetMaximum(0.3)
    tmpQCDHist1.SetMinimum(0)
    tmpQCDHist1.Draw()
    tmpQCDHist1.Fit('Fit0', '0ER')

    l1 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fitList[0],'Ratio between relaxed1/relaxed2: y = %.2f\pm%.2f + (%.4f\pm%.4f)x' %(fitList[0].GetParameter(0), fitList[0].GetParError(0), fitList[0].GetParameter(1), fitList[0].GetParError(1)))])
    l1.Draw('same')
    fitList[0].Draw('same')
    c.cd(2)
    tmpQCDHist2.SetTitle('1.5<iso<4/4<iso<10 SS QCD Events %s (%.1f fb^{-1}); %s; relaxed1/relaxed2' %(titleName, Lumi,varName))
    tmpQCDHist2.SetMaximum(0.3)
    tmpQCDHist2.GetXaxis().SetTitleOffset(1.2)
    tmpQCDHist2.SetMinimum(0)
    tmpQCDHist2.Draw()
    tmpQCDHist2.Fit('Fit1', '0ER')
    l2 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fitList[1],'Ratio between relaxed1/relaxed2: y = %.2f\pm%.2f + (%.4f\pm%.4f)x' %(fitList[1].GetParameter(0), fitList[1].GetParError(0), fitList[1].GetParameter(1), fitList[1].GetParError(1)))])
    l2.Draw('same')
    fitList[1].Draw('same')

    QCDHistList[1].SetTitle('OS Relaxed1 / SS Relaxed1 QCD Events %s (%.1f fb^{-1}); %s; OS/SS' %(titleName, Lumi,varName))
    QCDHistList[3].SetTitle('OS Relaxed2 / SS Relaxed2 QCD Events %s (%.1f fb^{-1}); %s; OS/SS' %(titleName, Lumi,varName))
    QCDHistList[2].SetTitle('SS Relaxed1 / SS Tight QCD Events %s (%.1f fb^{-1}); %s; Relaxed1/SS' %(titleName, Lumi,varName))
    QCDHistList[4].SetTitle('SS Relaxed2 / SS Tight QCD Events %s (%.1f fb^{-1}); %s; Relaxed2/SS' %(titleName, Lumi,varName))

    for k in [1,3]:
        c.cd(k+2)
        QCDHistList[k].Divide(QCDHistList[k+1])
        QCDHistList[k].SetMarkerStyle(8)
        QCDHistList[k].SetMaximum(3)
        QCDHistList[k].SetMinimum(0)
        QCDHistList[k].SetMarkerSize(0.9)
        QCDHistList[k].Draw('PE')
        QCDHistList[k].Fit('Fit%i' %(k+1), '0ER')
        lineInfoList.append(tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fitList[k+1],'Ratio between OS/SS: y = %.3f\pm%.3f + (%.4f\pm%.4f)x' %(fitList[k+1].GetParameter(0), fitList[k+1].GetParError(0), fitList[k+1].GetParameter(1), fitList[k+1].GetParError(1)))]))
        lineInfoList[i].Draw('same')
        fitList[k+1].Draw('same')
        i += 1
    QCDHistList[2].SetMaximum(9)
    QCDHistList[4].SetMaximum(80)

    for k in [2,4]:
        c.cd(k+2)
        QCDHistList[k].Divide(QCDHistList[0])
        QCDHistList[k].SetMarkerStyle(8)
        QCDHistList[k].SetMinimum(0)
        QCDHistList[k].SetMarkerSize(0.9)
        QCDHistList[k].Draw('PE')
        QCDHistList[k].Fit('Fit%i' %(k+1), '0ER')
        lineInfoList.append(tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fitList[k+1],'Ratio between relaxed%i/iso: y = %.3f\pm%.3f + (%.4f\pm%.4f)x' %(k/2,fitList[k+1].GetParameter(0), fitList[k+1].GetParError(0), fitList[k+1].GetParameter(1), fitList[k+1].GetParError(1)))]))
        lineInfoList[i].Draw('same')
        fitList[k+1].Draw('same')
        i += 1

    c.Print('%s)' %psfile)
    #ps.Close()
    print "Plot saved at %s" %(psfile)

op = opts()
if op.varName != 'test':
    getHistos(op.varName, op.signal, op.logy, float(op.sigBoost), int(op.nbins),
           op.useData, float(op.max), float(op.rangeMin), float(op.rangeMax), op.location, op.bTag, op.predict, 'False')

