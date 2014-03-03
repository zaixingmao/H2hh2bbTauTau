#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******

trainMass = 350
iFileName = '/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVA_%s.root' %(trainMass)
iFile = r.TFile(iFileName)
tree = iFile.Get("TestTree")
listBranch = tree.GetListOfBranches()

oFileName = ".%s_VarsBDT.root" %(iFileName[iFileName.rfind('/'):iFileName.rfind('.')])
ofile = r.TFile(oFileName, "RECREATE")

nBranches = listBranch.GetEntries()

for i in range(nBranches):
    iBranchName = listBranch.At(i).GetName()
    if iBranchName in ['classID', 'className', 'BDT']:
        continue

    tmpCanvasSig = r.TCanvas("%s_SigvsBDT" %(iBranchName),"c",800,600)
    r.gStyle.SetPalette(1)
    tree.Draw("%s:BDT" %(iBranchName), "classID == 0", "COLZ")
    tmpCanvasSig.Write()

    tmpCanvasBkg = r.TCanvas("%s_BkgvsBDT" %(iBranchName),"c",800,600)
    r.gStyle.SetPalette(1)
    tree.Draw("%s:BDT" %(iBranchName), "classID == 1", "COLZ")
    tmpCanvasBkg.Write()
    
    tool.printProcessStatus(i+1, nBranches, 'Saving to file %s' %(oFileName))
print '  -- saved %d branches' %(nBranches)
