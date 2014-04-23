#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import math
import optparse
import os
from array import array


def opts():
    parser = optparse.OptionParser()
    parser.add_option("--i", dest="inputFile", default = '', help="")
    options, args = parser.parse_args()
    return options

options = opts()

iFileName = options.inputFile

iFile = r.TFile(iFileName)
iTree = iFile.Get("eventTree")
cutFlow = iFile.Get("preselection")
total = iTree.GetEntries()

oFile1 = r.TFile(iFileName[0:iFileName.rfind('.root')] + '_0.root',"RECREATE")
tree1 = iTree.CloneTree(0)
for i in range(total):
    tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample %s' %iFileName)
    if i%2 == 0:
        iTree.GetEntry(i)
        tree1.Fill()
print ''
oFile1.cd()
tree1.Write()
nSaved1 = tree1.GetEntries()
oFile1.Close()

oFile2 = r.TFile(iFileName[0:iFileName.rfind('.root')] + '_1.root',"RECREATE")
tree2 = iTree.CloneTree(0)
for i in range(total):
    tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample %s' %iFileName)
    if i%2 == 1:
        iTree.GetEntry(i)
        tree2.Fill()
print ''
oFile2.cd()
tree2.Write()
nSaved2 = tree2.GetEntries()
oFile2.Close()

print 'looped through %i evnets' %total
print 'saved %i events at: %s_0.root' %(nSaved1,iFileName[0:iFileName.rfind('.root')])
print 'saved %i events at: %s_1.root' %(nSaved2,iFileName[0:iFileName.rfind('.root')])