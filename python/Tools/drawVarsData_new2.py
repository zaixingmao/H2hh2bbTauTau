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
    return passCut

def passCut(tree, bTag, region):
    if bTagSelection(tree, bTag) and abs(tree.eta1.at(0))<2.1 and abs(tree.eta2.at(0))<2.1:
        iso_count = 0
        sign_count = 0
        if varsList.findVar(tree, 'dEtaTauTau') > 1:
            return 0
        if region == 'LL':
            if  tree.iso1.at(0)>1.5  and tree.iso2.at(0)<1.5:
                  return 0
            if  tree.iso1.at(0)<1.5  and tree.iso2.at(0)>1.5:
                  return 0
        elif region == 'LT':
            if  tree.iso1.at(0)>1.5  and tree.iso2.at(0)>1.5:
                return 0
            if  tree.iso1.at(0)<1.5  and tree.iso2.at(0)>1.5:
                  return 0
        elif region == 'TL':
            if  tree.iso1.at(0)>1.5  and tree.iso2.at(0)>1.5:
                return 0
            if  tree.iso1.at(0)>1.5  and tree.iso2.at(0)<1.5:
                  return 0
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

def fitMultiDimension(n, MC_i, data_r, MC_r,y,e):
    func = r.TF3("func","[0]*x +[1]*y - [1]*[0]*z", 0, 200, 0, 2000, 0, 300)
    func.SetParameters(1, 0.5)
    func.SetParLimits(0, 0.9, 1.1)
    dataHist = r.TH3F('dataHist','', 200, 0, 200, 1000, 0, 2000, 300, 0, 300)
    for i in range(n):
        bin_x = findBin(MC_i[i], 200, 0, 200)
        bin_y = findBin(data_r[i], 1000, 0, 2000)
        bin_z = findBin(MC_r[i], 300, 0, 300)
        dataHist.SetBinContent(bin_x, bin_y, bin_z, y[i])
        dataHist.SetBinError(bin_x, bin_y, bin_z, e[i])

    dataHist.Fit(func, '0E')
    return func.GetParameter(0), func.GetParameter(1)

def addFakeTHStack(hist, stack):
    for iHist in stack.GetHists():
        for i in range(iHist.GetNbinsX()):
            currentValue = hist.GetBinContent(i+1)
            hist.SetBinContent(i+1,currentValue + iHist.GetBinContent(i+1))
    return hist

def getHistos(varName, signalSelection, logY, sigBoost, nbins, useData, max, rangeMin, rangeMax, location, bTag, predict, region):
    r.gStyle.SetOptStat(0)
    preFix = 'ClassApp_both_ClassApp_QCD_ClassApp_EWK_TMVARegApp_'

    fileList = [# ('ZZ', preFix + 'ZZ_eff_all.root', 2500, 5),
#                 ('tt_full_lep',preFix+'tt_eff_all.root', 26197.5, r.kRed-7),
#                 ('tt_semi_lep',preFix+'tt_semi_eff_all.root', 109281, r.kAzure+7),
#                 ('DYJetsToLL', 'DYJetsToLL_eff_all.root', 3504000, r.kGreen-7),
#                 ('DY2JetsToLL', preFix+'DY2JetsToLL_eff_all.root', 181000, r.kGreen-7),
#                 ('DY3JetsToLL', preFix+'DY3JetsToLL_eff_all.root', 51100, r.kGreen-7),
#                 ('W1JetsToLNu', preFix+'W1JetsToLNu_eff_all.root', 5400000, r.kMagenta-9),
#                 ('W2JetsToLNu', preFix+'W2JetsToLNu_eff_all.root', 1750000, r.kMagenta-9),
#                 ('W3JetsToLNu', preFix+'W3JetsToLNu_eff_all.root', 519000, r.kMagenta-9)
                ('QCD', preFix+'QCD_Pt-50to80_all.root', 519000, r.kOrange-4)]
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
    dataName = preFix + 'dataTotal_all.root'
    fData = r.TFile(dataName)
    treeData = fData.Get('eventTree')
    print 'Adding events from: %s ...' %dataName
    for iEntry in range(treeData.GetEntries()):
        treeData.GetEntry(iEntry)
        select = passCut(treeData, bTag, region)
        continue
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
            select = passCut(tmpTree[i], bTag, region)
            if not select:
                continue
            histList[4*i+select-1].Fill(varsList.findVar(tmpTree[i], varName), 1)#tmpTree[i].triggerEff)
    
        initNEventsList.append(tmpFile[i].Get('preselection'))
        for j in range(4):
            var_background.append(r.THStack())
