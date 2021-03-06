#!/usr/bin/env python
import sys
import ROOT as r
import time
from operator import itemgetter
import os


varsRange = { 
#             'fMass': (10, 200, 800, 30, 100, False, True),
#             'pt2': (12, 30, 150, 10000, 100, True, True, 'GeV'),
#              'tightPt': (20, 0, 400, 10000, 100, True, True),
#              'relaxPt': (20, 0, 400, 10000, 100, True, True),
#             'pt1pt2': (20, 0, 500, 10000, 100, True, True),
#             'iso1':(25, 0, 10, 20000, 600, True, True),
#             'iso2':(25, 0, 10, 20000, 600, True, True),
#             'eta1': (20, -3.14, 3.14, 50000, 100, True, True), 
#             'eta2': (20, -3.14, 3.14, 50000, 100, True, True), 
#             'phi1': (20, -3.14, 3.14, 50000, 100, True, True, 'rad'), 
#             'phi2': (20, -3.14, 3.14, 50000, 100, True, True, 'rad'), 
#             'NBTags': (6, 0, 5, 2000, 100, True, True), 
#             'J1CSVbtag': (12, 0, 1.2, 100000, 100, True, True),
#             'J1Eta': (20, -3.14, 3.14, 50000, 100, True, True),
#             'J1Pt': (20, 0, 400, 30000, 100, True, True),
#             'J2CSVbtag': (12, 0, 1.2, 100000, 100, True, True),
#             'J2Eta': (20, -3.14, 3.14, 50000, 100, True, True),
#             'J2Pt': (15, 0, 250, 10000, 100, True, True),
#             'J3CSVbtag':(12, 0, 1.2, 50000, 100, True, True),
#            'J3Eta': (20, -3.14, 3.14, 50000, 100, True, True),
#             'J3Pt': (15, 0, 250, 5000, 100, True, True),
#             'J4CSVbtag':(12, 0, 1.2, 50000, 100, True, True),
#             'J4Eta': (20, -3.14, 3.14, 10000, 100, True, True),
#             'J4Pt': (15, 0, 250, 5000, 100, True, True),
#             'svMass': (10, 0, 400, 20, 100, False, True),
#             'svPt': (10, 0, 600, 50, 100, False, True),
#              'mJJ': (15, 80, 150, 30000, 100, True, True),
#              'mJJReg': (10, 50, 200, 20, 100, False, True),
#              'met': (10, 0, 150, 30, 100, False, True),
#             'ptJJ': (15, 0, 600, 5000, 100, True, True),
#             'etaJJ': (20, -3.14, 3.14, 50000, 100, True, True),
#             'dPhiMetTau1': (8, 0, 3.14, 60, 100, False, True),
#             'dPhiMetTau2': (8, 0, 3.14, 20, 100, False, True),
#             'dPhiMetJet1': (8, 0, 3.14, 60, 100, False, True),
#             'dPhiMetJet2': (8, 0, 3.14, 60, 100, False, True),
#             'dPhiMetTauPair': (8, 0, 3.14, 60, 100, False, True),
#             'dPhiMetJetPair': (8, 0, 3.14, 60, 100, False, True),
#             'dPhiMetSVTauPair': (8, 0, 3.14, 60, 100, False, True),
#             'dRTauTau': (10, 0, r.TMath.Pi(), 60, 100, False, True), 
#             'dPhiTauTau': (20, 0, r.TMath.Pi(), 5000, 500, True, True), 
#             'dEtaTauTau': (20, 0, r.TMath.Pi(), 5000, 500, True, True), 
#             'dRJJ': (10, 0, 6.28, 60, 100, False, True),
#             'dRhh': (10, 0, 6.28, 60, 100, False, True),
#             'BDT_EWK': (20, -1., 1., 10000, 100, True, True),
#             'BDT_QCD': (20, -1., 1., 10000, 100, True, True),
#             'BDT_both': (20, -1., 1., 30, 100, False, True, 'binWidth'),
#             'nTauPairs': (5, 0, 5, 10000, 100, True, True),
#             'CSVJ1': (10, 0.6, 1.2, 60, 100, False, True),
#             'CSVJ2': (10, 0.2, 1.2, 30, 100, False, True),
#             'fMass': (20, 150, 550, 20, 100, False, True),
#             'fMassKinFit': (20, 150, 550, 20, 100, False, True),
            'byIsolationMVA2raw_1': (20, -1., 1., 20, 100, False, True),
            'byIsolationMVA2raw_2': (20, -1., 1., 20, 100, False, True),
            }

def angleInPie(absAngle):
    if absAngle > r.TMath.Pi():
        return 2*r.TMath.Pi() - absAngle
    else:
        return absAngle


