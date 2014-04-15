#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars
from array import array
import optparse
import math

xLabels = ['processedEvents', 'PATSkimmedEvents', 'atLeastOneDiTau', 'ptEta1', 'ptEta2', 'tau1Hadronic', 'tau2Hadronic',
           'muonVeto1', 'muonVeto2', 'eleVeto1', 'eleVeto2', 'isolation1', 'relaxed']

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()
CSVJet1 = lvClass()
CSVJet2 = lvClass()
tau1 = lvClass()
tau2 = lvClass()
combinedJJ = lvClass()
sv4Vec = lvClass()

def calcTrigOneTauEff(eta, pt, data = True, fitStart=25):
        le14_da = {20: (0.898, 44.3, 1.02),
                  25: (0.866, 43.1, 0.86),
                  30: (0.839, 42.3, 0.73),
                  35: (0.846, 42.4, 0.78),
                  }
        le14_mc = {20: (0.837, 43.6, 1.09),
                   25: (0.832, 40.4, 0.80),
                   30: (0.829, 40.4, 0.74),
                   35: (0.833, 40.1, 0.86),
                   }
        ge16_da = {20: (0.81, 43.6, 1.09),
                   25: (0.76, 41.8, 0.86),
                   30: (0.74, 41.2, 0.75),
                   35: (0.74, 41.2, 0.79),
                   }
        ge16_mc = {20: (0.70, 39.7, 0.95),
                   25: (0.69, 38.6, 0.74),
                   30: (0.69, 38.7, 0.61),
                   35: (0.69, 38.8, 0.61),
                   }
        le14 = le14_da if data else le14_mc
        ge16 = ge16_da if data else ge16_mc
        if abs(eta) < 1.4:
            d = le14
        else:
            d = ge16
        e, x0, sigma = d[fitStart]
        y = r.TMath.Erf((pt-x0)/2.0/sigma/math.sqrt(pt))  # https://github.com/rmanzoni/HTT/blob/master/CMGTools/H2TauTau/interface/TriggerEfficiency.h
        #y = r.TMath.Erf((pt-x0)/sigma/math.sqrt(2.0))
        return (1+y)*e/2.0

def opts():
    parser = optparse.OptionParser()
    parser.add_option("-l", dest="location", default="/scratch/zmao", help="location to be saved")
    parser.add_option("-n", dest="nevents", default="-1", help="amount of events to be saved")
    options, args = parser.parse_args()

    return options

options = opts()

def findFullMass(jetsList = [], sv4Vec = ''):
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    combinedJJ = jetsList[0][1]+jetsList[1][1]
    if jetsList[1][0] > 0 and jetsList[0][1].pt() > 30 and jetsList[1][1].pt() > 30 and abs(jetsList[0][1].eta()) < 2.4 and abs(jetsList[1][1].eta()) < 2.4:
        return combinedJJ, jetsList[0][0], jetsList[1][0], jetsList[0][1], jetsList[1][1], (combinedJJ+sv4Vec).mass(), r.Math.VectorUtil.DeltaR(jetsList[0][1], jetsList[1][1])
    else:
        return -1, -1, -1, -1, -1, -1, -1

def setDPhiInRange(dPhi):
    if dPhi > 3.14:
        return 6.283-dPhi
    else:
        return dPhi

def calcdPhiMetValues(tau1Phi, tau2Phi, j1Phi, j2Phi, metPhi, tauTauPhi, jjPhi, svPhi):
    return setDPhiInRange(abs(tau1Phi - metPhi)), setDPhiInRange(abs(tau2Phi - metPhi)), setDPhiInRange(abs(j1Phi - metPhi)), setDPhiInRange(abs(j2Phi - metPhi)), setDPhiInRange(abs(tauTauPhi - metPhi)), setDPhiInRange(abs(jjPhi - metPhi)),  setDPhiInRange(abs(svPhi - metPhi)) 

r.gStyle.SetOptStat(0)

signalEntries = enVars.signalEntries
ttEntries = enVars.ttEntries
ZZEntries = enVars.ZZEntries

#*******Get Sample Name and Locations******
sampleLocations = enVars.sampleLocations

