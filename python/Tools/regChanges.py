#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import math
import optparse
import os
from array import array

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
tau1 = lvClass()
tau2 = lvClass()
tau1True = lvClass()
tau2True = lvClass()
tau1RegTrue = lvClass()
tau2RegTrue = lvClass()
met1 = lvClass()
met2 = lvClass()
met1Reg = lvClass()
met2Reg = lvClass()

def reverseAngle(phi):
    if phi > 0:
        return phi - 3.14
    else:
        return phi + 3.14    

def calcMetInTaus(met, metPhi, phi1, phi2, eta1, eta2, etaPair):

    t1 = r.TVector3()
    t2 = r.TVector3()
    metV = r.TVector3()

    t1.SetPtEtaPhi(1., 0, phi1)
    t2.SetPtEtaPhi(1., 0, phi2)
    metV.SetPtEtaPhi(met, 0, metPhi)
#     metT1 = metV*t1
#     metT2 = metV*t2
    metT1 = (metV*t1 - (t1*t2)*(metV*t2))/(1-(t1*t2)*(t1*t2))
    metT2 = (metV*t2 - (t1*t2)*(metV*t1))/(1-(t1*t2)*(t1*t2))
    return metT1, metT2

def calcMetReg(met, metPhi, deltaJ1, deltaJ2, j1Phi, j2Phi):
    if deltaJ1 < 0:
        deltaJ1 = - deltaJ1
        j1Phi = reverseAngle(j1Phi)
    if deltaJ2 < 0:
        deltaJ2 = - deltaJ2
        j2Phi = reverseAngle(j2Phi)
    j1 = r.TVector3()
    j2 = r.TVector3()
    metV = r.TVector3()
    metV.SetPtEtaPhi(met, 0, metPhi)
    j1.SetPtEtaPhi(deltaJ1, 0, reverseAngle(j1Phi))
    j2.SetPtEtaPhi(deltaJ2, 0, reverseAngle(j2Phi))
    return (metV + j1 + j2).Pt(), (metV + j1 + j2).Phi() 

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--i", dest="inputFile", default = '', help="")
    options, args = parser.parse_args()
    return options

options = opts()

iFileName = options.inputFile

iFile = r.TFile(iFileName)
iTree = iFile.Get("eventTree")
cutFlow = iFile.Get("preselection")
total = iTree.GetEntries()

metReg = array('f', [0.])
metRegPhi = array('f', [0.])
metInTauPair = array('f', [0.])
metRegInTauPair = array('f', [0.])
mTauPair = array('f', [0.])
mTauPairWithMet = array('f', [0.])
mTauPairWithMetReg = array('f', [0.])

oFile = r.TFile(iFileName[0:iFileName.rfind('.root')] + '_new.root',"RECREATE")

tree = iTree.CloneTree(0)
tree.Branch("metReg",metReg,"metReg/F")
tree.Branch("metRegPhi",metRegPhi,"metRegPhi/F")
tree.Branch("mTauPair",mTauPair,"mTauPair/F")
tree.Branch("metInTauPair",metInTauPair,"metInTauPair/F")
tree.Branch("metRegInTauPair",metRegInTauPair,"metRegInTauPair/F")
tree.Branch("mTauPairWithMet",mTauPairWithMet,"mTauPairWithMet/F")
tree.Branch("mTauPairWithMetReg",mTauPairWithMetReg,"mTauPairWithMetReg/F")