def findVar(iTree, varName):
    varsDict = {'EVENT': iTree.EVENT,
                'HMass': iTree.HMass, 
                'charge1': iTree.charge1.at(0), 
                'charge2': iTree.charge2.at(0),
                'pt1': iTree.pt1.at(0), 
                'pt2': iTree.pt2.at(0), 
                'tightPt': iTree.pt1.at(0) if iTree.iso1.at(0) < iTree.iso2.at(0) else iTree.pt2.at(0),
                'relaxPt': iTree.pt1.at(0) if iTree.iso1.at(0) > iTree.iso2.at(0) else iTree.pt2.at(0),
                'pt1pt2': iTree.pt1.at(0)+iTree.pt2.at(0), 
                'iso1': iTree.iso1.at(0), 
                'iso2': iTree.iso2.at(0), 
                'phi1': iTree.phi1.at(0), 
                'phi2': iTree.phi2.at(0), 
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
                'fMassKinFit': iTree.fMassKinFit,
                'dPhiMetTau1': iTree.metTau1DPhi,
                'dPhiMetTau2': iTree.metTau2DPhi,
                'dPhiMetJet1': iTree.metJ1DPhi,
                'dPhiMetJet2': iTree.metJ2DPhi,
                'dPhiMetTauPair': iTree.metTauPairDPhi,
                'dPhiMetJetPair': iTree.metJetPairDPhi,
                'dPhiMetSVTauPair': iTree.metSvTauPairDPhi,
                'dRTauTau': iTree.dRTauTau,
                'dPhiTauTau': angleInPie(abs(iTree.phi1.at(0) - iTree.phi2.at(0))),
                'dEtaTauTau': angleInPie(abs(iTree.eta1.at(0) - iTree.eta2.at(0))),
                'dRJJ': iTree.dRJJ,
                'dRhh': iTree.dRhh,
                'mJJReg': iTree.mJJReg,
#                 'BDT_EWK': iTree.BDT_EWK,
#                 'BDT_QCD': iTree.BDT_QCD,
#                 'BDT_both': iTree.BDT_both,
                'met': iTree.met.at(0),
                'svPt': iTree.svPt.at(0),
                'nTauPairs': iTree.pt1.size(),
                'byIsolationMVA2raw_1': iTree.byIsolationMVA2raw_1,
                'byIsolationMVA2raw_2': iTree.byIsolationMVA2raw_2,

#                 'J1GenPt': iTree.J1GenPt,
#                 'J1GenEta': iTree.J1GenEta,
#                 'J1GenPhi': iTree.J1GenPhi,
#                 'J1GenMass': iTree.J1GenMass,
#                 'J2GenPt': iTree.J2GenPt,
#                 'J2GenEta': iTree.J2GenEta,
#                 'J2GenPhi': iTree.J2GenPhi,
#                 'J2GenMass': iTree.J2GenMass,
#                 'J3GenPt': iTree.J3GenPt,
#                 'J3GenEta': iTree.J3GenEta,
#                 'J3GenPhi': iTree.J3GenPhi,
#                 'J3GenMass': iTree.J3GenMass,
#                 'J4GenPt': iTree.J4GenPt,
#                 'J4GenEta': iTree.J4GenEta,
#                 'J4GenPhi': iTree.J4GenPhi,
#                 'J4GenMass': iTree.J4GenMass,
#                 'genBPt': iTree.genBPt,
#                 'genBEta': iTree.genBEta,
#                 'genBPhi': iTree.genBPhi,
#                 'genBMass': iTree.genBMass,
    }
    
    if varName in varsDict:
        return varsDict[varName]
    else:
        print 'Variable: %s not defined in varList.py' %varName
        return 'Null'

