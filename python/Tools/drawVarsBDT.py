#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import optparse

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--pdf", dest="drawPDF", default = False, help="save result in PDF instead of ROOT")
    options, args = parser.parse_args()
    return options

options = opts()

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******

trainMass = 260

iFileName = '/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVA_%s.root' %(trainMass)
iFile = r.TFile(iFileName)
tree = iFile.Get("TestTree")
listBranch = tree.GetListOfBranches()

oFileName = ".%s_VarsBDT.root" %(iFileName[iFileName.rfind('/'):iFileName.rfind('.')])
if options.drawPDF:
    oFileName = '%s.pdf' %(oFileName[0: oFileName.rfind('.')])
    canv = r.TCanvas("","c",800,600)
    ofile = r.TPDF(oFileName,112);
else:
    ofile = r.TFile(oFileName, "RECREATE")

nBranches = listBranch.GetEntries()

for i in range(nBranches):
    iBranchName = listBranch.At(i).GetName()
    if iBranchName in ['classID', 'className', 'BDT']:
        continue
    if not options.drawPDF:
        tmpCanvasSig = r.TCanvas("%s_SigvsBDT" %(iBranchName),"c",800,600)
    r.gStyle.SetPalette(1)
    tree.Draw("%s:BDT" %(iBranchName), "classID == 0", "COLZ")
    if options.drawPDF:
        canv.Update()
    else:
        tmpCanvasSig.Write()

    if not options.drawPDF:
        tmpCanvasBkg = r.TCanvas("%s_BkgvsBDT" %(iBranchName),"c",800,600)
    r.gStyle.SetPalette(1)
    tree.Draw("%s:BDT" %(iBranchName), "classID == 1", "COLZ")
    if options.drawPDF:
        canv.Update()
    else:
        tmpCanvasBkg.Write()
    
    
    tool.printProcessStatus(i+1, nBranches, 'Saving to file %s' %(oFileName))
print '  -- saved %d branches' %(nBranches)
