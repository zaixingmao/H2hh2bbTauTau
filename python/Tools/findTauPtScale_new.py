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
    parser.add_option("--scale", dest="scale", default = 1, help="")
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

def passCut(tree, bTag):
#     if tree.tauDecayMode1 != 10:
#         return 0

#     if  tree.iso1.at(0)>1.5  and tree.iso2.at(0)>1.5:
#           return 0
    isoCut = 3

    if  tree.iso1.at(0)>isoCut  and tree.iso2.at(0)<1.5:
          return 0
    if  tree.iso1.at(0)<1.5  and tree.iso2.at(0)>isoCut:
          return 0

    if bTagSelection(tree, bTag) and abs(tree.eta1.at(0))<2.1 and abs(tree.eta2.at(0))<2.1:
        iso_count = 3
        sign_count = 0
        maxIso = 10
        if  tree.iso1.at(0)>isoCut  and tree.iso2.at(0)>isoCut:
            iso_count = 1
        if (tree.iso1.at(0)>isoCut and tree.iso2.at(0)<1.5) or (tree.iso2.at(0)>isoCut and tree.iso1.at(0)<1.5):
            iso_count = 1
        if  tree.iso1.at(0) > maxIso  or tree.iso2.at(0) > maxIso:
            iso_count = 3
        if tree.charge1.at(0) -  tree.charge2.at(0) == 0:
            sign_count = 1
        if tree.iso1.at(0)<1.5  and tree.iso2.at(0)<1.5:
            iso_count = 0
        return (iso_count<<1) + sign_count + 1
    else:
        return 0

def findBin(x, nBins, xMin, xMax):
    bin =  int(nBins*(x-xMin)/(xMax-xMin))
    if bin >= nBins:
        return nBins-1
    else:
        return bin

def findCorrectBin(pt1, pt2, scale):
    if scale == 1:
        ptRange = [70, 120]
    else:
        ptRange = [10000, 10000]

    if pt1 < ptRange[0]:
        return 0.5
    elif (ptRange[0] < pt1 < ptRange[1]) and pt2 < ptRange[0]:
        return 1.5
    elif (ptRange[0] < pt1 < ptRange[1]) and (ptRange[0] < pt2 < ptRange[1]):
        return 2.5
    elif (ptRange[1] < pt1) and (pt2 < ptRange[0]):
        return 3.5
    elif (ptRange[1] < pt1) and (ptRange[0] < pt2 < ptRange[1]):
        return 4.5
    elif (ptRange[1] < pt1) and (ptRange[1] < pt2):
        return 5.5

def rangeName(i):
    nameList = ['r1*r1', 'r2*r1', 'r2*r2', 'r3*r1', 'r3*r2', 'r3*r3']
    return nameList[i]

def getHistos(varName, signalSelection, logY, sigBoost, nbins, useData, max, rangeMin, rangeMax, location, bTag, predict, predictPtBin, scale, region):
    r.gStyle.SetOptStat(0)
    preFix = 'ClassApp_both_ClassApp_QCD_ClassApp_EWK_TMVARegApp_'

    fileList = [('ZZ', preFix + 'ZZ_eff_all.root', 2500, 5),
                ('WZJetsTo2L2Q', preFix + 'WZJetsTo2L2Q_eff_all.root', 2207, 5),
                ('tt_full_lep',preFix + 'tt_eff_all.root', 26197.5, r.kRed-7),
                ('tt_semi_lep',preFix + 'tt_semi_eff_all.root', 109281, r.kAzure+7),
                #('DYJetsToLL', 'TMVARegApp_DYJetsToLL_eff_all.root', 3504000, r.kGreen-7),
                ('DY1JetsToLL', preFix + 'DY1JetsToLL_eff2_all.root', 561000, r.kGreen-7),
                ('DY2JetsToLL', preFix + 'DY2JetsToLL_eff2_all.root', 181000, r.kGreen-7),
                ('DY3JetsToLL', preFix + 'DY3JetsToLL_eff2_all.root', 51100, r.kGreen-7),
                ('W1JetsToLNu', preFix + 'W1JetsToLNu_eff2_all.root', 5400000, r.kMagenta-9),
                ('W2JetsToLNu', preFix + 'W2JetsToLNu_eff2_all.root', 1750000, r.kMagenta-9),
                ('W3JetsToLNu', preFix + 'W3JetsToLNu_eff2_all.root', 519000, r.kMagenta-9)]

    varName = "ptRange"
    histList = []
    QCDHistList = []
    varRange = [6, 0, 6]
    Lumi = 19.0
    initNEventsList = []
    legendHistos = []
    var_background = []
    ptBins = [varRange[1], 70, 120, varRange[2]]
    bins = array('f', ptBins)
    scaleMCPt = 1

    tmpFile = []
    tmpTree = []
    var_data = []

    for i in range(3):
