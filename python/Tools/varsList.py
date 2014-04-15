#!/usr/bin/env python
import sys
import ROOT as r
import time
from operator import itemgetter
import os


varsRange = { 
#               'HMass': (15, 200, 800, 100, 100, True),
#               'fMass': (15, 200, 800, 100, 100, True),
#             'pt1': (15, 0, 600, 100, 100, True),
#             'pt2': (15, 0, 600, 100, 100, True),
#             'iso1': iTree.iso1.at(0), 
#             'iso2': iTree.iso2.at(0), 
#             'eta1': iTree.eta1.at(0), 
#             'eta2': iTree.eta2.at(0), 
#             'NBTags': iTree.NBTags, 
#             'J1CSVbtag': iTree.J1CSVbtag,
#             'J1Eta': iTree.J1Eta,
#             'J1Mass': iTree.J1Mass,
#             'J1Phi': iTree.J1Phi,
#             'J1Pt': (15, 0, 600, 100, 100, True),
#             'J2CSVbtag': iTree.J1CSVbtag,
#             'J2Eta': iTree.J1Eta,
#             'J2Mass': iTree.J1Mass,
#             'J2Phi': iTree.J1Phi,
#             'J2Pt': (15, 0, 600, 100, 100, True),
#             'J3CSVbtag': iTree.J1CSVbtag,
#             'J3Eta': iTree.J1Eta,
#             'J3Mass': iTree.J1Mass,
#             'J3Phi': iTree.J1Phi,
#             'J3Pt': (15, 0, 600, 100, 100, True),
#             'J4CSVbtag': iTree.J1CSVbtag,
#             'J4Eta': iTree.J1Eta,
#             'J4Mass': iTree.J1Mass,
#             'J4Phi': iTree.J1Phi,
#             'J4Pt': (15, 0, 600, 100, 100, True),
#             'svMass': (15, 0, 600, 100, 100, True),
#             'mJJ': (15, 0, 600, 100, 100, True),
#             'dPhiMetTau1': (11, 0, 3.3, 500, 100, True),
#             'dPhiMetTau2': (11, 0, 3.3, 500, 100, True),
#             'dPhiMetJet1': (11, 0, 3.3, 500, 100, True),
#             'dPhiMetJet2': (11, 0, 3.3, 500, 100, True),
#             'dPhiMetTauPair': (11, 0, 3.3, 500, 100, True),
#             'dPhiMetJetPair': (11, 0, 3.3, 500, 100, True),
#             'dPhiMetSVTauPair': (11, 0, 3.3, 500, 100, True),
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
                'J1Phi': iTree.J1Phi,
                'J1Pt': iTree.J1Pt,
                'J2CSVbtag': iTree.J2CSVbtag,
                'J2Eta': iTree.J2Eta,
                'J2Mass': iTree.J2Mass,
                'J2Phi': iTree.J2Phi,
                'J2Pt': iTree.J2Pt,
                'J3CSVbtag': iTree.J3CSVbtag,
                'J3Eta': iTree.J3Eta,
                'J3Mass': iTree.J3Mass,
                'J3Phi': iTree.J3Phi,
                'J3Pt': iTree.J3Pt,
                'J4CSVbtag': iTree.J4CSVbtag,
                'J4Eta': iTree.J4Eta,
                'J4Mass': iTree.J4Mass,
                'J4Phi': iTree.J4Phi,
                'J4Pt': iTree.J4Pt,
                'svMass': iTree.svMass.at(0),
                'mJJ': iTree.mJJ,
                'fMass': iTree.fMass,
                'dPhiMetTau1': iTree.metTau1DPhi,
                'dPhiMetTau2': iTree.metTau2DPhi,
                'dPhiMetJet1': iTree.metJ1DPhi,
                'dPhiMetJet2': iTree.metJ2DPhi,
                'dPhiMetTauPair': iTree.metTauPairDPhi,
                'dPhiMetJetPair': iTree.metJetPairDPhi,
                'dPhiMetSVTauPair': iTree.metSvTauPairDPhi,}
    
    if varName in varsDict:
        return varsDict[varName]
    else:
        print 'Variable: %s not defined in varList.py' %varName
        return 'Null'