#             histList[4*i+j].SetFillColor(fileList[i][3])
#             histList[4*i+j].Scale(fileList[i][2]*Lumi/initNEventsList[i].GetBinContent(1))
            var_background[j].Add(histList[4*i+j])
            legendHistos[j].append((histList[4*i+j], '%s (%.2f)' %(fileList[i][0], histList[4*i+j].Integral())))

    data_i = []
    MC_i = []
    data_r = []
    MC_r = []
    e  = []
    data_o = []
    MC_o = []
    e_o = []

    for i in range(3):
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
            elif i == 1:
                data_o.append(dataValue)
                e_o.append(dataError)
                MC_o.append(MCValue)
            elif i == 2:
                data_r.append(dataValue)
                MC_r.append(MCValue)

    DrawSignal = False
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
            for iEntry in range(treeSignal.GetEntries()):
                treeSignal.GetEntry(iEntry)
                select = passCut(treeSignal, bTag, region)
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
        scale_mc, scale_qcd = fitMultiDimension(varRange[0], MC_i, data_r, MC_r, data_i, e)
        scale_mc2, scale_qcd2 = fitMultiDimension(varRange[0], MC_o, data_r, MC_r, data_o, e_o)
        relaxed2Tight = r.TH1F('relaxed2Tight','', varRange[0], varRange[1], varRange[2])
        sameS2OppositeS = r.TH1F('sameS2OppositeS','', varRange[0], varRange[1], varRange[2])
        ss_tight = r.TH1F('ss_tight','', varRange[0], varRange[1], varRange[2])
        os_relaxed = r.TH1F('os_relaxed','', varRange[0], varRange[1], varRange[2])
        ost_fromRelaxed = r.TH1F('ost_fromRelaxed','', varRange[0], varRange[1], varRange[2])
        ost_fromSameSign = r.TH1F('ost_fromSameSign','', varRange[0], varRange[1], varRange[2])

        for i in range(len(fileList)):
            histList[4*i+1].Scale(scale_mc)
            histList[4*i+2].Scale(scale_mc2)
            legendHistos[1][i+1] = (histList[4*i+1], '%s x%.2f (%.2f)' %(fileList[i][0], scale_mc,histList[4*i+1].Integral()))
            legendHistos[2][i+1] = (histList[4*i+2], '%s x%.2f (%.2f)' %(fileList[i][0], scale_mc2,histList[4*i+2].Integral()))
            for i in range(varRange[0]):
                relaxed2Tight.SetBinContent(i+1, scale_qcd*(data_r[i]-MC_r[i]*scale_mc))
                sameS2OppositeS.SetBinContent(i+1, scale_qcd2*(data_r[i]-MC_r[i]*scale_mc2))
                ost_fromRelaxed.SetBinContent(i+1, scale_qcd*(data_o[i]-MC_o[i]*scale_mc))
                ost_fromSameSign.SetBinContent(i+1, scale_qcd2*(data_i[i]-MC_i[i]*scale_mc2))
                    
                ss_tight.SetBinContent(i+1, data_i[i]-MC_i[i])
                os_relaxed.SetBinContent(i+1, data_o[i]-MC_o[i])

        ost_fromSameSign.SetLineColor(r.kSpring+1)
        ost_fromRelaxed.SetLineColor(r.kOrange-4)
        ost_fromSameSign.SetLineWidth(2)
        ost_fromRelaxed.SetLineWidth(2)
        ost_fromRelaxed.SetLineStyle(2)
        relaxed2Tight.SetFillColor(r.kSpring+1)
        sameS2OppositeS.SetFillColor(r.kOrange-4)
        legendHistos[1].append((relaxed2Tight, 'From SS/Relax (%.0f)' %relaxed2Tight.Integral()))
        legendHistos[2].append((sameS2OppositeS, 'From SS/Relax (%.0f)' %sameS2OppositeS.Integral()))
        legendHistos[0].append((ost_fromSameSign, 'From SS/Tight (%.0f)' %ost_fromSameSign.Integral()))
        legendHistos[0].append((ost_fromRelaxed, 'From OS/Relax (%.0f)' %ost_fromRelaxed.Integral()))
        var_background[1].Add(relaxed2Tight)
        var_background[2].Add(sameS2OppositeS)

        ost_fromRelaxed = tool.addFakeTHStack(ost_fromRelaxed,var_background[0], scale_mc)
        ost_fromSameSign = tool.addFakeTHStack(ost_fromSameSign,var_background[0], scale_mc2)

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

    psfile = '%s/%s_%s_all.pdf' %(location, varName, fileName)
    c = r.TCanvas("c","Test", 800, 600)
