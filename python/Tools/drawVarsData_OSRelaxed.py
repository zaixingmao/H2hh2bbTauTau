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
import random

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
    parser.add_option("--region", dest="region", default = 'LL', help="")


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
        return 'OS', 'cut-off with iso3'
    elif selection == 6:
        return 'SS', 'cut-off with iso3'

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
    if bTag == 'Loose' and (tree.CSVJ1 >= 0.24 and tree.CSVJ2 >= 0.24):
        passCut = 1
    return passCut

def passCut(tree, bTag, region):

    if bTagSelection(tree, bTag) and abs(tree.eta1.at(0))<2.1 and abs(tree.eta2.at(0))<2.1:
        if tree.iso1.at(0) > 10 or tree.iso2.at(0)>10:
            return 0
        if 1.5<tree.iso1.at(0)<3 and 1.5<tree.iso2.at(0)<3 and (tree.charge1.at(0) + tree.charge2.at(0) == 0):
            return 1
        if 1.5<tree.iso1.at(0)<3 and 1.5<tree.iso2.at(0)<3 and (tree.charge1.at(0) == tree.charge2.at(0)):
            return 2
        if 3<tree.iso1.at(0)<6 and 3<tree.iso2.at(0)<6 and (tree.charge1.at(0) + tree.charge2.at(0) == 0):
            return 3
        if 3<tree.iso1.at(0)<6 and 3<tree.iso2.at(0)<6 and (tree.charge1.at(0) == tree.charge2.at(0)):
            return 4
        if tree.iso1.at(0) > 6 and tree.iso2.at(0) > 6 and (tree.charge1.at(0) + tree.charge2.at(0) == 0):
            return 5
        if tree.iso1.at(0) > 6 and tree.iso2.at(0) > 6 and (tree.charge1.at(0) == tree.charge2.at(0)):
            return 6
        else:
            return 0
    else:
        return 0

def findBin(x, nBins, xMin, xMax):
    bin =  int(nBins*(x-xMin)/(xMax-xMin))
    if bin >= nBins:
        return nBins-1
    else:
        return bin

def findPtScale(select):
    scales = [1, 1.690, 0.352, 0.140]
    return scales[select-1]


def getAccuDist(hist, xMin, xMax, name):
    nBins = hist.GetNbinsX()
    total = hist.Integral()
    accuDist = r.TH1F(name, '', nBins, xMin, xMax)
    for i in range(nBins):
        accuDist.SetBinContent(i+1, hist.Integral(1, i+1)/total)
    return accuDist


