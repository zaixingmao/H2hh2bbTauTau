#!/usr/bin/env python
import sys
import ROOT as r
import time
from operator import itemgetter
import os


varsRange = { 
            'HMass': (15, 200, 800, 100, 100, True),
            'fMass': (15, 200, 800, 100, 100, True),
            'pt1': (15, 0, 600, 100, 100, True),
            'pt2': (15, 0, 600, 100, 100, True),
            'iso1':(8, 0, 1.6, 600, 600, True),
            'iso2':(20, 0, 4, 600, 600, True),
            'eta1': (20, -3.14, 3.14, 500, 100, True), 
            'eta2': (20, -3.14, 3.14, 500, 100, True), 
#             'NBTags': (6, 0, 5, 500, 100, True), 
            'J1CSVbtag': (12, 0, 1.2, 1000, 100, True),
            'J1Eta': (20, -3.14, 3.14, 500, 100, True),
            'J1Pt': (15, 0, 600, 100, 100, True),
            'J2CSVbtag': (12, 0, 1.2, 1000, 100, True),
            'J2Eta': (20, -3.14, 3.14, 500, 100, True),
            'J2Pt': (15, 0, 600, 100, 100, True),
            'J3CSVbtag':(12, 0, 1.2, 1000, 100, True),
            'J3Eta': (20, -3.14, 3.14, 500, 100, True),
            'J3Pt': (15, 0, 600, 100, 100, True),
            'J4CSVbtag':(12, 0, 1.2, 1000, 100, True),
            'J4Eta': (20, -3.14, 3.14, 500, 100, True),
            'J4Pt': (15, 0, 600, 100, 100, True),
            'svMass': (15, 0, 600, 100, 100, True),
            'mJJ': (15, 0, 600, 100, 100, True),
            'ptJJ': (15, 0, 600, 100, 100, True),
            'etaJJ': (20, -3.14, 3.14, 500, 100, True),
            'dPhiMetTau1': (10, 0, 3.14, 500, 100, True),
            'dPhiMetTau2': (10, 0, 3.14, 500, 100, True),
            'dPhiMetJet1': (10, 0, 3.14, 500, 100, True),
            'dPhiMetJet2': (10, 0, 3.14, 500, 100, True),
            'dPhiMetTauPair': (10, 0, 3.14, 500, 100, True),
            'dPhiMetJetPair': (10, 0, 3.14, 500, 100, True),
            'dPhiMetSVTauPair': (10, 0, 3.14, 500, 100, True),
            'dRTauTau': (20, 0, 6.28, 500, 100, True), 
            'dRJJ': (20, 0, 6.28, 500, 100, True),
            'dRhh': (20, 0, 6.28, 500, 100, True),
            }

def findVar(iTree, varName):
    varsDict = {'EVENT': iTree.EVENT,
                'HMass': iTree.HMass, 
                'charge1': iTree.charge1.at(0), 
                'charge2': iTree.charge2.at(0),
                'pt1': iTree.pt1.at(0), 
                'pt2': iTree.pt2.at(0), 
                'iso1': iTree.iso1.at(0), 
                'iso2': iTree.iso2.at(0), 
                'eta1': iTree.eta1.at(0), 
                'eta2': iTree.eta2.at(0), 
                'NBTags': iTree.NBTags, 
                'J1CSVbtag': iTree.J1CSVbtag,
                'J1Eta': iTree.J1Eta,
                'J1Mass': iTree.J1Mass,
                'J1Pt': iTree.J1Pt,
                'J2CSVbtag': iTree.J2CSVbtag,
                'J2Eta': iTree.J2Eta,
                'J2Mass': iTree.J2Mass,
                'J2Pt': iTree.J2Pt,
                'J3CSVbtag': iTree.J3CSVbtag,
                'J3Eta': iTree.J3Eta,
                'J3Mass': iTree.J3Mass,
                'J3Pt': iTree.J3Pt,
                'J4CSVbtag': iTree.J4CSVbtag,
                'J4Eta': iTree.J4Eta,
                'J4Mass': iTree.J4Mass,
                'J4Pt': iTree.J4Pt,
                'svMass': iTree.svMass.at(0),
                'mJJ': iTree.mJJ,
                'ptJJ': iTree.ptJJ,
                'etaJJ': iTree.etaJJ,
                'CSVJ1': iTree.CSVJ1,
                'CSVJ2': iTree.CSVJ2,
                'fMass': iTree.fMass,
                'dPhiMetTau1': iTree.metTau1DPhi,
                'dPhiMetTau2': iTree.metTau2DPhi,
                'dPhiMetJet1': iTree.metJ1DPhi,
                'dPhiMetJet2': iTree.metJ2DPhi,
                'dPhiMetTauPair': iTree.metTauPairDPhi,
                'dPhiMetJetPair': iTree.metJetPairDPhi,
                'dPhiMetSVTauPair': iTree.metSvTauPairDPhi,
                'dRTauTau': iTree.dRTauTau,
                'dRJJ': iTree.dRJJ,
                'dRhh': iTree.dRhh,
    }
    
    if varName in varsDict:
        return varsDict[varName]
    else:
        print 'Variable: %s not defined in varList.py' %varName
        return 'Null'
