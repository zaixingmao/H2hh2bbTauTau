#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import math
import optparse
import os
from array import array


effList_both = []
ifiles = []
iFileList = [('BDTEfficiency_17.root','17 Variables',r.kAzure+7), 
            ('BDTEfficiency_16.root','16 Variables (took out fMass)',r.kGreen), 
            ('BDTEfficiency_12.root', '12 Variables',r.kRed-7),
            ('BDTEfficiency_8.root', '8 Variables',r.kYellow),
            ('BDTEfficiency_4.root', '4 Variables',r.kMagenta-9)]
lHistList1=[]
lHistList2=[]


for i in range(len(iFileList)):
    ifiles.append(r.TFile(iFileList[i][0]))
    effList_both.append(ifiles[i].Get("eff_both"))
    effList_both[i].SetMarkerColor(iFileList[i][2])
    effList_both[i].SetMarkerSize(1)
    effList_both[i].SetMarkerStyle(2)
    lHistList2.append((effList_both[i], iFileList[i][1]))

legendPosition = (0.2, 0.2, 0.5, 0.5)

psfile = 'BDT_Eff_diff.pdf'
c = r.TCanvas("c","Test", 800, 600)


effList_both[0].SetTitle('Background Rejection VS Signal Efficiency ; Background Rejection; Signal Efficiency')
effList_both[0].SetMinimum(0.5)
effList_both[0].GetXaxis().SetRangeUser(0.5, 1)
effList_both[0].Draw('P')
for j in range(1, len(iFileList)):
    effList_both[j].Draw('sameP')
l = tool.setMyLegend(legendPosition, lHistList2)
l.Draw('same')
c.Update()
c.Print('%s' %psfile)

print 'plot saved at: %s' %psfile