def getHistos(varName, signalSelection, logY, sigBoost, nbins, useData, max, rangeMin, rangeMax, location, bTag, predict, predictPtBin, region):
    r.gStyle.SetOptStat(0)
    print "starting ..."
    preFix = 'ClassApp_both_ClassApp_QCD_ClassApp_EWK_TMVARegApp_'

    fileList = [('ZZ', preFix + 'ZZ_eff_all.root', 2500, 5),
                ('WZJetsTo2L2Q', preFix + 'WZJetsTo2L2Q_eff_all.root', 2207, 5),
                ('W1JetsToLNu', preFix + 'W1JetsToLNu_eff2_all.root', 5400000, r.kMagenta-9),
                ('W2JetsToLNu', preFix + 'W2JetsToLNu_eff2_all.root', 1750000, r.kMagenta-9),
                ('W3JetsToLNu', preFix + 'W3JetsToLNu_eff2_all.root', 519000, r.kMagenta-9),
                #('DYJetsToLL', 'TMVARegApp_DYJetsToLL_eff_all.root', 3504000, r.kGreen-7),
                ('DY1JetsToLL', preFix + 'DY1JetsToLL_eff2_all.root', 561000, r.kGreen-7),
                ('DY2JetsToLL', preFix + 'DY2JetsToLL_eff2_all.root', 181000, r.kGreen-7),
                ('DY3JetsToLL', preFix + 'DY3JetsToLL_eff2_all.root', 51100, r.kGreen-7),
                ('tt_full_lep',preFix + 'tt_eff_all.root', 26197.5, r.kRed-7),
                ('tt_semi_lep',preFix + 'tt_semi_eff_all.root', 109281, r.kAzure+7)]

    histList = []
    histList_4QCD = []
    QCDHistList = []
    QCDHistList_withScale = []
    varRange = [nbins, rangeMin, rangeMax]
    nBins = 10000
    Lumi = 19.0
    initNEventsList = []
    legendHistos = []
    var_background = []

    scaleMCPt = 1.0

    tmpFile = []
    tmpTree = []
    var_data = []
    var_data_4QCD = []

    for i in range(6):
        var_data.append(r.TH1F('data_%i' %(i),"", varRange[0], varRange[1], varRange[2]))

    dataName = preFix + 'dataTotal_all.root'
    fData = r.TFile(dataName)
    treeData = fData.Get('eventTree')
    print 'Adding events from: %s ...' %dataName
    for iEntry in range(treeData.GetEntries()):
        treeData.GetEntry(iEntry)
        select = passCut(treeData, bTag, region)
        if select == 0:
            continue
        var_data[select-1].Fill(varsList.findVar(treeData, varName))

    legendHistos.append([])
    for j in range(6):
        var_data[j].SetMarkerStyle(8)
        var_data[j].SetMarkerSize(0.9)
        legendHistos.append([])
        legendHistos[j].append((var_data[j], 'observed (%.0f)' %var_data[j].Integral()))

    for i in range(len(fileList)): 
        for j in range(6):
            histList.append(r.TH1F('%s_%i' %(fileList[i][0],j),fileList[i][0], varRange[0], varRange[1], varRange[2]))
        print 'Adding events from: %s ...' %(fileList[i][1])
        tmpFile.append(r.TFile(fileList[i][1]))
        tmpTree.append(tmpFile[i].Get('eventTree'))
        for iEntry in range(tmpTree[i].GetEntries()):
            tmpTree[i].GetEntry(iEntry)
            select = passCut(tmpTree[i], bTag, region)
            if (select == 0):
                continue
            histList[6*i+select-1].Fill(varsList.findVar(tmpTree[i], varName)*scaleMCPt, tmpTree[i].triggerEff)

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
    MC_List = []
    for i in range(6):
        QCDHistList.append(r.TH1F('QCD_%i' %(i),"", varRange[0], varRange[1], varRange[2]))
        MC_List.append(r.TH1F('MC_total_%i' %(i),"", varRange[0], varRange[1], varRange[2]))
        QCDHistList_withScale.append(r.TH1F('QCD_withScale_%i' %(i),"", varRange[0], varRange[1], varRange[2]))

        for j in range(varRange[0]):
            dataValue = var_data[i].GetBinContent(j+1)
            dataError = var_data[i].GetBinError(j+1)
            MCValue = 0
            for k in range(len(fileList)):
                MCValue +=  histList[6*k+i].GetBinContent(j+1)

            MC_List[i].SetBinContent(j+1, MCValue)
            if dataValue - MCValue > 0:
                QCDHistList[i].SetBinContent(j+1, dataValue - MCValue)
                QCDHistList_withScale[i].SetBinContent(j+1, dataValue - MCValue)
        QCDHistList_withScale[i].Sumw2()
        QCDHistList_withScale[i].Scale(1)

        MC_List[i].Sumw2()

