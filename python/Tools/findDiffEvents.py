#!/usr/bin/env python
import ROOT as r
import optparse
import tool
from array import array
import enVars

r.gROOT.SetBatch(True)  # to suppress canvas pop-outs


vecVarList = enVars.vecVarList

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--file1", dest="file1", default="", help="REQUIRED: .root file 1 over which to run")
    parser.add_option("--file2", dest="file2", default="", help="REQUIRED: .root file 2 over which to run")
    options, args = parser.parse_args()

    if not all([options.file1, options.file2]):
        parser.print_help()
        exit()
    return options

def getVectBranchVal(iBranchName, tree, entry):
    tree.GetEntry(entry)
    if iBranchName == 'pt1':
        return tree.pt1.at(0)
    elif iBranchName == 'pt2':
        return tree.pt2.at(0)
    elif iBranchName == 'eta1':
        return tree.eta1.at(0)
    elif iBranchName == 'eta2':
        return tree.eta2.at(0)
    elif iBranchName == 'phi1':
        return tree.phi1.at(0)
    elif iBranchName == 'phi2':
        return tree.phi2.at(0)
    elif iBranchName == 'iso1':
        return tree.iso1.at(0)
    elif iBranchName == 'iso2':
        return tree.iso2.at(0)
    elif iBranchName == 'svEta':
        return tree.svEta.at(0)
    elif iBranchName == 'svPhi':
        return tree.svPhi.at(0)
    elif iBranchName == 'svMass':
        return tree.svMass.at(0)
    elif iBranchName == 'svPt':
        return tree.svPt.at(0)


def getBranchVal(varList, tree, entry):
    branchList = tree.GetListOfBranches()
    i = 0
    for iBranch in branchList:
        iBranchName = iBranch.GetName()
        iBranch.GetEntry(entry)
        if iBranchName in vecVarList:
            varList[i][0] = getVectBranchVal(iBranchName, tree, entry)
        else:
            varList[i][0] = iBranch.GetLeaf(iBranchName).GetValue()
        i+=1
    return varList

options = opts()

f1 = r.TFile(options.file1)
f2 = r.TFile(options.file2)
tree1 = f1.Get("eventTree")
tree1.SetLineColor(r.kAzure+9)
tree1.SetFillColor(r.kAzure+9)
tree1.SetFillStyle(3003)
tree2 = f2.Get("eventTree")
tree2.SetLineColor(2)
tree2.SetLineWidth(2)
tree2.SetLineStyle(2)

oFileName = "%sin%s" %(options.file1[0:options.file1.find('.')], options.file2)
oFile = r.TFile(oFileName, "RECREATE")
oTree = r.TTree()

evnNumList1 = []
varList = []
listBranch = tree1.GetListOfBranches()
for i in range(listBranch.GetEntries()):
    varList.append(array('f', [0.]))
    oTree.Branch(listBranch.At(i).GetName(), varList[i], "%s/F" %(listBranch.At(i).GetName()))

#get event number list for each tree
for i in range(tree1.GetEntries()):
    tree1.GetEntry(i)
    evnNumList1.append(tree1.EVENT)

nEntries = tree2.GetEntries()
counter = 0

for i in range(nEntries):
    tool.printProcessStatus(i, nEntries, 'Comparing root files')
    tree2.GetEntry(i)
    if tree2.EVENT in evnNumList1:
        continue
    #print setVarList[1][0]
    getBranchVal(varList = varList, tree = tree2, entry = i)
    oTree.Fill()
    counter+=1
print '  -- saved %d events' %(counter)

oFile.cd()
oTree.Write()
oFile.Close()
    
    