#         var_data.append(r.TH1F('data_%i' %(i),"", len(ptBins)-1, bins))
        var_data.append(r.TH1F('data_%i' %(i),"", 6, 0, 6))

    dataName = preFix + 'dataTotal_all.root'
    fData = r.TFile(dataName)
    treeData = fData.Get('eventTree')
    print 'Adding events from: %s ...' %dataName
    for iEntry in range(treeData.GetEntries()):
        treeData.GetEntry(iEntry)
        select = passCut(treeData, bTag)
        if (select == 0) or (select == 1) or (select > 4):
            continue
#         var_data[select-2].Fill(treeData.pt1.at(0))
#         var_data[select-2].Fill(treeData.pt2.at(0))
        var_data[select-2].Fill(findCorrectBin(treeData.pt1.at(0), treeData.pt2.at(0), scale))

    legendHistos.append([])
    for j in range(3):
        var_data[j].SetMarkerStyle(8)
        var_data[j].SetMarkerSize(0.9)
        legendHistos.append([])
        legendHistos[j+1].append((var_data[j], 'observed (%.0f)' %var_data[j].Integral()))

    for i in range(len(fileList)): 
        for j in range(4):
#             histList.append(r.TH1F('%s_%i' %(fileList[i][0],j),fileList[i][0], len(ptBins)-1, bins))
            histList.append(r.TH1F('%s_%i' %(fileList[i][0],j),fileList[i][0], 6, 0, 6))

        print 'Adding events from: %s ...' %(fileList[i][1])
        tmpFile.append(r.TFile(fileList[i][1]))
        tmpTree.append(tmpFile[i].Get('eventTree'))
        for iEntry in range(tmpTree[i].GetEntries()):
            tmpTree[i].GetEntry(iEntry)
            select = passCut(tmpTree[i], bTag)
            if (not select) or (select > 4):
                continue
#             histList[4*i+select-1].Fill(tmpTree[i].pt1.at(0)*scaleMCPt, tmpTree[i].triggerEff)
#             histList[4*i+select-1].Fill(tmpTree[i].pt2.at(0)*scaleMCPt, tmpTree[i].triggerEff)
            histList[4*i+select-1].Fill(findCorrectBin(tmpTree[i].pt1.at(0), tmpTree[i].pt2.at(0), scale), tmpTree[i].triggerEff)

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
#         QCDHistList.append(r.TH1F('QCD_%i' %(i),"", len(ptBins)-1, bins))
        QCDHistList.append(r.TH1F('QCD_%i' %(i),"", 6, 0, 6))

        for j in range(6):
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

    QCDDiff = r.TH1F('QCD_diff',"", 6, 0, 6)
    QCDDiff2 = r.TH1F('QCD_diff2',"", 6, 0, 6)

    QCDDiff = QCDHistList[1].Clone()
    QCDDiff.Divide(QCDHistList[2])
    QCDDiff.Sumw2()
    QCDDiff2 = QCDHistList[0].Clone()
    QCDDiff2.Divide(QCDHistList[2])
    QCDDiff2.Sumw2()

    DrawSignal = False
    if signalSelection != '':
        var_signal = []
        for i in range(4):
#             var_signal.append(r.TH1F('%s_%i' %(signalSelection,i),"", len(ptBins)-1, bins))
            var_signal.append(r.TH1F('%s_%i' %(signalSelection,i),"", 6, 0, 6))

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
#                 var_signal[select-1].Fill(treeSignal.pt1.at(0), treeSignal.triggerEff)
#                 var_signal[select-1].Fill(treeSignal.pt2.at(0), treeSignal.triggerEff)
                var_signal[select-1].Fill(findCorrectBin(treeSignal.pt1.at(0), treeSignal.pt2.at(0), scale), treeSignal.triggerEff)

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
#         relaxed2Tight = r.TH1F('relaxed2Tight','', len(ptBins)-1, bins)
#         SS2OS = r.TH1F('SS2OS','', len(ptBins)-1, bins)
#         relaxed2Signal = r.TH1F('relaxed2Signal','', len(ptBins)-1, bins)
#         SS2OS_signal = r.TH1F('SS2OS_signal','', len(ptBins)-1, bins)
#         fullHistTranslate = r.TH1F('fullHistTranslate','', len(ptBins)-1, bins)

        relaxed2Tight = r.TH1F('relaxed2Tight','', 6, 0, 6)
        SS2OS = r.TH1F('SS2OS','', 6, 0, 6)
        relaxed2Signal = r.TH1F('relaxed2Signal','', 6, 0, 6)
        SS2OS_signal = r.TH1F('SS2OS_signal','', 6, 0, 6)