def findVarInChain(iChain, varName):
    varsDict = {
                'J1GenPt': iChain.J1GenPt,
                'J1GenEta': iChain.J1GenEta,
                'J1GenPhi': iChain.J1GenPhi,
                'J1GenMass': iChain.J1GenMass,
                'J2GenPt': iChain.J2GenPt,
                'J2GenEta': iChain.J2GenEta,
                'J2GenPhi': iChain.J2GenPhi,
                'J2GenMass': iChain.J2GenMass,
                'J3GenPt': iChain.J3GenPt,
                'J3GenEta': iChain.J3GenEta,
                'J3GenPhi': iChain.J3GenPhi,
                'J3GenMass': iChain.J3GenMass,
                'J4GenPt': iChain.J4GenPt,
                'J4GenEta': iChain.J4GenEta,
                'J4GenPhi': iChain.J4GenPhi,
                'J4GenMass': iChain.J4GenMass,
                'J1PtUncorr': iChain.J1PtUncorr,
                'J1VtxPt': iChain.J1VtxPt,
                'J1Vtx3dL': iChain.J1Vtx3dL,
                'J1Vtx3deL': iChain.J1Vtx3deL,
                'J1ptLeadTrk': iChain.J1ptLeadTrk,
                'J1vtxMass': iChain.J1vtxMass,
                'J1vtxPt': iChain.J1vtxPt,
                'J1Ntot': iChain.J1Ntot,
                'J1SoftLeptPt': iChain.J1SoftLepPt,
                'J1SoftLeptEta': iChain.J1SoftLepEta,
                'J1SoftLeptPhi': iChain.J1SoftLepPhi,
                'J1SoftLeptPID': iChain.J1SoftLepPID,
                'J1JECUnc': iChain.J1JECUnc,
                'J1Et': iChain.J1Et,
                'J1Mt': iChain.J1Mt,

                'J2PtUncorr': iChain.J2PtUncorr,
                'J2VtxPt': iChain.J2VtxPt,
                'J2Vtx3dL': iChain.J2Vtx3dL,
                'J2Vtx3deL': iChain.J2Vtx3deL,
                'J2ptLeadTrk': iChain.J2ptLeadTrk,
                'J2vtxMass': iChain.J2vtxMass,
                'J2vtxPt': iChain.J2vtxPt,
                'J2Ntot': iChain.J2Ntot,
                'J2SoftLeptPt': iChain.J2SoftLepPt,
                'J2SoftLeptEta': iChain.J2SoftLepEta,
                'J2SoftLeptPhi': iChain.J2SoftLepPhi,
                'J2SoftLeptPID': iChain.J2SoftLepPID,
                'J2JECUnc': iChain.J2JECUnc,
                'J2Et': iChain.J2Et,
                'J2Mt': iChain.J2Mt,

                'J3PtUncorr': iChain.J3PtUncorr,
                'J3VtxPt': iChain.J3VtxPt,
                'J3Vtx3dL': iChain.J3Vtx3dL,
                'J3Vtx3deL': iChain.J3Vtx3deL,
                'J3ptLeadTrk': iChain.J3ptLeadTrk,
                'J3vtxMass': iChain.J3vtxMass,
                'J3vtxPt': iChain.J3vtxPt,
                'J3Ntot': iChain.J3Ntot,
                'J3SoftLeptPt': iChain.J3SoftLepPt,
                'J3SoftLeptEta': iChain.J3SoftLepEta,
                'J3SoftLeptPhi': iChain.J3SoftLepPhi,
                'J3SoftLeptPID': iChain.J3SoftLepPID,
                'J3JECUnc': iChain.J3JECUnc,
                'J3Et': iChain.J3Et,
                'J3Mt': iChain.J3Mt,

                'J4PtUncorr': iChain.J4PtUncorr,
                'J4VtxPt': iChain.J4VtxPt,
                'J4Vtx3dL': iChain.J4Vtx3dL,
                'J4Vtx3deL': iChain.J4Vtx3deL,
                'J4ptLeadTrk': iChain.J4ptLeadTrk,
                'J4vtxMass': iChain.J4vtxMass,
                'J4vtxPt': iChain.J4vtxPt,
                'J4Ntot': iChain.J4Ntot,
                'J4SoftLeptPt': iChain.J4SoftLepPt,
                'J4SoftLeptEta': iChain.J4SoftLepEta,
                'J4SoftLeptPhi': iChain.J4SoftLepPhi,
                'J4SoftLeptPID': iChain.J4SoftLepPID,
                'J4JECUnc': iChain.J4JECUnc,
                'J4Et': iChain.J4Et,
                'J4Mt': iChain.J4Mt,

                'J1Eta': iChain.J1Eta,
                'J1Mass': iChain.J1Mass,
                'J1Pt': iChain.J1Pt,
                'J1Phi': iChain.J1Phi,
                'J2Eta': iChain.J2Eta,
                'J2Mass': iChain.J2Mass,
                'J2Pt': iChain.J2Pt,
                'J2Phi': iChain.J2Phi,
                'J3Eta': iChain.J3Eta,
                'J3Mass': iChain.J3Mass,
                'J3Pt': iChain.J3Pt,
                'J3Phi': iChain.J3Phi,
                'J4Eta': iChain.J4Eta,
                'J4Mass': iChain.J4Mass,
                'J4Pt': iChain.J4Pt,
                'J4Phi': iChain.J4Phi,

#                 'genBPt': iChain.genBPt,
#                 'genBEta': iChain.genBEta,
#                 'genBPhi': iChain.genBPhi,
#                 'genBMass': iChain.genBMass,
    }