varList = ['EVENT', 'HMass', 'svMass', 'svPt', 'svEta', 'svPhi', 'J1Pt', 'J1Eta','J1Phi', 'J1Mass', 'NBTags', 'iso1', 'iso2', 'mJJ', 'J2Pt', 'J2Eta','J2Phi', 'J2Mass','pZeta', 'pZ', 'm1', 'm2',
           'pZV', 'J3Pt', 'J3Eta','J3Phi', 'J3Mass', 'J4Pt', 'J4Eta','J4Phi', 'J4Mass', 'J1CSVbtag', 'J2CSVbtag', 'J3CSVbtag', 'J4CSVbtag', 'pt1', 'eta1', 'phi1', 'pt2', 'eta2', 'phi2', 'met', 
           'charge1', 'charge2',  'metphi',# 'genBPt', 'genBEta', 'genBPhi', 'genTauPt', 'genTauEta', 'genTauPhi', 'genElePt', 'genEleEta', 'genElePhi', 'genMuPt', 'genMuEta', 'genMuPhi',
          ]

blackList = enVars.corruptedROOTfiles

for iSample, iLocation in sampleLocations:

    cutFlow = r.TH1F()
    #tool.addHistFromFiles(dirName=iLocation, histName = "TT/results", hist = cutFlow, xAxisLabels=xLabels)
    tool.addHistFromFiles(dirName=iLocation, histName = "preselection", hist = cutFlow, xAxisLabels=xLabels)
    cutFlow.SetName('preselection')

    #iChain = r.TChain("ttTreeBeforeChargeCut/eventTree")
    iChain = r.TChain("eventTree")
    nEntries = tool.addFiles(ch=iChain, dirName=iLocation, knownEventNumber=signalEntries, printTotalEvents=True, blackList=blackList)
    iChain.SetBranchStatus("*",0)
    for iVar in range(len(varList)):
        iChain.SetBranchStatus(varList[iVar],1)
    fullMass = array('f', [0.])
    mJJ = array('f', [0.])
    ptJJ = array('f', [0.])
    etaJJ = array('f', [0.])
    phiJJ = array('f', [0.])
    CSVJ1 = array('f', [0.])
    CSVJ2 = array('f', [0.])
    dRTauTau = array('f', [0.])
    dRJJ = array('f', [0.])
    dRhh = array('f', [0.])
    mTop1 = array('f', [0.])
    mTop2 = array('f', [0.])
    pZ_new = array('f', [0.])
    pZV_new = array('f', [0.])
    pZ_new2 = array('f', [0.])
    pZV_new2 = array('f', [0.])
    triggerEff = array('f', [0.])
    metTau1DPhi = array('f', [0.])
    metTau2DPhi = array('f', [0.])
    metJ1DPhi = array('f', [0.])
    metJ2DPhi = array('f', [0.])
    metTauPairDPhi = array('f', [0.])
    metJetPairDPhi = array('f', [0.])
    metSvTauPairDPhi = array('f', [0.])
    iChain.LoadTree(0)
    iTree = iChain.GetTree().CloneTree(0)
    iSample = iSample + '_%s' %('all' if options.nevents == "-1" else options.nevents)
    iFile = r.TFile("%s/%s.root" %(options.location,iSample),"recreate")
    iTree.Branch("fMass", fullMass, "fMass/F")
    iTree.Branch("mJJ", mJJ, "mJJ/F")
    iTree.Branch("etaJJ", etaJJ, "etaJJ/F")
    iTree.Branch("phiJJ", phiJJ, "phiJJ/F")
    iTree.Branch("ptJJ", ptJJ, "ptJJ/F")
    iTree.Branch("CSVJ1", CSVJ1, "CSVJ1/F")
    iTree.Branch("CSVJ2", CSVJ2, "CSVJ2/F")
    iTree.Branch("dRTauTau", dRTauTau, "dRTauTau/F")
    iTree.Branch("dRJJ", dRJJ, "dRJJ/F")
    iTree.Branch("dRhh", dRhh, "dRhh/F")
    iTree.Branch("mTop1", mTop1, "mTop1/F")
    iTree.Branch("mTop2", mTop2, "mTop2/F")
    iTree.Branch("pZ_new", pZ_new, "pZ_new/F")
    iTree.Branch("pZV_new", pZV_new, "pZV_new/F")
    iTree.Branch("pZ_new2", pZ_new2, "pZ_new2/F")
    iTree.Branch("pZV_new2", pZV_new2, "pZV_new2/F")
    iTree.Branch("triggerEff", triggerEff, "triggerEff/F")
    iTree.Branch("metTau1DPhi", metTau1DPhi, "metTau1DPhi/F")
    iTree.Branch("metTau2DPhi", metTau2DPhi, "metTau2DPhi/F")
    iTree.Branch("metJ1DPhi", metJ1DPhi, "metJ1DPhi/F")
    iTree.Branch("metJ2DPhi", metJ2DPhi, "metJ2DPhi/F")
    iTree.Branch("metTauPairDPhi", metTauPairDPhi, "metTauPairDPhi/F")
    iTree.Branch("metJetPairDPhi", metJetPairDPhi, "metJetPairDPhi/F")
    iTree.Branch("metSvTauPairDPhi", metSvTauPairDPhi, "metSvTauPairDPhi/F")

    counter = 0

    for iEntry in range(nEntries):
        iChain.LoadTree(iEntry)
        iChain.GetEntry(iEntry)
        if counter == int(options.nevents):
            break
        if iChain.svMass.size() == 0:
            continue
        if not tool.calc(iChain):
            continue
