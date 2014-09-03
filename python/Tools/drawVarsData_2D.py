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

file = r.TFile('combined.root')
tree = file.Get('eventTree')

xsHist = file.Get("xs")
nameList = {'H2hh260': 0, 
            'H2hh300': 1,
            'H2hh350': 2,
            'WZJetsTo2L2Q': 3,
            'ZZ': 4,
            'tt_full': 5,
            'tt_semi': 6,
            'DY1JetsToLL': 7,
            'DY2JetsToLL': 8,            
            'DY3JetsToLL': 9,
            'W1JetsToLNu': 10,
            'W2JetsToLNu': 11,
            'W3JetsToLNu': 12,
            'dataOSRelax': 13}

h_svMass = r.TH2F('H2hh350_svMass', '', 20, -1., 1., 16, 0, 400)
h_mJJ = r.TH2F('H2hh350_mJJ', '', 20, -1., 1., 16, 0, 400)
h_svMass.SetTitle('H2hh350_svMass; BDT; svMass')
h_mJJ.SetTitle('H2hh350_mJJ; BDT; mJJ')


h_svMass2 = r.TH2F('bkg_svMass', '', 20, -1., 1., 16, 0, 400)
h_mJJ2 = r.TH2F('bkg_mJJ', '', 20, -1., 1., 16, 0, 400)
h_svMass2.SetTitle('bkg_svMass; BDT; svMass')
h_mJJ2.SetTitle('bkg_mJJ; BDT; mJJ')

nTotal = tree.GetEntries()
Lumi = 19.0

for iEntry in range(nTotal):
    tree.GetEntry(iEntry)
    xsScale = xsHist.GetBinContent(nameList[tree.sampleName])
    if tree.sampleName == 'H2hh350':
        h_svMass.Fill(tree.BDT_350, tree.svMass, tree.triggerEff*xsScale)
        h_mJJ.Fill(tree.BDT_350, tree.mJJ, tree.triggerEff*xsScale)
    if tree.sampleName != 'H2hh350' and tree.sampleName != 'H2hh260' and tree.sampleName != 'H2hh300':
        h_svMass2.Fill(tree.BDT_350, tree.svMass, tree.triggerEff*xsScale)
        h_mJJ2.Fill(tree.BDT_350, tree.mJJ, tree.triggerEff*xsScale)

psfile = '2D_plot.pdf'
c = r.TCanvas("c","Test", 900, 800)
c.Divide(2,2)
r.gStyle.SetOptStat(0)

l = r.TLine(0.2,0,0.2,400)
l.SetLineStyle(2)
l.SetLineColor(r.kRed)

c.cd(1)
h_svMass.Draw('COLZ')
h_svMass.GetYaxis().SetTitleOffset(1.3)
l.Draw('same')
c.cd(2)
h_mJJ.Draw('COLZ')
h_mJJ.GetYaxis().SetTitleOffset(1.3)

l.Draw('same')
c.cd(3)
h_svMass2.Draw('COLZ')
h_svMass2.GetYaxis().SetTitleOffset(1.3)

l.Draw('same')
c.cd(4)
h_mJJ2.Draw('COLZ')
h_mJJ2.GetYaxis().SetTitleOffset(1.3)

l.Draw('same')

c.Print('%s' %psfile)
c.Close()