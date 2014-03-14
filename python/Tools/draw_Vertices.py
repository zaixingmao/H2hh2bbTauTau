#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="nVertices.pdf"

#Title = "No Required b Tags, EleMuLooseVeto on Leg1"
title = "nVertices"

r.gStyle.SetOptStat(0)

sampleLocations = enVars.sampleLocations

hist1 = r.TH1F("hist1","nVertices", 50, 0, 49)
hist2 = r.TH1F("hist2","nVertices", 50, 0, 49)
hist3 = r.TH1F("hist3","nVertices", 50, 0, 49)
hist4 = r.TH1F("hist4","nVertices", 50, 0, 49)
hist5 = r.TH1F("hist5","nVertices", 50, 0, 49)
histList = [hist1, hist2, hist3, hist4, hist5]
hist1.SetTitle("nVertices; nVertices; Unit Normalized")
hist2.SetTitle("nVertices; nVertices; Unit Normalized")
hist3.SetTitle("nVertices; nVertices; Unit Normalized")
hist4.SetTitle("nVertices; nVertices; Unit Normalized")
hist5.SetTitle("nVertices; nVertices; Unit Normalized")

i = 0
legendHistos = []

for iSample, iLocation in sampleLocations:
    iChain = r.TChain("ttTreeIni/eventTree")
    nEntries = tool.addFiles(ch=iChain, dirName=iLocation, knownEventNumber=0, printTotalEvents=True, blackList=[])
    total = iChain.GetEntries()
    for j in range(total):
        tool.printProcessStatus(iCurrent=j, total=total, processName = 'Looping sample')
        iChain.GetEntry(j)
        histList[i].Fill(iChain.vertices)
    print ' '
    legendHistos.append((histList[i], iSample))
    i+=1

intList = tool.unitNormHists(histList)

legendPosition = (0.6, 0.75, 1., 0.85)

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPDF(psfile,112)

c = r.TCanvas("c","Test", 800, 600)
r.gPad.SetTickx()
r.gPad.SetTicky()

tool.setDrawHists2(sigHist1=hist1,sigHist2=hist2, sigHist3=hist3, ttHist=hist4, ZZHist=hist5)
l = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos)
l.Draw("same")
ps.Close()

print "Plot saved at %s" %(psfile)
