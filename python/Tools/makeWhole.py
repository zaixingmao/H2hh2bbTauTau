#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import math
import optparse
import os
from array import array

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--massPoint", dest="massPoint", default = '260', help="")
    options, args = parser.parse_args()
    return options

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))

dR_tauEleMu_max = 0.2
dR_b_max = 0.5
lumi = 19.0

def findDR(genPt, genEta, genPhi, pt, eta, phi):

    tmpGen = lvClass()
    tmpParticle = lvClass()
    tmpParticle.SetCoordinates(pt, eta, phi, 0)
    dR = 999999.0
    for i in range(len(genPt)):
        tmpGen.SetCoordinates(genPt.at(i), genEta.at(i), genPhi.at(i), 0)
        tmpDR = r.Math.VectorUtil.DeltaR(tmpParticle, tmpGen)
        if tmpDR < dR:
            dR = tmpDR
    return dR


def findGenMatch(dR1_tau, dR2_tau, dR1_b, dR2_b, dR1_ele, dR2_ele, dR1_mu, dR2_mu, option = ''):
    #for leg1
    leg1 = sorted([('t',dR1_tau), ('b',dR1_b), ('e',dR1_ele), ('m',dR1_mu)], key=itemgetter(1))    
    #for leg2
    leg2 = sorted([('t',dR2_tau), ('b',dR2_b), ('e',dR2_ele), ('m',dR2_mu)], key=itemgetter(1))
    leg1Match = leg1[0][0]
    leg2Match = leg2[0][0]

    if leg1[0][1] > dR_tauEleMu_max:
        leg1Match = 'x'
    if leg2[0][1] > dR_tauEleMu_max:
        leg2Match = 'x'

    if 'e(tau)' in option:
        if leg1Match == 'e' and leg1[1][0] == 't' and leg1[1][1] < dR_tauEleMu_max:
            leg1Match = 'e(t)'
        if leg2Match == 'e' and leg2[1][0] == 't' and leg2[1][1] < dR_tauEleMu_max:
            leg2Match = 'e(t)'
    
    if 'e(b)' in option:
        if leg1Match == 'e' and leg1[1][0] == 'b' and leg1[1][1] < dR_b_max:
            leg1Match = 'e(b)'
        if leg2Match == 'e' and leg2[1][0] == 'b' and leg2[1][1] < dR_b_max:
            leg2Match = 'e(b)'
        if 'e(tau)' in option:
            if leg1Match == 'e' and leg1[1][0] == 't' and leg1[1][1] < dR_tauEleMu_max:
                leg1Match = 'e(t)'
            if leg2Match == 'e' and leg2[1][0] == 't' and leg2[1][1] < dR_tauEleMu_max:
                leg2Match = 'e(t)'
    
    if 'tau(b)' in option:
        if leg1Match == 'tau':
            if leg1[1][0] == 'b' and leg1[1][1] < dR_b_max:
                leg1Match = 't(b)'
        if leg2Match == 'tau':
            if leg2[1][0] == 'b' and leg2[1][1] < dR_b_max:
                leg2Match = 't(b)'

    stringList = [leg1Match, leg2Match]
    stringList.sort()
    return '%s%s' %(stringList[0], stringList[1])

def passCut(tree, option):
    if 'bTag' in option and (tree.CSVJ1 < 0.68 or tree.CSVJ2 < 0.24):
        return 0
#     if  tree.mJJ<90  or tree.mJJ>140:
#         return 0

    passIso = 0
    passSign = 0
    if 'tight' in option and (tree.iso1.at(0) < 1.5 and tree.iso2.at(0) < 1.5):
            passIso = 1
    if 'relaxed' in option and (tree.iso1.at(0) > 3 and tree.iso2.at(0) > 3):
            passIso = 1
    if 'SS' in option and (tree.charge1.at(0) == tree.charge2.at(0)):
            passSign = 1
    if 'OS' in option and (tree.charge1.at(0) == -tree.charge2.at(0)):
            passSign = 1
    return passIso*passSign