#         scale_SS2OS_l = QCDDiff.GetBinContent(1)
#         scale_er_SS2OS_l = QCDDiff.GetBinError(1)
#         scale_relaxed2Tight_l = QCDDiff2.GetBinContent(1)
#         scale_er_relaxed2Tight_l = QCDDiff2.GetBinError(1)
#         scale_SS2OS_m = QCDDiff.GetBinContent(2)
#         scale_er_SS2OS_m = QCDDiff.GetBinError(2)
#         scale_relaxed2Tight_m = QCDDiff2.GetBinContent(2)
#         scale_er_relaxed2Tight_m = QCDDiff2.GetBinError(2)
#         scale_SS2OS_h = QCDDiff.GetBinContent(3)
#         scale_er_SS2OS_h = QCDDiff.GetBinError(3)
#         scale_relaxed2Tight_h = QCDDiff2.GetBinContent(3)
#         scale_er_relaxed2Tight_h = QCDDiff2.GetBinError(3)

        scale1 = []
        scale2 = []

        for i in range(varRange[0]):
            scale1.append((QCDDiff.GetBinContent(1+i), QCDDiff.GetBinError(1+i)))
            scale2.append((QCDDiff2.GetBinContent(1+i), QCDDiff2.GetBinError(1+i)))

            SS_tight_Events = QCDHistList[0].GetBinContent(i+1)
            SS_tight_Error = QCDHistList[0].GetBinError(i+1)
            OS_relaxed_Events = QCDHistList[1].GetBinContent(i+1)
            OS_relaxed_Error = QCDHistList[1].GetBinError(i+1)
            SS_Events = QCDHistList[2].GetBinContent(i+1)
            SS_Error = QCDHistList[2].GetBinError(i+1)

#             if predictPtBin == 'True':
#                 ptValue1 = QCDHistList[0].GetBinCenter(i+1)
#                 ptValue2 = QCDHistList[1].GetBinCenter(i+1)
#                 if ptValue1 <= ptBins[1]:
#                     scale_1 = scale_relaxed2Tight_l
#                 elif ptValue1 <= ptBins[2]:
#                     scale_1 = scale_relaxed2Tight_m
#                 elif ptValue1 > ptBins[2]:
#                     scale_1 = scale_relaxed2Tight_h
# 
#                 if ptValue2 <= ptBins[1]:
#                     scale_2 = scale_SS2OS_l
#                 elif ptValue2 <= ptBins[2]:
#                     scale_2 = scale_SS2OS_m
#                 elif ptValue2 > ptBins[2]:
#                     scale_2 = scale_SS2OS_h

#             relaxed2Tight.SetBinContent(i+1, scale_1*SS_Events)
#             relaxed2Signal.SetBinContent(i+1, scale_1*OS_relaxed_Events)
#             SS2OS.SetBinContent(i+1, scale_2*SS_Events)
#             SS2OS_signal.SetBinContent(i+1, scale_2*SS_tight_Events)

            relaxed2Tight.SetBinContent(i+1, scale2[i][0]*SS_Events)
            relaxed2Signal.SetBinContent(i+1, scale2[i][0]*OS_relaxed_Events)
            SS2OS.SetBinContent(i+1, scale1[i][0]*SS_Events)
            SS2OS_signal.SetBinContent(i+1, scale1[i][0]*SS_tight_Events)


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
        #legendHistos[0].append((fullHistTranslate, 'full hist (%.0f)' %fullHistTranslate.Integral()))

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
    elif bTag == 'Loose':
        titleName = 'Loose b-tag'
        fileName = 'loose_bTag'

    psfile = '%s/%s_%s_%i.pdf' %(location, varName, fileName, scale)
    c = r.TCanvas("c","Test", 800, 600)
    #ps = r.TPDF(psfile,112)
    c.Divide(2,2)
    drawOpt = ''
    for k in range(4):
        c.cd(k+1)
        r.gPad.SetTicky()
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
    c.cd(1)
    r.gPad.SetLogy(0)
    QCDDiff.SetTitle('OS/SS MultiJet Relaxed Events %s (%.1f fb^{-1}); %s; OS/SS' %(titleName, Lumi,varName))
    QCDDiff.SetMarkerStyle(8)
    QCDDiff.SetMarkerSize(0.9)
    QCDDiff.SetMaximum(4)
    QCDDiff.SetMinimum(0)
    QCDDiff.Draw('PE')

    f1 = []
    fFind = []
    f1List = []
    r1_1 = r.sqrt(scale1[0][0])
    r1_2 = scale1[1][0]/r1_1
    r1_3 = scale1[3][0]/r1_1
    scaleList1 = [r1_1*r1_1, r1_1*r1_2, r1_2*r1_2, r1_3*r1_1, r1_3*r1_2, r1_3*r1_3]

    for k in range(varRange[0]):
        f1.append(r.TGraph(4))
        f1[k].SetPoint(0, k,scale1[k][0]+scale1[k][1])
        f1[k].SetPoint(3, k,scale1[k][0]-scale1[k][1])
        f1[k].SetPoint(1, k+1,scale1[k][0]+scale1[k][1])
        f1[k].SetPoint(2, k+1,scale1[k][0]-scale1[k][1])
        f1[k].SetFillStyle(3001)
        f1[k].SetFillColor(k+1)
        f1List.append((f1[k],'Scale in region %s: %.2f \pm %.2f' %(rangeName(k), scale1[k][0], scale1[k][1])))
        f1[k].Draw('fsame')
        fFind.append(r.TF1('fFind%i' %k, '%f' %scaleList1[k], k, k+1))
        fFind[k].Draw('same')

