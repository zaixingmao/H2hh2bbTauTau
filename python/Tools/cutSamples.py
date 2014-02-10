#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars
from array import array

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()
combinedJJ = lvClass()
sv4Vec = lvClass()


def findFullMass(jetsList = [], sv4Vec = ''):
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    combinedJJ = jetsList[0][1]+jetsList[1][1]
    if jetsList[1][0] > 0 and jetsList[0][1].pt() > 0 and jetsList[1][1].pt() > 0:
      return combinedJJ.pt(), combinedJJ.eta(), combinedJJ.phi(), combinedJJ.mass(), jetsList[0][0], jetsList[1][0], (combinedJJ+sv4Vec).mass()
    else:
        return -1, -1, -1, -1, -1, -1, -1

r.gStyle.SetOptStat(0)

signalEntries = enVars.signalEntries
ttEntries = enVars.ttEntries
ZZEntries = enVars.ZZEntries

#*******Get Sample Name and Locations******
sampleLocations = enVars.sampleLocations

varList = ['EVENT', 'HMass', 'svMass', 'svPt', 'svEta', 'svPhi', 'J1Pt', 'J1Eta','J1Phi', 'J1Mass', 'NBTags', 'iso1', 'iso2', 'mJJ', 'J2Pt', 'J2Eta','J2Phi', 'J2Mass',
           'J3Pt', 'J3Eta','J3Phi', 'J3Mass', 'J4Pt', 'J4Eta','J4Phi', 'J4Mass', 'J1CSVbtag', 'J2CSVbtag', 'J3CSVbtag', 'J4CSVbtag']

for iSample in range(len(sampleLocations)):
    iChain = r.TChain("ttTreeFinal/eventTree")
    tool.addFiles(ch=iChain, dirName=sampleLocations[iSample][1], knownEventNumber=signalEntries)
    iChain.SetBranchStatus("*",0)
    for iVar in range(len(varList)):
        iChain.SetBranchStatus(varList[iVar],1)
    nEntires = iChain.GetEntries()
    fullMass = array('f', [0.])
    mJJ = array('f', [0.])
    ptJJ = array('f', [0.])
    etaJJ = array('f', [0.])
    phiJJ = array('f', [0.])
    CSVJ1 = array('f', [0.])
    CSVJ2 = array('f', [0.])
    iChain.LoadTree(0)
    iTree = iChain.GetTree().CloneTree(0)
    iFile = r.TFile("%s.root" %(sampleLocations[iSample][0]),"recreate")
    iTree.Branch("fMass", fullMass, "fMass/F")
    iTree.Branch("mJJ", mJJ, "mJJ/F")
    iTree.Branch("etaJJ", etaJJ, "etaJJ/F")
    iTree.Branch("phiJJ", phiJJ, "phiJJ/F")
    iTree.Branch("ptJJ", ptJJ, "ptJJ/F")
    iTree.Branch("CSVJ1", CSVJ1, "CSVJ1/F")
    iTree.Branch("CSVJ2", CSVJ2, "CSVJ2/F")

    counter = 0

    for iEntry in range(nEntires):
        iChain.LoadTree(iEntry)
        iChain.GetEntry(iEntry)
        if iChain.svMass.size() == 0:
            continue
        jetsList = [(iChain.J1CSVbtag, J1.SetCoordinates(iChain.J1Pt, iChain.J1Eta, iChain.J1Phi, iChain.J1Mass)),
                    (iChain.J2CSVbtag, J2.SetCoordinates(iChain.J2Pt, iChain.J2Eta, iChain.J2Phi, iChain.J2Mass)),
                    (iChain.J3CSVbtag, J3.SetCoordinates(iChain.J3Pt, iChain.J3Eta, iChain.J3Phi, iChain.J3Mass)),
                    (iChain.J4CSVbtag, J4.SetCoordinates(iChain.J4Pt, iChain.J4Eta, iChain.J4Phi, iChain.J4Mass))]
        sv4Vec.SetCoordinates(iChain.svPt.at(0), iChain.svEta.at(0), iChain.svPhi.at(0), iChain.svMass.at(0))
        ptJJ[0], etaJJ[0], phiJJ[0], mJJ[0], CSVJ1[0], CSVJ2[0], fullMass[0] = findFullMass(jetsList=jetsList, sv4Vec=sv4Vec) 
        iTree.Fill()
        counter += 1
        tool.printProcessStatus(iEntry, nEntires, 'Saving to file %s.root' %(sampleLocations[iSample][0]))
    print ''

    iFile.cd()
    iTree.Write()
    iFile.Close()
