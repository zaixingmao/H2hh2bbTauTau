#!/usr/bin/env python
import ROOT as r
import optparse
import tool

r.gROOT.SetBatch(True)  # to suppress canvas pop-outs

fileList = ['dataB_all.root', 'dataA_all.root', 'dataC_all.root', 'dataD_all.root']

fList = []
treeList = []
legendHistos = []
histList = []

for i in range(len(fileList)):
    fList.append(r.TFile(fileList[i]))
    treeList.append(fList[i].Get("eventTree"))
    histList.append(r.TH1F())
    histList[i].SetLineColor(i+1)
    treeList[i].SetLineColor(i+1)
    legendHistos.append((histList[i],"%s with %d events" %(fileList[i], treeList[i].GetEntries())))

legendPosition = (0.5, 0.75, 0.9, 0.85)


listBranch = treeList[0].GetListOfBranches()

oFileName = "test.root"
ofile = r.TFile(oFileName, "RECREATE")

nBranches = listBranch.GetEntries()

for i in range(nBranches):
    iBranchName = listBranch.At(i).GetName()
    tmpCanvas = r.TCanvas(iBranchName,"c",800,600)

    treeList[0].Draw("%s" %(iBranchName), "")
    for i in range(1, len(fileList)):
        treeList[i].Draw("%s" %(iBranchName), "", "same")
    l = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos)
    l.Draw("same")
    tmpCanvas.Write()
    tool.printProcessStatus(i+1, nBranches, 'Saving to file %s.root' %(oFileName))
print '  -- saved %d branches' %(nBranches)