#     flErr = r.TGraph(4)
#     flErr.SetPoint(0, ptBins[0],QCDDiff.GetBinContent(1)+QCDDiff.GetBinError(1))
#     flErr.SetPoint(3, ptBins[0],QCDDiff.GetBinContent(1)-QCDDiff.GetBinError(1))
#     flErr.SetPoint(1, ptBins[1],QCDDiff.GetBinContent(1)+QCDDiff.GetBinError(1))
#     flErr.SetPoint(2, ptBins[1],QCDDiff.GetBinContent(1)-QCDDiff.GetBinError(1))
#     flErr.SetFillStyle(3001)
#     flErr.SetFillColor(r.kRed)
#     fmErr = r.TGraph(4)
#     fmErr.SetPoint(0, ptBins[1],QCDDiff.GetBinContent(2)+QCDDiff.GetBinError(2))
#     fmErr.SetPoint(3, ptBins[1],QCDDiff.GetBinContent(2)-QCDDiff.GetBinError(2))
#     fmErr.SetPoint(1, ptBins[2],QCDDiff.GetBinContent(2)+QCDDiff.GetBinError(2))
#     fmErr.SetPoint(2, ptBins[2],QCDDiff.GetBinContent(2)-QCDDiff.GetBinError(2))
#     fmErr.SetFillStyle(3001)
#     fmErr.SetFillColor(r.kBlue)
#     fhErr = r.TGraph(4)
#     fhErr.SetPoint(0, ptBins[2],QCDDiff.GetBinContent(3)+QCDDiff.GetBinError(3))
#     fhErr.SetPoint(3, ptBins[2],QCDDiff.GetBinContent(3)-QCDDiff.GetBinError(3))
#     fhErr.SetPoint(1, ptBins[3],QCDDiff.GetBinContent(3)+QCDDiff.GetBinError(3))
#     fhErr.SetPoint(2, ptBins[3],QCDDiff.GetBinContent(3)-QCDDiff.GetBinError(3))
#     fhErr.SetFillStyle(3001)
#     fhErr.SetFillColor(r.kGreen)
#     flErr.Draw('fsame')
#     fmErr.Draw('fsame')
#     fhErr.Draw('fsame')

 #    lFit1 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(flErr,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(QCDDiff.GetBinContent(1), QCDDiff.GetBinError(1))),
#                                                      (fmErr,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(QCDDiff.GetBinContent(2), QCDDiff.GetBinError(2))),
#                                                      (fhErr,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(QCDDiff.GetBinContent(3), QCDDiff.GetBinError(3)))])
    f1List.append((fFind[0], 'r1: %.2f' %r1_1))
    f1List.append((fFind[0], 'r2: %.2f' %r1_2))
    f1List.append((fFind[0], 'r3: %.2f' %r1_3))
    lFit1 = tool.setMyLegend((0.25, 0.5, 0.9, 0.85), f1List)
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
    QCDDiff2.SetMaximum(0.2)
    QCDDiff2.Draw('PE')

    f2 = []
    f2Find = []
    f2List = []
    r2_1 = r.sqrt(scale2[0][0])
    r2_2 = scale2[1][0]/r2_1
    r2_3 = scale2[3][0]/r2_1
    scaleList2 = [r2_1*r2_1, r2_1*r2_2, r2_2*r2_2, r2_3*r2_1, r2_3*r2_2, r2_3*r2_3]

    for k in range(varRange[0]):
        f2.append(r.TGraph(4))
        f2[k].SetPoint(0, k,scale2[k][0]+scale2[k][1])
        f2[k].SetPoint(3, k,scale2[k][0]-scale2[k][1])
        f2[k].SetPoint(1, k+1,scale2[k][0]+scale2[k][1])
        f2[k].SetPoint(2, k+1,scale2[k][0]-scale2[k][1])
        f2[k].SetFillStyle(3001)
        f2[k].SetFillColor(k+1)
        f2List.append((f2[k],'Scale in region %s: %.3f \pm %.3f' %(rangeName(k), scale2[k][0], scale2[k][1])))
        f2[k].Draw('fsame') 
        f2Find.append(r.TF1('f2Find%i' %k, '%f' %scaleList2[k], k, k+1))
        f2Find[k].Draw('same')

 #    flErr2 = r.TGraph(4)
