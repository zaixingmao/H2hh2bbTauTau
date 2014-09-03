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
    parser.add_option("--region", dest="region", default = 'LL', help="")
    parser.add_option("--unit", dest="unit", default = '', help="")


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
        return 'SS', 'cut-off wiht iso3'

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
#     if tree.tauDecayMode1 != 10:
#         return 0
#         return 0
#     if tree.pt1.size() > 1:
#         return 0
    isoCut = 3
    iso_count = 3
    if  tree.mJJ<90  or tree.mJJ>140:
        return 0

    if region == 'LL':
        if  tree.iso1.at(0)>1.5  and tree.iso2.at(0)>1.5:
              iso_count = 2
        if  tree.iso1.at(0)>isoCut  and tree.iso2.at(0)<1.5:
              return 0
        if  tree.iso1.at(0)<1.5  and tree.iso2.at(0)>isoCut:
              return 0
    elif region == 'LT':
        if tree.iso1.at(0)>1.5  and tree.iso2.at(0)<1.5:
              iso_count = 2
        if tree.iso1.at(0)>isoCut  and tree.iso2.at(0)>isoCut:
            return 0
        if tree.iso1.at(0)<1.5  and tree.iso2.at(0)>isoCut:
            return 0
    elif region == 'TL':
        if tree.iso1.at(0)<1.5  and tree.iso2.at(0)>1.5:
              iso_count = 2
        if tree.iso1.at(0)>isoCut  and tree.iso2.at(0)>isoCut:
            return 0
        if tree.iso1.at(0)>isoCut  and tree.iso2.at(0)<1.5:
            return 0

    if bTagSelection(tree, bTag) and abs(tree.eta1.at(0))<2.1 and abs(tree.eta2.at(0))<2.1:
        sign_count = 0
        maxIso = 10
        if  tree.iso1.at(0) > maxIso  or tree.iso2.at(0) > maxIso:
            iso_count = 5
        elif  tree.iso1.at(0)>isoCut and tree.iso2.at(0)>isoCut:
            iso_count = 1

#         elif  1.5<tree.iso1.at(0)<3 and 3<tree.iso2.at(0):
#             iso_count = 1
#         elif  1.5<tree.iso2.at(0)<3 and 3<tree.iso1.at(0):
#             iso_count = 1

        elif (tree.iso1.at(0)>isoCut and tree.iso2.at(0)<1.5) or (tree.iso2.at(0)>isoCut and tree.iso1.at(0)<1.5):
            iso_count = 1
        elif  tree.iso1.at(0)<1.5  and tree.iso2.at(0)<1.5:
            iso_count = 0
        else:
            return 0
        if tree.charge1.at(0) - tree.charge2.at(0) == 0:
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

def findPtScale(pt1, pt2, direction, region):
    scaleDictUp = {'LL': 0.051, #0.036, 
                   'LT': 0.248, #0.221,
                   'TL': 0.229, #0.201
                  }  
    if direction == 'up':
        return scaleDictUp[region]

    scale1 = 1.0
    scale2 = 1.0
    ptRange = [70, 120]
    scaleDictLeft = {'LL': [1.06, 0.97, 0.97],#[1.08, 0.93, 0.93], 
                     'LT': [1.29, 0.92, 1.30], #[1.3, 1.04, 1.0],
                     'TL': [1.24, 0.63, 2.15],#[1.21, 0.78, 2.05]
                    }

    scale = scaleDictLeft[region]

    if pt1 < ptRange[0]:
        scale1 = scale[0]
    elif ptRange[0] < pt1 < ptRange[1]:
        scale1 = scale[1]
    elif ptRange[1] < pt1:
        scale1 = scale[2]
    if pt2 < ptRange[0]:
        scale2 = scale[0]
    elif ptRange[0] < pt2 < ptRange[1]:
        scale2 = scale[1]
    elif ptRange[1] < pt2:
        scale2 = scale[2]

    if region == 'LL':
        return scale1*scale2
    elif region == 'LT':
        return scale1
    elif region == 'TL':
        return scale2