for i in range(total):
    tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample %s' %iFileName)
    iTree.GetEntry(i)
    metReg[0], metRegPhi[0] = calcMetReg(iTree.met.at(0), iTree.metphi.at(0), 
                                         iTree.CSVJ1PtReg - iTree.CSVJ1Pt,
                                         iTree.CSVJ2PtReg - iTree.CSVJ2Pt,
                                         iTree.CSVJ1Phi, iTree.CSVJ2Phi)
    tau1.SetCoordinates(iTree.pt1.at(0), iTree.eta1.at(0), iTree.phi1.at(0), iTree.m1.at(0))
    tau2.SetCoordinates(iTree.pt2.at(0), iTree.eta2.at(0), iTree.phi2.at(0), iTree.m2.at(0))
    tauPairPhi = (tau1+tau2).phi()
    tauPairEta = (tau1+tau2).eta()
    metInTauPair[0] = iTree.met.at(0)*math.cos(iTree.metphi.at(0) - tauPairPhi)
    metRegInTauPair[0] = metReg[0]*math.cos(metRegPhi[0] - tauPairPhi)
    metInTau1 = iTree.met.at(0)*math.cos(iTree.metphi.at(0) - iTree.phi1.at(0))
    metInTau2 = iTree.met.at(0)*math.cos(iTree.metphi.at(0) - iTree.phi2.at(0))
    mTauPair[0] = (tau1+tau2).mass()

    met1_mod, met2_mod = calcMetInTaus(iTree.met.at(0), iTree.metphi.at(0), iTree.phi1.at(0), iTree.phi2.at(0), iTree.eta1.at(0), iTree.eta2.at(0), tauPairEta)

#     tau1True.SetCoordinates(tau1.pt()+met1_mod, iTree.eta1.at(0), iTree.phi1.at(0), tau1.mass())
#     tau2True.SetCoordinates(tau2.pt()+met2_mod, iTree.eta2.at(0), iTree.phi2.at(0), tau2.mass())
    if met1_mod < 0:
        tau1True.SetCoordinates(tau1.pt(), iTree.eta1.at(0), iTree.phi1.at(0), tau1.mass())
    else:
        tau1True.SetCoordinates(met1_mod, iTree.eta1.at(0), iTree.phi1.at(0), 0)
        tau1True = tau1 + tau1True
    if met2_mod < 0:
        tau2True.SetCoordinates(tau2.pt(), iTree.eta2.at(0), iTree.phi2.at(0), tau2.mass())
    else:
        tau2True.SetCoordinates(met2_mod, iTree.eta2.at(0), iTree.phi2.at(0), 0)
        tau2True = tau2 + tau2True
    mTauPairWithMet[0] = (tau1True+tau2True).mass()

    met1Reg_mod, met2Reg_mod = calcMetInTaus(metReg[0], metRegPhi[0], iTree.phi1.at(0), iTree.phi2.at(0), iTree.eta1.at(0), iTree.eta2.at(0), tauPairEta)
    if met1Reg_mod < 0:
        tau1RegTrue.SetCoordinates(tau1.pt(), iTree.eta1.at(0), iTree.phi1.at(0), tau1.mass())
    else:
        tau1RegTrue.SetCoordinates(met1Reg_mod, iTree.eta1.at(0), iTree.phi1.at(0), 0)
        tau1RegTrue = tau1 + tau1RegTrue

    if met2Reg_mod < 0:
        tau2RegTrue.SetCoordinates(tau2.pt(), iTree.eta2.at(0), iTree.phi2.at(0), tau2.mass())
    else:
        tau2RegTrue.SetCoordinates(met2Reg_mod, iTree.eta2.at(0), iTree.phi2.at(0), 0.)
        tau2RegTrue = tau2 + tau2RegTrue

#     tau1RegTrue.SetCoordinates(tau1.pt()+met1Reg_mod, iTree.eta1.at(0), iTree.phi1.at(0), tau1.mass())
#     tau2RegTrue.SetCoordinates(tau2.pt()+met2Reg_mod, iTree.eta2.at(0), iTree.phi2.at(0), tau2.mass())

    mTauPairWithMetReg[0] = (tau1RegTrue+tau2RegTrue).mass()
    tree.Fill()
print ''
oFile.cd()
tree.Write()
cutFlow.Write()
nSaved1 = tree.GetEntries()
oFile.Close()



print 'looped through %i events' %total
print 'saved %i events at: %s_new.root' %(nSaved1,iFileName[0:iFileName.rfind('.root')])