#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import math
import optparse
import os
from array import array

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
j1Reg = lvClass()
j2Reg = lvClass()

def splitFileNames(inputName):
    fileNames = []
    tmpName = ''
    for i in range(len(inputName)):
        if inputName[i] != ' ' and inputName[i] != ',':
            tmpName += inputName[i]
        elif inputName[i] == ',':
            fileNames.append(tmpName)
            tmpName = ''
    fileNames.append(tmpName)
    return fileNames

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--i", dest="inputFile", default = '', help="")
    parser.add_option("--v", dest="var", default = 'both', help="")
    parser.add_option("--o", dest="outputFile", default = 'trainSample', help="")
    options, args = parser.parse_args()
    return options

options = opts()

jetPtUncorr = array('f', [0.])
jetPt = array('f', [0.])
jetEt = array('f', [0.])
jetMt = array('f', [0.])
jetptLeadTrk = array('f', [0.])
jetVtx3dL  = array('f', [0.])
jetVtx3deL  = array('f', [0.])
jetvtxMass  = array('f', [0.])
jetVtxPt = array('f', [0.])
jetJECUnc = array('f', [0.])
jetNtot = array('f', [0.])
jetSoftLeptPtRel = array('f', [0.])
jetSoftLeptPt = array('f', [0.])
jetSoftLeptdR = array('f', [0.])
matchGenJetPt = array('f', [0.])
triggerEff = array('f', [0.])

oFile = r.TFile("%s_%s.root" %(options.outputFile, options.var),"recreate")
oTree = r.TTree("eventTree", "")
oTree.Branch("jetPtUncorr", jetPtUncorr, "jetPtUncorr/F")
oTree.Branch("jetPt", jetPt, "jetPt/F")
oTree.Branch("jetEt", jetEt, "jetEt/F")
oTree.Branch("jetMt", jetMt, "jetMt/F")
oTree.Branch("jetptLeadTrk", jetptLeadTrk, "jetptLeadTrk/F")
oTree.Branch("jetVtx3dL", jetVtx3dL, "jetVtx3dL/F")
oTree.Branch("jetVtx3deL", jetVtx3deL, "jetVtx3deL/F")
oTree.Branch("jetvtxMass", jetvtxMass, "jetvtxMass/F")
oTree.Branch("jetVtxPt", jetVtxPt, "jetVtxPt/F")
oTree.Branch("jetJECUnc", jetJECUnc, "jetJECUnc/F")
oTree.Branch("jetNtot", jetNtot, "jetNtot/F")
oTree.Branch("jetSoftLeptPtRel", jetSoftLeptPtRel, "jetSoftLeptPtRel/F")
oTree.Branch("jetSoftLeptPt", jetSoftLeptPt, "jetSoftLeptPt/F")
oTree.Branch("jetSoftLeptdR", jetSoftLeptdR, "jetSoftLeptdR/F")
oTree.Branch("matchGenJetPt", matchGenJetPt, "matchGenJetPt/F")
oTree.Branch("triggerEff", triggerEff, "triggerEff/F")

fileList = splitFileNames(options.inputFile)
print fileList
for iFile in fileList:
    ifile = r.TFile(iFile)
    iTree = ifile.Get("eventTree")
    total = iTree.GetEntries()

    for i in range(total):
        r.gStyle.SetOptStat(0)
        tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample %s' %iFile)
        iTree.GetEntry(i)

        jetPtUncorr[0] = iTree.CSVJ1PtUncorr
        jetPt[0] = iTree.CSVJ1Pt
        jetEt[0] = iTree.CSVJ1Et
        jetMt[0] = iTree.CSVJ1Mt
        jetptLeadTrk[0] = iTree.CSVJ1ptLeadTrk
        jetVtx3dL[0] = iTree.CSVJ1Vtx3dL
        jetVtx3deL[0] = iTree.CSVJ1Vtx3deL
        jetvtxMass[0] = iTree.CSVJ1vtxMass
        jetVtxPt[0] = iTree.CSVJ1VtxPt
        jetJECUnc[0] = iTree.CSVJ1JECUnc
        jetNtot[0] = iTree.CSVJ1Ntot
        jetSoftLeptPtRel[0] = iTree.CSVJ1SoftLeptPtRel
        jetSoftLeptPt[0] = iTree.CSVJ1SoftLeptPt
        jetSoftLeptdR[0] = iTree.CSVJ1SoftLeptdR    
        matchGenJetPt[0] = iTree.matchGenJet1Pt
        triggerEff[0] = iTree.triggerEff
        
        if options.var == 'j1' or options.var == 'both':
            oTree.Fill()

        jetPtUncorr[0] = iTree.CSVJ2PtUncorr
        jetPt[0] = iTree.CSVJ2Pt
        jetEt[0] = iTree.CSVJ2Et
        jetMt[0] = iTree.CSVJ2Mt
        jetptLeadTrk[0] = iTree.CSVJ2ptLeadTrk
        jetVtx3dL[0] = iTree.CSVJ2Vtx3dL
        jetVtx3deL[0] = iTree.CSVJ2Vtx3deL
        jetvtxMass[0] = iTree.CSVJ2vtxMass
        jetVtxPt[0] = iTree.CSVJ2VtxPt
        jetJECUnc[0] = iTree.CSVJ2JECUnc
        jetNtot[0] = iTree.CSVJ2Ntot
        jetSoftLeptPtRel[0] = iTree.CSVJ2SoftLeptPtRel
        jetSoftLeptPt[0] = iTree.CSVJ2SoftLeptPt
        jetSoftLeptdR[0] = iTree.CSVJ2SoftLeptdR   
        matchGenJetPt[0] = iTree.matchGenJet2Pt
        triggerEff[0] = iTree.triggerEff

        if options.var == 'j2' or options.var == 'both':
            oTree.Fill()
    print ''

oFile.cd()
oTree.Write()
nSaved = oTree.GetEntries()
oFile.Close()

print 'saved %i events at: %s_%s.root' %(nSaved,options.outputFile, options.var)