def findVarInChain_Data(iChain, varName):
    varsDict = {
                'J1PtUncorr': iChain.J1PtUncorr,
                'J1VtxPt': iChain.J1VtxPt,
                'J1Vtx3dL': iChain.J1Vtx3dL,
                'J1Vtx3deL': iChain.J1Vtx3deL,
                'J1ptLeadTrk': iChain.J1ptLeadTrk,
                'J1vtxMass': iChain.J1vtxMass,
                'J1vtxPt': iChain.J1vtxPt,
                'J1Ntot': iChain.J1Ntot,
                'J1SoftLeptPt': iChain.J1SoftLepPt,
                'J1SoftLeptEta': iChain.J1SoftLepEta,
                'J1SoftLeptPhi': iChain.J1SoftLepPhi,
                'J1SoftLeptPID': iChain.J1SoftLepPID,
                'J1JECUnc': iChain.J1JECUnc,
                'J1Et': iChain.J1Et,
                'J1Mt': iChain.J1Mt,

                'J2PtUncorr': iChain.J2PtUncorr,
                'J2VtxPt': iChain.J2VtxPt,
                'J2Vtx3dL': iChain.J2Vtx3dL,
                'J2Vtx3deL': iChain.J2Vtx3deL,
                'J2ptLeadTrk': iChain.J2ptLeadTrk,
                'J2vtxMass': iChain.J2vtxMass,
                'J2vtxPt': iChain.J2vtxPt,
                'J2Ntot': iChain.J2Ntot,
                'J2SoftLeptPt': iChain.J2SoftLepPt,
                'J2SoftLeptEta': iChain.J2SoftLepEta,
                'J2SoftLeptPhi': iChain.J2SoftLepPhi,
                'J2SoftLeptPID': iChain.J2SoftLepPID,
                'J2JECUnc': iChain.J2JECUnc,
                'J2Et': iChain.J2Et,
                'J2Mt': iChain.J2Mt,

                'J3PtUncorr': iChain.J3PtUncorr,
                'J3VtxPt': iChain.J3VtxPt,
                'J3Vtx3dL': iChain.J3Vtx3dL,
                'J3Vtx3deL': iChain.J3Vtx3deL,
                'J3ptLeadTrk': iChain.J3ptLeadTrk,
                'J3vtxMass': iChain.J3vtxMass,
                'J3vtxPt': iChain.J3vtxPt,
                'J3Ntot': iChain.J3Ntot,
                'J3SoftLeptPt': iChain.J3SoftLepPt,
                'J3SoftLeptEta': iChain.J3SoftLepEta,
                'J3SoftLeptPhi': iChain.J3SoftLepPhi,
                'J3SoftLeptPID': iChain.J3SoftLepPID,
                'J3JECUnc': iChain.J3JECUnc,
                'J3Et': iChain.J3Et,
                'J3Mt': iChain.J3Mt,

                'J4PtUncorr': iChain.J4PtUncorr,
                'J4VtxPt': iChain.J4VtxPt,
                'J4Vtx3dL': iChain.J4Vtx3dL,
                'J4Vtx3deL': iChain.J4Vtx3deL,
                'J4ptLeadTrk': iChain.J4ptLeadTrk,
                'J4vtxMass': iChain.J4vtxMass,
                'J4vtxPt': iChain.J4vtxPt,
                'J4Ntot': iChain.J4Ntot,
                'J4SoftLeptPt': iChain.J4SoftLepPt,
                'J4SoftLeptEta': iChain.J4SoftLepEta,
                'J4SoftLeptPhi': iChain.J4SoftLepPhi,
                'J4SoftLeptPID': iChain.J4SoftLepPID,
                'J4JECUnc': iChain.J4JECUnc,
                'J4Et': iChain.J4Et,
                'J4Mt': iChain.J4Mt,

                'J1Eta': iChain.J1Eta,
                'J1Mass': iChain.J1Mass,
                'J1Pt': iChain.J1Pt,
                'J1Phi': iChain.J1Phi,
                'J2Eta': iChain.J2Eta,
                'J2Mass': iChain.J2Mass,
                'J2Pt': iChain.J2Pt,
                'J2Phi': iChain.J2Phi,
                'J3Eta': iChain.J3Eta,
                'J3Mass': iChain.J3Mass,
                'J3Pt': iChain.J3Pt,
                'J3Phi': iChain.J3Phi,
                'J4Eta': iChain.J4Eta,
                'J4Mass': iChain.J4Mass,
                'J4Pt': iChain.J4Pt,
                'J4Phi': iChain.J4Phi,
    }
    

    if varName in varsDict:
        return varsDict[varName]
    else:
        print 'Variable: %s not defined in varList.py' %varName
        return 'Null'