def findMatch(iTree, isData):
    if isData:
        return 'ff'

    matchTuple1 = [iTree.pt1.at(0), iTree.eta1.at(0), iTree.phi1.at(0)]
    matchTuple2 = [iTree.pt2.at(0), iTree.eta2.at(0), iTree.phi2.at(0)]

    dR1_tau = findDR(iTree.genTauPt,iTree.genTauEta,iTree.genTauPhi,matchTuple1[0],matchTuple1[1],matchTuple1[2])
    dR2_tau = findDR(iTree.genTauPt,iTree.genTauEta,iTree.genTauPhi,matchTuple2[0],matchTuple2[1],matchTuple2[2])
    dR1_b = findDR(iTree.genBPt,iTree.genBEta,iTree.genBPhi,matchTuple1[0],matchTuple1[1],matchTuple1[2])
    dR2_b = findDR(iTree.genBPt,iTree.genBEta,iTree.genBPhi,matchTuple2[0],matchTuple2[1],matchTuple2[2])
    dR1_ele = findDR(iTree.genElePt,iTree.genEleEta,iTree.genElePhi,matchTuple1[0],matchTuple1[1],matchTuple1[2])
    dR2_ele = findDR(iTree.genElePt,iTree.genEleEta,iTree.genElePhi,matchTuple2[0],matchTuple2[1],matchTuple2[2])
    dR1_mu = findDR(iTree.genMuPt,iTree.genMuEta,iTree.genMuPhi,matchTuple1[0],matchTuple1[1],matchTuple1[2])
    dR2_mu = findDR(iTree.genMuPt,iTree.genMuEta,iTree.genMuPhi,matchTuple2[0],matchTuple2[1],matchTuple2[2])

    genMatch = findGenMatch(dR1_tau, dR2_tau, dR1_b, dR2_b, dR1_ele, dR2_ele, dR1_mu, dR2_mu)

    return genMatch

op = opts()
massPoint = op.massPoint

preFix = '/scratch/zmao/relaxed_regression3/%s/ClassApp_both_TMVARegApp_' %massPoint

fileList = [('H2hh260', preFix + 'H2hh260_all.root', 'OStightbTag', 14.76),
            ("H2hh300", preFix + "H2hh300_all.root", 'OStightbTag', 15.9), 
            ('H2hh350', preFix + 'H2hh350_all.root', 'OStightbTag', 8.57),
            ('WZJetsTo2L2Q', preFix + 'WZJetsTo2L2Q_eff_all.root', 'OStightbTag', 2207),
            ('ZZ', preFix + 'ZZ_eff_all.root', 'OStightbTag', 2500),
            ("tt_full", preFix + "tt_eff_all.root", 'OStightbTag', 26197.5), 
            ("tt_semi", preFix + "tt_semi_eff_all.root", 'OStightbTag', 109281), 
            ("tt_MSDecays", preFix + "TTJets_MSDecays_all.root", 'OStightbTag', 131300), 
            ("DY1JetsToLL", preFix + "DY1JetsToLL_eff2_all.root", 'OStightbTag', 561000), 
            ('DY2JetsToLL', preFix + 'DY2JetsToLL_eff2_all.root', 'OStightbTag', 181000),
            ('DY3JetsToLL', preFix + 'DY3JetsToLL_eff2_all.root', 'OStightbTag', 51100),
            ('W1JetsToLNu', preFix + 'W1JetsToLNu_eff2_all.root', 'OStightbTag', 5400000),
            ('W2JetsToLNu', preFix + 'W2JetsToLNu_eff2_all.root', 'OStightbTag', 1750000),
            ('W3JetsToLNu', preFix + 'W3JetsToLNu_eff2_all.root', 'OStightbTag', 519000),
            ('dataOSRelax', preFix + 'dataTotal_all.root', 'OSrelaxedbTag', 0.062),#0.05),
            ]

oFileName = 'combined_%s.root' %massPoint
oFile = r.TFile(oFileName, 'RECREATE')
oTree = r.TTree('eventTree', '')

BDT = array('f', [0.])
mJJReg = array('f', [0.])
mJJ = array('f', [0.])
svMass = array('f', [0.])
BDT_QCD = array('f', [0.])
BDT_EWK = array('f', [0.])

triggerEff = array('f', [0.])
sampleName = bytearray(20)
genMatchName = bytearray(3)
initEvents = r.TH1F('initEvents', '', len(fileList), 0, len(fileList))
xs = r.TH1F('xs', '', len(fileList), 0, len(fileList))
finalEventsWithXS = r.TH1F('finalEventsWithXS', '', len(fileList), 0, len(fileList))

svMassRange = [20, 0, 400]
mJJRegRange = [15, 50, 200]
BDTRange = [20, -1.0, 1.0]