def calc(alpha, nT,nL):
    return pow(nT-alpha*nL,2)/(alpha*nL)

def drawX2vsAlpha(hist1, hist2, nbins, xmin, xmax):
    plotHist = r.TGraph() 
    hist = r.TH1F('plotHist', '', nbins, xmin, xmax)
    incre = (xmax - xmin)/nbins
    nHistBins = hist1.GetNbinsX()
    iAlpha = xmin
    counter = 0
    min = 1000
    minX = 0
    while iAlpha < xmax:
        xSquare = 0
        for iBin in range(nHistBins):
            nT = hist1.GetBinContent(iBin+1)
            nL = hist2.GetBinContent(iBin+1)
            xSquare += calc(iAlpha, nT,nL)
        iAlpha += incre
        if xSquare < min:
            min = xSquare
            minX = iAlpha
        plotHist.SetPoint(counter, iAlpha, xSquare) 
        hist.Fill(iAlpha, xSquare)
        counter += 1
    return plotHist, hist, min, minX

def findUnevenRange(xmin, nbins, hist):
    xBins = []
    xBins.append(xmin)
    nTotal = hist.Integral()
    binMin = nTotal/7
    for i in range(nbins):
        upperBin = hist.GetXaxis().GetBinUpEdge(i+1)
        lowerBin = hist.GetXaxis().GetBinLowEdge(i+1)
        binContent = hist.GetBinContent(i+1)
        if ( binContent< binMin) and i < nbins-1:
            hist.Fill(1.5*upperBin-0.5*lowerBin, binContent)
        elif ( binContent< binMin) and i == nbins-1:
            xBins[len(xBins)-1] = upperBin
        else:
            xBins.append(upperBin)
    return array('d',xBins)

def findBinScale(value, binsArray):
    counterMax = len(binsArray)
    for iCounter in range(1, counterMax):
        if value < binsArray[iCounter]:
            return 1/(binsArray[iCounter]-binsArray[iCounter-1])
    return 0

def findRange(hist, yValue, xMiddle):
    nbins = hist.GetNbinsX()
    x1 = 0
    x2 = 0
    deltaY1 = 1000
    deltaY2 = 1000
    for i in range(nbins):
        if hist.GetBinCenter(i+1) < xMiddle:
            if deltaY1 > abs(hist.GetBinContent(i+1) - yValue):
                deltaY1 = abs(hist.GetBinContent(i+1) - yValue)
                x1 = hist.GetBinCenter(i+1)
        else:
            if deltaY2 > abs(hist.GetBinContent(i+1) - yValue):
                deltaY2 = abs(hist.GetBinContent(i+1) - yValue)
                x2 = hist.GetBinCenter(i+1)
    return x1, x2

def getHistos(varName, signalSelection, logY, sigBoost, nbins, useData, max, rangeMin, rangeMax, location, bTag, predict, predictPtBin, region, unit):
    r.gStyle.SetOptStat(0)
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
                ('tt_MSDecays',preFix + 'TTJets_MSDecays_all.root', 249500, r.kAzure+7),]