#     flErr2.SetPoint(0, ptBins[0],QCDDiff2.GetBinContent(1)+QCDDiff2.GetBinError(1))
#     flErr2.SetPoint(3, ptBins[0],QCDDiff2.GetBinContent(1)-QCDDiff2.GetBinError(1))
#     flErr2.SetPoint(1, ptBins[1],QCDDiff2.GetBinContent(1)+QCDDiff2.GetBinError(1))
#     flErr2.SetPoint(2, ptBins[1],QCDDiff2.GetBinContent(1)-QCDDiff2.GetBinError(1))
#     flErr2.SetFillStyle(3001)
#     flErr2.SetFillColor(r.kRed)
#     fmErr2 = r.TGraph(4)
#     fmErr2.SetPoint(0, ptBins[1],QCDDiff2.GetBinContent(2)+QCDDiff2.GetBinError(2))
#     fmErr2.SetPoint(3, ptBins[1],QCDDiff2.GetBinContent(2)-QCDDiff2.GetBinError(2))
#     fmErr2.SetPoint(1, ptBins[2],QCDDiff2.GetBinContent(2)+QCDDiff2.GetBinError(2))
#     fmErr2.SetPoint(2, ptBins[2],QCDDiff2.GetBinContent(2)-QCDDiff2.GetBinError(2))
#     fmErr2.SetFillStyle(3001)
#     fmErr2.SetFillColor(r.kBlue)
#     fhErr2 = r.TGraph(4)
#     fhErr2.SetPoint(0, ptBins[2],QCDDiff2.GetBinContent(3)+QCDDiff2.GetBinError(3))
#     fhErr2.SetPoint(3, ptBins[2],QCDDiff2.GetBinContent(3)-QCDDiff2.GetBinError(3))
#     fhErr2.SetPoint(1, ptBins[3],QCDDiff2.GetBinContent(3)+QCDDiff2.GetBinError(3))
#     fhErr2.SetPoint(2, ptBins[3],QCDDiff2.GetBinContent(3)-QCDDiff2.GetBinError(3))
#     fhErr2.SetFillStyle(3001)
#     fhErr2.SetFillColor(r.kGreen)
#     flErr2.Draw('fsame')
#     fmErr2.Draw('fsame')
#     fhErr2.Draw('fsame')
#     lFit2 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(flErr2,'Scale between relaxed/tight in SS region: %.3f \pm %.3f' %(QCDDiff2.GetBinContent(1), QCDDiff2.GetBinError(1))),
#                                                      (fmErr2,'Scale between relaxed/tight in SS region: %.3f \pm %.3f' %(QCDDiff2.GetBinContent(2), QCDDiff2.GetBinError(2))),
#                                                     (fhErr2,'Scale between relaxed/tight in SS region: %.3f \pm %.3f' %(QCDDiff2.GetBinContent(3), QCDDiff2.GetBinError(3)))])
#     lFit2.Draw('same')
    f2List.append((f2Find[0], 'r1: %.2f' %r2_1))
    f2List.append((f2Find[0], 'r2: %.2f' %r2_2))
    f2List.append((f2Find[0], 'r3: %.2f' %r2_3))
    lFit2 = tool.setMyLegend((0.15, 0.6, 0.9, 0.85), f2List)
    lFit2.Draw('same')

    c.Print('%s)' %psfile)
    #ps.Close()
    print "Plot saved at %s" %(psfile)

op = opts()
if op.varName != 'test':
    getHistos(op.varName, op.signal, op.logy, float(op.sigBoost), int(op.nbins),
           op.useData, float(op.max), float(op.rangeMin), float(op.rangeMax), op.location, op.bTag, op.predict, 'True', int(op.scale), op.region)