#     for i in range(4):
#         QCDHistList_withScale.append(r.TH1F('QCD_withScale_%i' %(i),"", varRange[0], varRange[1], varRange[2]))
#         for j in range(varRange[0]):
#             dataValue = var_data_4QCD[i].GetBinContent(j+1)
#             MCValue = 0
#             for k in range(len(fileList)):
#                 MCValue +=  histList_4QCD[4*k+i].GetBinContent(j+1)
#             if dataValue - MCValue > 0:
#                 QCDHistList_withScale[i].SetBinContent(j+1, dataValue - MCValue)

    QCDDiff_1 = r.TH1F('QCDDiff_1',"", varRange[0], varRange[1], varRange[2])
    QCDDiff_2 = r.TH1F('QCDDiff_2',"", varRange[0], varRange[1], varRange[2])
    QCDDiff_3 = r.TH1F('QCDDiff_3',"", varRange[0], varRange[1], varRange[2])


    fit1 = r.TF1("fit1","[0]", varRange[1],varRange[2])
    fit1.SetParName(0,'scale')
    fit1.FixParameter(0,1.0)

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
                select = passCut(treeSignal, bTag, region)
                if (not select):
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


        QCDHistList_withScale[5].SetLineColor(r.kSpring+1)
        QCDHistList_withScale[3].SetLineColor(r.kOrange-4)
        QCDHistList_withScale[1].SetLineColor(r.kRed)
        QCDHistList_withScale[1].SetLineStyle(2)
        QCDHistList_withScale[3].SetLineStyle(2)
        QCDHistList_withScale[5].SetLineStyle(2)


        legendHistos[0].append((QCDHistList_withScale[1], 'From LL iso 1.5~3 (%.0f)' %QCDHistList_withScale[1].Integral()))
        legendHistos[2].append((QCDHistList_withScale[3], 'From LL iso 3~6 (%.0f)' %QCDHistList_withScale[3].Integral()))
        legendHistos[4].append((QCDHistList_withScale[5], 'From LL iso 6~10 (%.0f)' %QCDHistList_withScale[5].Integral()))

        QCDDiff_1_sub = r.TH1F('QCDDiff_1_sub',"", varRange[0], varRange[1], varRange[2])
        QCDDiff_2_sub = r.TH1F('QCDDiff_2_sub',"", varRange[0], varRange[1], varRange[2])
        QCDDiff_3_sub = r.TH1F('QCDDiff_3_sub',"", varRange[0], varRange[1], varRange[2])

        QCDDiff_1_sub.Add(QCDHistList_withScale[1], MC_List[0])
        QCDDiff_2_sub.Add(QCDHistList_withScale[3], MC_List[2])
        QCDDiff_3_sub.Add(QCDHistList_withScale[5], MC_List[4])

        QCDHistList_withScale[1] = tool.addFakeTHStack(QCDHistList_withScale[1],var_background[0])
        QCDHistList_withScale[3] = tool.addFakeTHStack(QCDHistList_withScale[3],var_background[2])
        QCDHistList_withScale[5] = tool.addFakeTHStack(QCDHistList_withScale[5],var_background[4])

    QCDDiff_list = []
    QCDDiff_list.append(r.TH1F('QCDDiff_1',"", varRange[0], varRange[1], varRange[2]))
    QCDDiff_list.append(r.TH1F('QCDDiff_2',"", varRange[0], varRange[1], varRange[2]))
    QCDDiff_list.append(r.TH1F('QCDDiff_3',"", varRange[0], varRange[1], varRange[2]))

    QCDDiff_list[0].Add(var_data[0])
    QCDDiff_list[1].Add(var_data[2])
    QCDDiff_list[2].Add(var_data[4])

    QCDDiff_list[0].Divide(QCDDiff_1_sub)
    QCDDiff_list[1].Divide(QCDDiff_2_sub)
    QCDDiff_list[2].Divide(QCDDiff_3_sub)

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
    elif bTag == 'Loose':
        titleName = 'Loose b-tag'
        fileName = 'loose_bTag'


    maxList = [30, 80, 200]

    psfile = '%s/%s_%s_OSCompare.pdf' %(location, varName, fileName)
    c = r.TCanvas("c","Test", 1200, 800)
#     ps = r.TPDF(psfile,112)
    c.Divide(3,2)

    for i in range(3):
        c.cd(i+1)
        var_background[2*i].SetTitle('OS Relaxed Events %s (%.1f fb^{-1}); %s; events / bin' %(titleName, Lumi,varName))
        var_background[2*i].SetMaximum(maxList[i])
        var_background[2*i].SetMinimum(0.0)
        var_background[2*i].Draw()
        var_data[2*i].Draw('PE same')
        QCDHistList_withScale[2*i+1].SetLineWidth(2)
        QCDHistList_withScale[2*i+1].Draw('sameE')
        legendPosition = (0.55, 0.93 - 0.03*len(legendHistos[2*i]), 0.85, 0.9)
        l.append(tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos[2*i]))
        l[i].Draw('same')
        c.Update()
    
    fit1.SetLineStyle(2)

    for i in range(3):
        c.cd(i+4)
        QCDDiff_list[i].Draw('PE')
        fit1.Draw('same')
        c.Update()

    c.Print('%s' %psfile)

    print "Plot saved at %s" %(psfile)
    c.Close()

op = opts()
if op.varName != 'test':
    getHistos(op.varName, op.signal, op.logy, float(op.sigBoost), int(op.nbins),
           op.useData, float(op.max), float(op.rangeMin), float(op.rangeMax), op.location, op.bTag, op.predict, 'False', op.region)