#                 ('tt_full_lep',preFix + 'tt_eff_all.root', 26197.5, r.kRed-7),
#                 ('tt_semi_lep',preFix + 'tt_semi_eff_all.root', 109281, r.kAzure+7)]

    histList = []
    histList_4QCD = []
    QCDHistList = [] 
    QCDHistList_withScale = []
    nbins = 200
    varRange = [nbins, rangeMin, rangeMax]
    Lumi = 19.0
    initNEventsList = []
    legendHistos = []
    var_background = []

    scaleMCPt = 1.0

    tmpFile = []
    tmpTree = []
    var_data = []
    var_data_original = []
    var_data_4QCD = []


    data4Binning = r.TH1F('data4Binning',"", nbins, varRange[1], varRange[2])

    dataName = preFix + 'dataTotal_all.root'
    fData = r.TFile(dataName)
    treeData = fData.Get('eventTree')
    print 'Adding events from: %s ...' %dataName
    for iEntry in range(treeData.GetEntries()):
        treeData.GetEntry(iEntry)
        select = passCut(treeData, bTag, region)
        if select != 4:
            continue
        data4Binning.Fill(varsList.findVar(treeData, varName))

    xBinsArray = findUnevenRange(xmin=rangeMin, nbins=nbins, hist=data4Binning)
    print 'New binning: ', xBinsArray

    for i in range(5):
        var_data.append(r.TH1F('data_%i' %(i),"", len(xBinsArray)-1, xBinsArray))
        var_data_original.append(r.TH1F('data_original_%i' %(i),"", len(xBinsArray)-1, xBinsArray))
        if i < 5:
            var_data_4QCD.append(r.TH1F('data_4QCD_%i' %(i),"", len(xBinsArray)-1, xBinsArray))

    print 'Adding events from: %s ...' %dataName
    for iEntry in range(treeData.GetEntries()):
        treeData.GetEntry(iEntry)
        select = passCut(treeData, bTag, region)
        value = varsList.findVar(treeData, varName)
        if (select == 0) or (select == 1) or (select > 6):
            continue
        var_data[select-2].Fill(value, findBinScale(value, xBinsArray))
        var_data_original[select-2].Fill(value)

        if select == 2:
            var_data_4QCD[0].Fill(value, findBinScale(value, xBinsArray)*findPtScale(treeData.pt1.at(0),treeData.pt2.at(0), 'left', region))
        elif select == 3:
            var_data_4QCD[1].Fill(value, findBinScale(value, xBinsArray)*findPtScale(treeData.pt1.at(0),treeData.pt2.at(0), 'up', region))
        elif select == 4:
            var_data_4QCD[2].Fill(value, findBinScale(value, xBinsArray)*findPtScale(treeData.pt1.at(0),treeData.pt2.at(0), 'left', region))
            var_data_4QCD[3].Fill(value, findBinScale(value, xBinsArray)*findPtScale(treeData.pt1.at(0),treeData.pt2.at(0), 'up', region))



    legendHistos.append([])
    for j in range(5):
        var_data[j].SetMarkerStyle(8)
        var_data[j].SetMarkerSize(0.9)
        legendHistos.append([])
        legendHistos[j+1].append((var_data[j], 'observed (%.0f)' %var_data[j].Integral("width")))

    for i in range(len(fileList)): 
        for j in range(6):
            histList.append(r.TH1F('%s_%i' %(fileList[i][0],j),fileList[i][0], len(xBinsArray)-1, xBinsArray))
            histList_4QCD.append(r.TH1F('%s_%i_2' %(fileList[i][0],j),fileList[i][0], len(xBinsArray)-1, xBinsArray))
        print 'Adding events from: %s ...' %(fileList[i][1])
        tmpFile.append(r.TFile(fileList[i][1]))
        tmpTree.append(tmpFile[i].Get('eventTree'))
        for iEntry in range(tmpTree[i].GetEntries()):
            tmpTree[i].GetEntry(iEntry)
            select = passCut(tmpTree[i], bTag, region)
            value = varsList.findVar(tmpTree[i], varName)*scaleMCPt
            if (not select) or (select > 6):
                continue
            histList[6*i+select-1].Fill(value, findBinScale(value, xBinsArray)*tmpTree[i].triggerEff)
            if select == 2:
                histList_4QCD[6*i].Fill(value, findBinScale(value, xBinsArray)*tmpTree[i].triggerEff*findPtScale(tmpTree[i].pt1.at(0), tmpTree[i].pt2.at(0), 'left', region))
            elif select == 3:
                histList_4QCD[6*i+1].Fill(value, findBinScale(value, xBinsArray)*tmpTree[i].triggerEff*findPtScale(tmpTree[i].pt1.at(0), tmpTree[i].pt2.at(0), 'up', region))
            elif select == 4:             
                histList_4QCD[6*i+2].Fill(value, findBinScale(value, xBinsArray)*tmpTree[i].triggerEff*findPtScale(tmpTree[i].pt1.at(0), tmpTree[i].pt2.at(0), 'left', region))
                histList_4QCD[6*i+3].Fill(value, findBinScale(value, xBinsArray)*tmpTree[i].triggerEff*findPtScale(tmpTree[i].pt1.at(0), tmpTree[i].pt2.at(0), 'up', region))

        initNEventsList.append(tmpFile[i].Get('preselection'))
        for j in range(6):
            var_background.append(r.THStack())
            histList[6*i+j].SetFillColor(fileList[i][3])
            histList[6*i+j].Scale(fileList[i][2]*Lumi/initNEventsList[i].GetBinContent(1))
            histList_4QCD[6*i+j].Scale(fileList[i][2]*Lumi/initNEventsList[i].GetBinContent(1))
                
            var_background[j].Add(histList[6*i+j])
            legendHistos[j].append((histList[6*i+j], '%s (%.2f)' %(fileList[i][0], histList[6*i+j].Integral("width"))))

    data_i = []
    MC_i = []
    data_r = []
    MC_r = []
    e = []

    for i in range(3):
        QCDHistList.append(r.TH1F('QCD_%i' %(i),"", len(xBinsArray)-1, xBinsArray))
        for j in range(len(xBinsArray)-1):
            var_data[i].SetBinError(j+1, var_data_original[i].GetBinError(j+1)/(xBinsArray[j+1]-xBinsArray[j]))
            dataValue = var_data[i].GetBinContent(j+1)*(xBinsArray[j+1]-xBinsArray[j])
            dataError = var_data[i].GetBinError(j+1)*(xBinsArray[j+1]-xBinsArray[j])
            MCValue = 0
            for k in range(len(fileList)):
                MCValue +=  histList[6*k+1+i].GetBinContent(j+1)*(xBinsArray[j+1]-xBinsArray[j])
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

    for i in range(4):
        QCDHistList_withScale.append(r.TH1F('QCD_withScale_%i' %(i),"", len(xBinsArray)-1, xBinsArray))
        for j in range(len(xBinsArray)-1):
            dataValue = var_data_4QCD[i].GetBinContent(j+1)
            dataError = var_data_4QCD[i].GetBinError(j+1)
            MCValue = 0
            for k in range(len(fileList)):
                MCValue +=  histList_4QCD[6*k+i].GetBinContent(j+1)
            if dataValue - MCValue > 0:
                QCDHistList_withScale[i].SetBinContent(j+1, dataValue - MCValue)

    QCDDiff = r.TH1F('QCD_diff',"", len(xBinsArray)-1, xBinsArray)
    QCDDiff2 = r.TH1F('QCD_diff2',"", len(xBinsArray)-1, xBinsArray)

    QCDDiff = QCDHistList[1].Clone()
    QCDDiff.Divide(QCDHistList_withScale[2])
    QCDDiff.Sumw2()
    QCDDiff2 = QCDHistList[0].Clone()
    QCDDiff2.Divide(QCDHistList_withScale[3])
    QCDDiff2.Sumw2()

    fit1 = r.TF1("fit1","[0]", varRange[1],varRange[2])
    fit1.SetParName(0,'scale')
    fit1.FixParameter(0,1.0)

    QCDDiff.Fit('fit1', '0EM')
    fit1.SetLineStyle(2)
    fit1.SetLineColor(r.kRed)
    fit2 = r.TF1("fit2","[0]", varRange[1],varRange[2])
    fit2.SetParName(0,'scale')
    fit2.FixParameter(0,1.0)
    QCDDiff2.Fit('fit2', '0EM')
    fit2.SetLineStyle(2)
    fit2.SetLineColor(r.kRed)


    DrawSignal = False
    if signalSelection != '':
        var_signal = []
        for i in range(6):
            var_signal.append(r.TH1F('%s_%i' %(signalSelection,i),"", len(xBinsArray)-1, xBinsArray))
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
                if (not select) or (select > 6):
                    continue
                value = varsList.findVar(treeSignal, varName)
                var_signal[select-1].Fill(value, findBinScale(value, xBinsArray)*treeSignal.triggerEff)
            initNEventsSignal = fSignal.Get('preselection')
            for i in range(6):
                var_signal[i].SetLineStyle(7)
                var_signal[i].SetLineWidth(4)
                var_signal[i].Scale(signalDict[signalSelection][1]*sigBoost*Lumi/initNEventsSignal.GetBinContent(1))
                if sigBoost != 1:
                    legendHistos[i].append((var_signal[i], '%sx%0.f (%.2f)' %(signalSelection, sigBoost, var_signal[i].Integral("width"))))
                else:
                    legendHistos[i].append((var_signal[i], '%s (%.2f)' %(signalSelection, var_signal[i].Integral("width"))))
            DrawSignal = True
        else:
            print '%s not supported, please use H260, H300 or H350' %signalSelection

    if predict == 'True':

        scale_SS2OS = fit1.GetParameter(0)
        scale_er_SS2OS = fit1.GetParError(0)
        scale_relaxed2Tight = fit2.GetParameter(0)
        scale_er_relaxed2Tight = fit2.GetParError(0)

        QCDHistList_withScale[0].Scale(scale_SS2OS)
        QCDHistList_withScale[1].Scale(scale_relaxed2Tight)
        QCDHistList_withScale[2].Scale(scale_SS2OS)
        QCDHistList_withScale[3].Scale(scale_relaxed2Tight)

        QCDHistList_withScale[3].SetFillColor(r.kSpring+1)
        QCDHistList_withScale[2].SetFillColor(r.kOrange-4)
        QCDHistList_withScale[0].SetLineColor(r.kSpring+1)
        QCDHistList_withScale[0].SetLineWidth(2)
        QCDHistList_withScale[1].SetLineStyle(2)
        QCDHistList_withScale[1].SetLineColor(r.kOrange-4)
        QCDHistList_withScale[1].SetLineWidth(2)

        legendHistos[0].append((QCDHistList_withScale[0], 'From SS/Tight (%.0f)' %QCDHistList_withScale[0].Integral("width")))
        legendHistos[0].append((QCDHistList_withScale[1], 'From OS/Relax (%.0f)' %QCDHistList_withScale[1].Integral("width")))

        var_background[1].Add(QCDHistList_withScale[3])
        var_background[2].Add(QCDHistList_withScale[2])
        legendHistos[1].append((QCDHistList_withScale[3], 'From SS/Relax (%.0f)' %QCDHistList_withScale[3].Integral("width")))
        legendHistos[2].append((QCDHistList_withScale[2], 'From SS/Relax (%.0f)' %QCDHistList_withScale[2].Integral("width")))
        QCDHistList_withScale[1] = tool.addFakeTHStack(QCDHistList_withScale[1],var_background[0])
        QCDHistList_withScale[0] = tool.addFakeTHStack(QCDHistList_withScale[0],var_background[0])


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

    psfile = '%s/%s_%s_all.pdf' %(location, varName, fileName)
    c = r.TCanvas("c","Test", 800, 900)
    #ps = r.TPDF(psfile,112)
    c.Divide(2,3)
    drawOpt = ''
    for k in range(6):
        c.cd(k+1)
        r.gPad.SetTicky()
        if logY == 'True':
            r.gPad.SetLogy()
        signSelection, iso = conditions(k+1)
        var_background[k].SetTitle('%s %s Events %s (%.1f fb^{-1}); %s; events / %s' %(signSelection, iso, titleName, Lumi,varName, unit))
        var_background[k].SetMaximum(max)
        var_background[k].SetMinimum(0.01)
        var_background[k].Draw()
        if predict == 'True' and k == 0:
            QCDHistList_withScale[0].Draw('same')
            QCDHistList_withScale[1].Draw('same')
        if k != 0 and useData == 'True':
            var_data[k-1].Draw('PE same')
        legendPosition = (0.63, 0.93 - 0.03*len(legendHistos[k]), 0.93, 0.9)
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
    QCDDiff.SetMinimum(0.01)
    QCDDiff.Draw('PE')

    fit1.Draw('same')
    lFit1 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fit1,'Scale between OS/SS in relaxed region: %.2f \pm %.2f' %(fit1.GetParameter(0), fit1.GetParError(0)))])
    lFit1.Draw('same')
    for k in range(3):
        c.cd(k+2)
        if logY == 'True':
            r.gPad.SetLogy()
        signSelection, iso = conditions(k+2)
        QCDHistList_withScale[k+1].SetTitle('%s %s Data - MC Events %s (%.1f fb^{-1}); %s; events / %s' %(signSelection, iso, titleName, Lumi,varName, unit))
        QCDHistList_withScale[k+1].SetMarkerStyle(8)
        QCDHistList_withScale[k+1].SetMarkerSize(0.9)
        QCDHistList_withScale[k+1].SetMaximum(max)
        QCDHistList_withScale[k+1].SetMinimum(1)
        QCDHistList_withScale[k+1].Draw('PE')
    c.Update()
    c.Print('%s' %psfile)
    c.cd(1)
    r.gPad.SetLogy(0)
    QCDDiff2.SetTitle('tight/relaxed MultiJet SS Events %s (%.1f fb^{-1}); %s; tight/relaxed' %(titleName, Lumi,varName))
    QCDDiff2.SetMarkerStyle(8)
    QCDDiff2.SetMarkerSize(0.9)
    QCDDiff2.SetMinimum(0.1)
    QCDDiff2.SetMaximum(3)
    QCDDiff2.Draw('PE')
    fit2.Draw('same')
    lFit2 = tool.setMyLegend((0.15, 0.7, 0.9, 0.85),[(fit2,'Scale between relaxed/tight in SS region: %.3f \pm %.3f' %(fit2.GetParameter(0), fit2.GetParError(0)))])
    lFit2.Draw('same')
    c.Print('%s' %psfile)
    #ps.Close()
    c.Clear()
    c.SetGrid()
    XSRange = [0.05, 0.1]
    line = r.TF1('line', '[0]', XSRange[0], XSRange[1])
    plotHist, histNew, min, xMin = drawX2vsAlpha(QCDHistList[0],QCDHistList[2], 100, XSRange[0], XSRange[1])
    line.SetParameter(0, min+1)
    plotHist.SetTitle('Chi Square Test; #alpha; #chi^{2}')
    plotHist.Draw('APL')
    plotHist.GetYaxis().SetNdivisions(520)
    point = tool.setMyLegend((0.15, 0.8, 0.9, 0.85),[(var_signal[0],'Minimum %.2f at %.3f' %(min, xMin))])
    point.Draw('same')
    line.SetLineColor(r.kRed)
    line.SetLineStyle(2)
    line.Draw('same')
    x1, x2 = findRange(histNew, min+1, xMin)
#     line2 = tool.setMyLegend((0.3, 0.3, 0.8, 0.36),[(line, "#chi^{2} = %.2f, #alpha = [%.3f ~ %.3f] or [%.0f%%, %.0f%%]" %(min+1, x1, x2, 100*(xMin-x1)/xMin, 100*(x2-xMin)/xMin))])
#     line2.Draw('same')

    c.Print('%s)' %psfile)
    print "Plot saved at %s" %(psfile)

op = opts()
if op.varName != 'test':
    getHistos(op.varName, op.signal, op.logy, float(op.sigBoost), int(op.nbins),
           op.useData, float(op.max), float(op.rangeMin), float(op.rangeMax), op.location, op.bTag, op.predict, 'False', op.region, op.unit)