scaleSVMass = r.TH1F("scaleSVMass", "", svMassRange[0], svMassRange[1], svMassRange[2])
scaleSVMassMC = r.TH1F("MC_Data_svMass", "", svMassRange[0], svMassRange[1], svMassRange[2])
scaleMJJReg = r.TH1F("scaleMJJReg", "", mJJRegRange[0], mJJRegRange[1], mJJRegRange[2])
scaleMJJRegMC = r.TH1F("MC_Data_mJJReg", "", mJJRegRange[0], mJJRegRange[1], mJJRegRange[2])
scaleBDT = r.TH1F("scaleBDT", "", BDTRange[0], BDTRange[1], BDTRange[2])
scaleBDTMC = r.TH1F("MC_Data_BDT", "", BDTRange[0], BDTRange[1], BDTRange[2])


oTree.Branch("BDT", BDT, "BDT/F")
oTree.Branch("mJJReg", mJJReg, "mJJReg/F")
oTree.Branch("mJJ", mJJ, "mJJ/F")

oTree.Branch("svMass", svMass, "svMass/F")

# oTree.Branch("BDT_QCD", BDT_QCD, "BDT_QCD/F")
# oTree.Branch("BDT_EWK", BDT_EWK, "BDT_EWK/F")

oTree.Branch("triggerEff", triggerEff, "triggerEff/F")
oTree.Branch("sampleName", sampleName, "sampleName[21]/C")
oTree.Branch("genMatchName", genMatchName, "genMatchName[21]/C")


for name, ifile, option, xsValue in fileList:
    iFile = r.TFile(ifile)
    iTree = iFile.Get('eventTree')
    total = iTree.GetEntries()
    tmpHist = iFile.Get('preselection')
    initEvents.Fill(name, tmpHist.GetBinContent(1))
    isData = False
    if 'data' in name:
        isData = True
    eventsSaved = 0.

    scale = xsValue/tmpHist.GetBinContent(1)*lumi

    if isData:
        xsValue = xsValue*tmpHist.GetBinContent(1)/lumi

    for i in range(0, total):
        tool.printProcessStatus(iCurrent=i+1, total=total, processName = 'Looping sample [%s]' %name)
        iTree.GetEntry(i)
        #Fill Histograms
        if passCut(iTree, 'OSrelaxedbTag') and (not ("H2hh" in name)):
            if isData:
                scaleSVMass.Fill(iTree.svMass.at(0), iTree.triggerEff)
                scaleMJJReg.Fill(iTree.mJJReg, iTree.triggerEff)
                scaleBDT.Fill(iTree.BDT_both, iTree.triggerEff)
            else:
                scaleSVMassMC.Fill(iTree.svMass.at(0), iTree.triggerEff*scale)
                scaleMJJRegMC.Fill(iTree.mJJReg, iTree.triggerEff*scale)
                scaleBDTMC.Fill(iTree.BDT_both, iTree.triggerEff*scale)

        if not passCut(iTree, option):
            continue
        BDT[0] = iTree.BDT_both
        mJJReg[0] = iTree.mJJReg
        mJJ[0] = iTree.mJJ
        svMass[0] = iTree.svMass.at(0)

#         BDT_QCD[0] = iTree.BDT_QCD
#         BDT_EWK[0] = iTree.BDT_EWK
        triggerEff[0] = iTree.triggerEff
        sampleName[:21] = name
        genMatchName[:3] = findMatch(iTree, isData)
        oTree.Fill()
        eventsSaved += triggerEff[0]

    xs.Fill(name, xsValue)
    finalEventsWithXS.Fill(name, eventsSaved*xsValue/tmpHist.GetBinContent(1)*lumi)
    print ' --- Events Saved: %.2f' %eventsSaved

scaleSVMass.Sumw2()
scaleSVMassMC.Sumw2()
scaleSVMassMC.Divide(scaleSVMass)

scaleMJJReg.Sumw2()
scaleMJJRegMC.Sumw2()
scaleMJJRegMC.Divide(scaleMJJReg)

scaleBDT.Sumw2()
scaleBDTMC.Sumw2()
scaleBDTMC.Divide(scaleBDT)


oFile.cd()
scaleSVMassMC.Write()
scaleMJJRegMC.Write()
scaleBDTMC.Write()
initEvents.Write()
xs.Write()
finalEventsWithXS.Write()
oTree.Write()
oFile.Close()

print 'Combined event saved at: %s' %oFileName



