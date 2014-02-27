#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars
from array import array

r.gStyle.SetOptStat(0)
  
ttFileName = tool.reWeightROOTFile(fileName = "/scratch/zmao/test2/bkg/tt_7.root", treeName = "eventTree", weight = 26.2)
ZZFileName = tool.reWeightROOTFile(fileName = "/scratch/zmao/test2/bkg/ZZ_7.root", treeName = "eventTree", weight = 2.5)

sampleLocations = [("bkg", "/scratch/zmao/test2/bkg/")]


for iSample, iLocation in sampleLocations:
    iChain = r.TChain("eventTree")
    nEntries = tool.addFiles(ch=iChain, dirName=iLocation, knownEventNumber=-1, printTotalEvents=True)
    iChain.SetBranchStatus("*",1)
    iChain.LoadTree(0)
    iTree = iChain.GetTree().CloneTree(0)
    iFile = r.TFile("%s.root" %(iSample),"recreate")

    counter = 0

    for iEntry in range(nEntries):
        iChain.LoadTree(iEntry)
        iChain.GetEntry(iEntry)
        iTree.Fill()
        counter += 1
        tool.printProcessStatus(iEntry, nEntries, 'Saving to file %s.root' %(iSample))
    print '  -- saved %d events' %(counter)

    iFile.cd()
    iTree.Write()
    iFile.Close()