#     if varName == 'BDT_both':
#         r.gPad.SetLogy()
    histList[2].SetTitle('Relaxed Events dEtaTauTau < 1 %s ; %s; events / bin' %(titleName,varName))
#     histList[2].SetMaximum(100)
    histList[2].SetMinimum(0)
    histList[2].SetLineColor(r.kRed)
    histList[2].SetLineWidth(2)
    histList[3].SetLineWidth(2)
    histList[2].Draw()
    histList[3].Draw('same')
    histList[3].SetLineColor(r.kBlue)
    histList[3].SetLineStyle(2)
    var_signal[0].SetLineColor(r.kBlack)
    var_signal[0].SetLineStyle(2)
    var_signal[0].Draw('same')

    l1 = tool.setMyLegend(lPosition=(0.5,0.7,0.93,0.8), lHistList=[(histList[2], 'OS QCD (%.2f)' %histList[2].Integral()),
                                                                   (histList[3], 'SS QCD (%.2f)' %histList[3].Integral())])
    l1.Draw('same')

    #ps = r.TPDF(psfile,112)
#     c.Divide(2,2)
#     drawOpt = ''
#     for k in range(4):
#         c.cd(k+1)
#         if logY == 'True':
#             r.gPad.SetLogy()
#         signSelection, iso = conditions(k+1)
#         var_background[k].SetTitle('%s %s Events %s (%.1f fb^{-1}); %s; events / bin' %(signSelection, iso, titleName, Lumi,varName))
#         var_background[k].SetMaximum(max)
#         var_background[k].SetMinimum(0.01)
#         var_background[k].Draw()
#         if k == 0 and useData == 'True' and predict == 'True':
#             ost_fromSameSign.Draw('same')
#             ost_fromRelaxed.Draw('same')
# 
#         if k != 0 and useData == 'True':
#             var_data[k-1].Draw('PE same')
#         legendPosition = (0.63, 0.93 - 0.035*len(legendHistos[k]), 0.93, 0.9)
#         l.append(tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos[k]))
#         l[k].Draw('same')
#         var_signal[k].Draw('same')
#     c.Update()
#     c.Print('%s(' %psfile)
#     if predict == 'True':
#         c.cd(1)
#         l1 = tool.setMyLegend(lPosition=(0.5,0.7,0.93,0.9), lHistList=[(sameS2OppositeS, 'from SS/Relaxed (%.2f)' %sameS2OppositeS.Integral()),
#                                                                    (os_relaxed, 'Data - MC x%.2f (%.2f)' %(scale_mc2, os_relaxed.Integral()))])
#         sameS2OppositeS.Draw()
#         sameS2OppositeS.SetTitle('QCD background in OS Relaxed Region %s (%.1f fb^{-1}); %s; events / bin' %(titleName,Lumi,varName))
#         os_relaxed.SetLineWidth(2)
#         os_relaxed.SetLineStyle(2)
#         os_relaxed.Draw('same')
#         l1.Draw('same')
#         c.cd(2)
#         l2 = tool.setMyLegend(lPosition=(0.5,0.7,0.93,0.9), lHistList=[(relaxed2Tight, 'from SS/Relaxed (%.2f)' %relaxed2Tight.Integral()),
#                                                                    (ss_tight, 'Data - MC x%.2f (%.2f)' %(scale_mc, ss_tight.Integral()))])
#         relaxed2Tight.SetTitle('QCD background in SS Tight Region %s (%.1f fb^{-1}); %s; events / bin' %(titleName,Lumi,varName))
#         relaxed2Tight.Draw()
#         ss_tight.SetLineWidth(2)
#         ss_tight.SetLineStyle(2)
#         ss_tight.Draw('same')
#         l2.Draw('same')
    c.Update()
    c.Print('%s' %psfile)
    #ps.Close()
    print "Plot saved at %s" %(psfile)

op = opts()
if op.varName != 'test':
    getHistos(op.varName, op.signal, op.logy, float(op.sigBoost), int(op.nbins),
           op.useData, float(op.max), float(op.rangeMin), float(op.rangeMax), op.location, op.bTag, op.predict, op.region)