#         if iChain.charge1.at(0) - iChain.charge2.at(0) == 0: #sign requirement
#             continue
        if iChain.pt1.at(0)<45 or iChain.pt2.at(0)<45: #pt cut
            continue        
        if abs(iChain.eta1.at(0))>2.1 or abs(iChain.eta2.at(0))>2.1: #pt cut
            continue        

        jetsList = [(iChain.J1CSVbtag, J1.SetCoordinates(iChain.J1Pt, iChain.J1Eta, iChain.J1Phi, iChain.J1Mass)),
                    (iChain.J2CSVbtag, J2.SetCoordinates(iChain.J2Pt, iChain.J2Eta, iChain.J2Phi, iChain.J2Mass)),
                    (iChain.J3CSVbtag, J3.SetCoordinates(iChain.J3Pt, iChain.J3Eta, iChain.J3Phi, iChain.J3Mass)),
                    (iChain.J4CSVbtag, J4.SetCoordinates(iChain.J4Pt, iChain.J4Eta, iChain.J4Phi, iChain.J4Mass))]
        sv4Vec.SetCoordinates(iChain.svPt.at(0), iChain.svEta.at(0), iChain.svPhi.at(0), iChain.svMass.at(0))
        bb = lvClass()
        bb, CSVJ1[0], CSVJ2[0], CSVJet1, CSVJet2, fullMass[0], dRJJ[0] = findFullMass(jetsList=jetsList, sv4Vec=sv4Vec) 
        if bb == -1:
            continue
        ptJJ[0] = bb.pt()
        etaJJ[0] = bb.eta()
        phiJJ[0] = bb.phi()
        mJJ[0] = bb.mass()
        tau1.SetCoordinates(iChain.pt1.at(0), iChain.eta1.at(0), iChain.phi1.at(0), iChain.m1.at(0))
        tau2.SetCoordinates(iChain.pt2.at(0), iChain.eta2.at(0), iChain.phi2.at(0), iChain.m2.at(0))
        mTop1[0] = (CSVJet1 + tau1).mass()
        mTop2[0] = (CSVJet2 + tau2).mass()

        pZ_new[0] = iChain.pZ/iChain.svPt.at(0)
        pZV_new[0] = iChain.pZV/iChain.svPt.at(0)
        pZ_new2[0] = iChain.pZ/fullMass[0]
        pZV_new2[0] = iChain.pZV/fullMass[0]

        dRTauTau[0] = r.Math.VectorUtil.DeltaR(tau1, tau2)
        dRhh[0] = r.Math.VectorUtil.DeltaR(bb, sv4Vec)

        metTau1DPhi[0], metTau2DPhi[0], metJ1DPhi[0], metJ2DPhi[0], metTauPairDPhi[0], metJetPairDPhi[0], metSvTauPairDPhi[0] = calcdPhiMetValues(iChain.phi1.at(0), iChain.phi2.at(0), CSVJet1.phi(), CSVJet2.phi(), iChain.metphi.at(0), (tau1+tau2).phi(), bb.phi(), iChain.svPhi.at(0))

        eff1 = calcTrigOneTauEff(eta=iChain.eta1.at(0), pt=iChain.pt1.at(0), data = True, fitStart=25)
        eff2 = calcTrigOneTauEff(eta=iChain.eta2.at(0), pt=iChain.pt2.at(0), data = True, fitStart=25)
        triggerEff[0] = eff1*eff2
        iTree.Fill()
        counter += 1
        tool.printProcessStatus(iEntry, nEntries, 'Saving to file %s.root' %(iSample))
    print '  -- saved %d events' %(counter)

    iFile.cd()
    cutFlow.Write()
    iTree.Write()
    iFile.Close()
