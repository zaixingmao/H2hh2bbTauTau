#!/usr/bin/env python

import ROOT as r
import tool
import varsList
import optparse
import math
from array import array
import numpy

def passCut(tree, region):
    if region == "SS":
        if tree.charge1.at(0) + tree.charge2.at(0) == 0:
            return 0
    else:
        if tree.charge1.at(0) == tree.charge2.at(0):
            return 0
    if tree.CSVJ1 < 0.68 or tree.CSVJ2 < 0.68:
        return 0
    if abs(tree.eta1.at(0)) > 2.1 or abs(tree.eta2.at(0)) > 2.1:
        return 0

fileLocation = 
file = r.TFile(fileLocation)
tree = file.Get('eventTree')

tree_ini = file.Get('iniTree')

varRanges = [25, 0, 250]

pt1 = r.TH1F("pt1", "", varRanges[0], varRanges[1], varRanges[2])
pt2 = r.TH1F("pt2", "", varRanges[0], varRanges[1], varRanges[2])

pt1_init = r.TH1F("pt1_init", "", varRanges[0], varRanges[1], varRanges[2])
pt2_init = r.TH1F("pt2_init", "", varRanges[0], varRanges[1], varRanges[2])


print 'Adding events from: %s ...' %fileLocation

for iEntry in range(tree.GetEntries()):
    tree.GetEntry(iEntry)
    select = passCut(tree, region)
    if select == 0:
        continue
    pt1.Fill(tree.pt1.at(0))
    pt2.Fill(tree.pt2.at(0))

for iEntry in range(tree_ini.GetEntries()):
    tree_ini.GetEntry(iEntry)
    select = passCut(tree_ini, region)
    if select == 0:
        continue
    pt1_init.Fill(tree_ini.pt1.at(0))
    pt2_init.Fill(tree_ini.pt2.at(0))

pt1.Divide(pt1_init)
pt2.Divide(pt2_init)

