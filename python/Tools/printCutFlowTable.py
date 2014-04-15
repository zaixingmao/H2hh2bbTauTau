#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars
import sys

SampleList = [('QCD_Pt-30-50', 'QCD_Pt-30to50_all.root'),
              ('QCD_Pt-50-80', 'QCD_Pt-50to80_all.root'),
              ('QCD_Pt-80-120', 'QCD_Pt-80to120_all.root'),
              ('QCD-Pt-120-170', 'QCD-120to170_all.root'),
              ('QCD_Pt-30-50_b', 'QCD_Pt-30To50_bEnriched_all.root'),
              ('QCD_Pt-50-150_b', 'QCD_Pt-50To150_bEnriched_all.root'),
              ('QCD_Pt-150_b', 'QCD_Pt-150_bEnriched_all.root')
              ]

titleLine = "\t\t\t"
secondLine = "Before Selection\t"
thirdLine = "Same Sign Events\t"

for iSample, iLocation in SampleList:
    titleLine += '%s\t' %(iSample)
    tmpFile = r.TFile(iLocation)
    tmpTree = tmpFile.Get('eventTree')
    tmpHist = tmpFile.Get('preselection')
    secondLine += '%i\t\t' %(tmpHist.GetBinContent(1))
    thirdLine += '%i\t\t' %(tmpTree.GetEntries())

f = open('QCD.txt','w')
f.write('%s\n' %titleLine)
f.write('%s\n' %secondLine)
f.write('%s\n' %thirdLine)
f.close()