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

def passCut(tree):
    if tree.CSVJ1 > 0.679 and tree.CSVJ2 > 0.244 and abs(tree.eta1.at(0))<2.1 and abs(tree.eta2.at(0))<2.1:
        iso_count = 0
        sign_count = 0
        if tree.iso2.at(0) > 1.5:
            iso_count = 1
        if tree.charge1.at(0) -  tree.charge2.at(0) == 0:
            sign_count = 1
        return (iso_count<<1) + sign_count + 1
    else:
        return 0

def getHistos(varName, signalSelection, logY, sigBoost, nbins, useData, max, rangeMin, rangeMax, location):
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
    var_background = []

    tmpFile = []
    tmpTree = []
    var_data = []

    for i in range(3):
        var_data.append(r.TH1F('%s_%i' %(fileList[i][0],i),"", varRange[0], varRange[1], varRange[2]))
    fData = r.TFile('dataTotal_all.root')
    treeData = fData.Get('eventTree')
    print 'Adding events from: dataTotal_all.root ...'
    for iEntry in range(treeData.GetEntries()):
        treeData.GetEntry(iEntry)
        select = passCut(treeData)
        if (select == 0) or (select == 1):
            continue
        var_data[select-2].Fill(varsList.findVar(treeData, varName))
    for j in range(3):
        var_data[j].SetMarkerStyle(8)
        var_data[j].SetMarkerSize(0.9)
        legendHistos.append((var_data[j], 'observed'))

    for i in range(len(fileList)): 
        for j in range(4):
            histList.append(r.TH1F('%s_%i' %(fileList[i][0],j),fileList[i][0], varRange[0], varRange[1], varRange[2]))
        print 'Adding events from: %s ...' %(fileList[i][1])
        tmpFile.append(r.TFile(fileList[i][1]))
        tmpTree.append(tmpFile[i].Get('eventTree'))
        for iEntry in range(tmpTree[i].GetEntries()):
            tmpTree[i].GetEntry(iEntry)
            select = passCut(tmpTree[i])
            if not select:
                continue
            histList[4*i+select-1].Fill(varsList.findVar(tmpTree[i], varName), tmpTree[i].triggerEff)
    
        initNEventsList.append(tmpFile[i].Get('preselection'))
        for j in range(4):
            var_background.append(r.THStack())
            histList[4*i+j].SetFillColor(fileList[i][3])
            histList[4*i+j].Scale(fileList[i][2]*Lumi/initNEventsList[i].GetBinContent(1))
            var_background[j].Add(histList[4*i+j])
            legendHistos.append((histList[4*i+j], '%s (%.2f)' %(fileList[i][0], histList[4*i+j].Integral())))

    DrawSignal = False
    if signalSelection != '':
        var_signal = []
        for i in range(4):
            var_signal.append(r.TH1F('%s_%i' %(fileList[i][0],i),"", varRange[0], varRange[1], varRange[2]))
        signalDict = {'H260': ('H2hh260_all.root', 14.76),
                      'H300': ('H2hh300_all.root', 15.9),
                      'H350': ('H2hh350_all.root', 8.57)}
        if signalSelection in signalDict:
            fSignal = r.TFile(signalDict[signalSelection][0])
            treeSignal = fSignal.Get('eventTree')
            print 'Adding events from: %s ...' %(signalDict[signalSelection][0])
            for iEntry in range(treeSignal.GetEntries()):
                treeSignal.GetEntry(iEntry)
                select = passCut(treeSignal)
                if not select:
                    continue
                var_signal[select-1].Fill(varsList.findVar(treeSignal, varName), treeSignal.triggerEff)
            initNEventsSignal = fSignal.Get('preselection')
            for i in range(4):
                var_signal[i].SetLineStyle(7)
                var_signal[i].SetLineWidth(4)
                var_signal[i].Scale(signalDict[signalSelection][1]*sigBoost*Lumi/initNEventsSignal.GetBinContent(1))
                if sigBoost != 1:
                    legendHistos.append((var_signal[i], '%sx%0.f (%.2f)' %(signalSelection, sigBoost, var_signal[i].Integral())))
                else:
                    legendHistos.append((var_signal[i], '%s (%.2f)' %(signalSelection, var_signal[i].Integral())))
            DrawSignal = True
        else:
            print '%s not supported, please use H260, H300 or H350' %signalSelection

    legendPosition = (0.6, 0.7, 0.90, 0.88)
    l = []

    psfile = '%s/%s_combined.pdf' %(location, varName)
    c = r.TCanvas("c","Test", 800, 600)
    ps = r.TPDF(psfile,112)
    c.Divide(2,2)
    drawOpt = ''
    for k in range(4):
        c.cd(k+1)
        if logY == 'True':
            r.gPad.SetLogy()
        signSelection, iso = conditions(k+1)
        var_background[k].SetTitle('%s %s Events 1 Medium 1 Loose b-tag (%.1f fb^{-1}); %s; events / bin' %(signSelection, iso, Lumi,varName))
        var_background[k].SetMaximum(max)
        var_background[k].SetMinimum(0.01)
        var_background[k].Draw()
        if k != 0:
            var_data[k-1].Draw('PE same')
            l.append(tool.setMyLegend(lPosition=legendPosition, lHistList=[legendHistos[k-1],legendHistos[3+k], legendHistos[7+k], legendHistos[11+k], legendHistos[15+k], legendHistos[16+k], legendHistos[23+k]]))
        else:
            l.append(tool.setMyLegend(lPosition=legendPosition, lHistList=[legendHistos[3+k], legendHistos[7+k], legendHistos[11+k], legendHistos[15+k], legendHistos[16+k], legendHistos[23+k]]))
        l[k].Draw('same')
        var_signal[k].Draw('same')
        c.Update()

    ps.Close()
    print "Plot saved at %s" %(psfile)
    histList = []

op = opts()
if op.varName != 'test':
    getHistos(op.varName, op.signal, op.logy, float(op.sigBoost), int(op.nbins),
           op.useData, float(op.max), float(op.rangeMin), float(op.rangeMax), op.location)

