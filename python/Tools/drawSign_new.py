#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import math
import optparse
lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))

dR_tauEleMu_max = 0.2
dR_b_max = 0.5

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--i", dest="inputFile", default = False, help="")
    parser.add_option("--t", dest="title", default = False, help="")
    parser.add_option("--o", dest="option", default = False, help="")
    options, args = parser.parse_args()
    return options


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

def genMatchingFound(dR1_tau, dR2_tau, dR1_b, dR2_b, dR1_ele, dR2_ele, dR1_mu, dR2_mu, option):
    if option == 'all':
        return True
    elif option == '2genTau0genB':
        if dR1_tau<dR_tauEleMu_max and dR2_tau<dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max:
            return True
        else:
            return False
    elif option == '1genTau1genB':
        if dR1_tau<dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b<dR_b_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau<dR_tauEleMu_max and dR1_b<dR_b_max and dR2_b>dR_b_max:
            return True
        else:
            return False
    elif option == '1genTau0genB':
        if dR1_tau<dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau<dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max:
            return True
        else:
            return False
    elif option == '1genTau0genB1genEle0genMu':
        if dR1_tau<dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR2_ele<dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        elif  dR1_tau>dR_tauEleMu_max and dR2_tau<dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele<dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '1genTau0genB0genEle1genMu':
        if dR1_tau<dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR2_ele>dR_tauEleMu_max and dR2_mu<dR_tauEleMu_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau<dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele>dR_tauEleMu_max and dR1_mu<dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '1genTau0genB1genEleMu':
        if dR1_tau<dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR2_ele<dR_tauEleMu_max and dR2_mu<dR_tauEleMu_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau<dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele<dR_tauEleMu_max and dR1_mu<dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '1genTau0genB0genEle0genMu':
        if dR1_tau<dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR2_ele>dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau<dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele>dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '0genTau1genB':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b<dR_b_max and dR2_b>dR_b_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b<dR_b_max:
            return True
        else:
            return False
    elif option == '0genTau1genB1genEle0genMu':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b<dR_b_max and dR2_b>dR_b_max and dR2_ele<dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b<dR_b_max and dR1_ele<dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '0genTau1genB0genEle1genMu':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b<dR_b_max and dR2_b>dR_b_max and dR2_ele>dR_tauEleMu_max and dR2_mu<dR_tauEleMu_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b<dR_b_max and dR1_ele>dR_tauEleMu_max and dR1_mu<dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '0genTau1genB1genEleMu':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b<dR_b_max and dR2_b>dR_b_max and dR2_ele<dR_tauEleMu_max and dR2_mu<dR_tauEleMu_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b<dR_b_max and dR1_ele<dR_tauEleMu_max and dR1_mu<dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '0genTau1genB0genEle0genMu':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b<dR_b_max and dR2_b>dR_b_max and dR2_ele>dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b<dR_b_max and dR1_ele>dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '0genTau2genB':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b<dR_b_max and dR2_b<dR_b_max:
            return True
        else:
            return False
    elif option == '0genTau0genB':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max:
            return True
        else:
            return False
    elif option == '0genTau0genB1genEle1genMu':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele<dR_tauEleMu_max and dR2_ele>dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max and dR2_mu<dR_tauEleMu_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele>dR_tauEleMu_max and dR2_ele<dR_tauEleMu_max and dR1_mu<dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '0genTau0genB2genEle0genMu':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele<dR_tauEleMu_max and dR2_ele<dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '0genTau0genB0genEle2genMu':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele>dR_tauEleMu_max and dR2_ele>dR_tauEleMu_max and dR1_mu<dR_tauEleMu_max and dR2_mu<dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '0genTau0genB1genEle0genMu':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele<dR_tauEleMu_max and dR2_ele>dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele>dR_tauEleMu_max and dR2_ele<dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '0genTau0genB0genEle1genMu':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele>dR_tauEleMu_max and dR2_ele>dR_tauEleMu_max and dR1_mu<dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele>dR_tauEleMu_max and dR2_ele>dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max and dR2_mu<dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '0genTau0genB1genEleMu':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele<dR_tauEleMu_max and dR1_mu<dR_tauEleMu_max:
            return True
        elif dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR2_ele<dR_tauEleMu_max and dR2_mu<dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '0genTau0genB0genEle0genMu':
        if dR1_tau>dR_tauEleMu_max and dR2_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR2_b>dR_b_max and dR1_ele>dR_tauEleMu_max and dR2_ele>dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == 'bothGenBTauMatch':
        if (dR1_tau<dR_tauEleMu_max and dR1_b<dR_b_max) or (dR2_b<dR_b_max and dR2_tau<dR_tauEleMu_max):
            return True
        else:
            return False
    elif option == '1genTauB1genTau0genB':
        if dR1_tau<dR_tauEleMu_max and dR1_b<dR_b_max and dR2_tau<dR_tauEleMu_max and dR2_b>dR_b_max:
            return True
        elif dR2_tau<dR_tauEleMu_max and dR2_b<dR_b_max and dR1_tau<dR_tauEleMu_max and dR1_b>dR_b_max:
            return True
        else:
            return False
    elif option == '1genTauB0genTau1genB':
        if dR1_tau<dR_tauEleMu_max and dR1_b<dR_b_max and dR2_tau>dR_tauEleMu_max and dR2_b<dR_b_max:
            return True
        elif dR2_tau<dR_tauEleMu_max and dR2_b<dR_b_max and dR1_tau>dR_tauEleMu_max and dR1_b<dR_b_max:
            return True
        else:
            return False
    elif option == '2genTauB':
        if dR1_tau<dR_tauEleMu_max and dR1_b<dR_b_max and dR2_tau<dR_tauEleMu_max and dR2_b<dR_b_max:
            return True
        else:
            return False
    elif option == '1genTauB0genTau0genB1genEle0genMu':
        if dR1_tau<dR_tauEleMu_max and dR1_b<dR_b_max and dR2_tau>dR_tauEleMu_max and dR2_b>dR_b_max and dR2_ele<dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        elif dR2_tau<dR_tauEleMu_max and dR2_b<dR_b_max and dR1_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR1_ele<dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '1genTauB0genTau0genB0genEle1genMu':
        if dR1_tau<dR_tauEleMu_max and dR1_b<dR_b_max and dR2_tau>dR_tauEleMu_max and dR2_b>dR_b_max and dR2_ele>dR_tauEleMu_max and dR2_mu<dR_tauEleMu_max:
            return True
        elif dR2_tau<dR_tauEleMu_max and dR2_b<dR_b_max and dR1_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR1_ele>dR_tauEleMu_max and dR1_mu<dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '1genTauB0genTau0genB1genEleMu':
        if dR1_tau<dR_tauEleMu_max and dR1_b<dR_b_max and dR2_tau>dR_tauEleMu_max and dR2_b>dR_b_max and dR2_ele<dR_tauEleMu_max and dR2_mu<dR_tauEleMu_max:
            return True
        elif dR2_tau<dR_tauEleMu_max and dR2_b<dR_b_max and dR1_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR1_ele<dR_tauEleMu_max and dR1_mu<dR_tauEleMu_max:
            return True
        else:
            return False
    elif option == '1genTauB0genTau0genB0genEle0genMu':
        if dR1_tau<dR_tauEleMu_max and dR1_b<dR_b_max and dR2_tau>dR_tauEleMu_max and dR2_b>dR_b_max and dR2_ele>dR_tauEleMu_max and dR2_mu>dR_tauEleMu_max:
            return True
        elif dR2_tau<dR_tauEleMu_max and dR2_b<dR_b_max and dR1_tau>dR_tauEleMu_max and dR1_b>dR_b_max and dR1_ele>dR_tauEleMu_max and dR1_mu>dR_tauEleMu_max:
            return True
        else:
            return False


options = opts()

r.gStyle.SetOptStat(0)

histRange1 = [100, 0.0, 5.0]
histRange2 = [100, 0.0, 5.0]
histRange3 = [50, 0, 250]

tmpHist1 = r.TH1F('tmpHist1', '', histRange1[0], histRange1[1], histRange1[2])
tmpHist2 = r.TH1F('tmpHist2', '', histRange2[0], histRange2[1], histRange2[2])
tmpHist3 = r.TH1F('tmpHist3', '', histRange1[0], histRange1[1], histRange1[2])
tmpHist4 = r.TH1F('tmpHist4', '', histRange2[0], histRange2[1], histRange2[2])
tmpHist5 = r.TH1F('tmpHist5', '', histRange1[0], histRange1[1], histRange1[2])
tmpHist6 = r.TH1F('tmpHist6', '', histRange2[0], histRange2[1], histRange2[2])
tmpHist7 = r.TH1F('tmpHist7', '', histRange3[0], histRange3[1], histRange3[2])
tmpHist8 = r.TH1F('tmpHist8', '', histRange3[0], histRange3[1], histRange3[2])
tmpHist9 = r.TH1F('tmpHist9', '', histRange3[0], histRange3[1], histRange3[2])
tmpHist10 = r.TH1F('tmpHist10', '', histRange3[0], histRange3[1], histRange3[2])

tmpHist_total1 = r.TH1F('total1', '', histRange1[0], histRange1[1], histRange1[2])
tmpHist_total2 = r.TH1F('total2', '', histRange2[0], histRange2[1], histRange2[2])


title = options.title

psfile = 'chargeSignVS'
genPar = 'mu'
postfix = options.option
max1 = 1.
max2 = 1.

iFile = r.TFile(options.inputFile)
iTree = iFile.Get('eventTree')

legendPosition = (0.35, 0.75, 0.9, 0.9)
#draw from the highest histogram
legendList = []

total = iTree.GetEntries()
ssEvents = 0
osEvents = 0

for i in range(0, total):
    tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample')
    iTree.GetEntry(i)

    matchTuple1 = [iTree.pt1.at(0), iTree.eta1.at(0), iTree.phi1.at(0)]
    matchTuple2 = [iTree.pt2.at(0), iTree.eta2.at(0), iTree.phi2.at(0)]

    if genPar == 'B':
        genTuple = [iTree.genBPt, iTree.genBEta, iTree.genBPhi]
    elif genPar == 'Tau':
        genTuple = [iTree.genTauPt, iTree.genTauEta, iTree.genTauPhi]
    elif genPar == 'e':
        genTuple = [iTree.genElePt, iTree.genEleEta, iTree.genElePhi]
    elif genPar == 'mu':
        genTuple = [iTree.genMuPt, iTree.genMuEta, iTree.genMuPhi]
    elif genPar == 'BTau':
        dR1_tau = findDR(iTree.genTauPt,iTree.genTauEta,iTree.genTauPhi,matchTuple1[0],matchTuple1[1],matchTuple1[2])
        dR2_tau = findDR(iTree.genTauPt,iTree.genTauEta,iTree.genTauPhi,matchTuple2[0],matchTuple2[1],matchTuple2[2])
        dR1_b = findDR(iTree.genBPt,iTree.genBEta,iTree.genBPhi,matchTuple1[0],matchTuple1[1],matchTuple1[2])
        dR2_b = findDR(iTree.genBPt,iTree.genBEta,iTree.genBPhi,matchTuple2[0],matchTuple2[1],matchTuple2[2])
        dR1_ele = findDR(iTree.genElePt,iTree.genEleEta,iTree.genElePhi,matchTuple1[0],matchTuple1[1],matchTuple1[2])
        dR2_ele = findDR(iTree.genElePt,iTree.genEleEta,iTree.genElePhi,matchTuple2[0],matchTuple2[1],matchTuple2[2])
        dR1_mu = findDR(iTree.genMuPt,iTree.genMuEta,iTree.genMuPhi,matchTuple1[0],matchTuple1[1],matchTuple1[2])
        dR2_mu = findDR(iTree.genMuPt,iTree.genMuEta,iTree.genMuPhi,matchTuple2[0],matchTuple2[1],matchTuple2[2])
        if not genMatchingFound(dR1_tau, dR2_tau, dR1_b, dR2_b, dR1_ele, dR2_ele, dR1_mu, dR2_mu, postfix):
            continue
        genTuple = [iTree.genTauPt, iTree.genTauEta, iTree.genTauPhi]

    dR1 = findDR(genTuple[0],genTuple[1],genTuple[2],matchTuple1[0],matchTuple1[1],matchTuple1[2])
    dR2 = findDR(genTuple[0],genTuple[1],genTuple[2],matchTuple2[0],matchTuple2[1],matchTuple2[2])

    tmpHist_total1.Fill(dR1)
    tmpHist_total2.Fill(dR2)
    
    #for same signs
    if iTree.charge1.at(0) == iTree.charge2.at(0):
        tmpHist1.Fill(dR1)
        tmpHist2.Fill(dR2)
        ssEvents+=1
        tmpHist7.Fill(matchTuple1[0])
        tmpHist8.Fill(matchTuple2[0])

    elif iTree.charge1.at(0) == - iTree.charge2.at(0):
        tmpHist3.Fill(dR1)
        tmpHist4.Fill(dR2)
        osEvents+=1
        tmpHist9.Fill(matchTuple1[0])
        tmpHist10.Fill(matchTuple2[0])

print''

pEff1 = r.TEfficiency(tmpHist1, tmpHist_total1)
pEff2 = r.TEfficiency(tmpHist2, tmpHist_total2)

histList1 = [(tmpHist1, 'Same Sign Events %i / %i' %(ssEvents, total)),
            (tmpHist3, 'Opposite Sign Events %i / %i' %(osEvents, total))]
histList2 = [(tmpHist2, 'Same Sign Events %i / %i' %(ssEvents, total)),
            (tmpHist4, 'Opposite Sign Events %i / %i' %(osEvents, total))]

tmpHist5.SetTitle('%s same sign rate; dR; SS/(SS+OS)' %(title))
tmpHist6.SetTitle('%s same sign rate; dR; SS/(SS+OS)' %(title))

c = r.TCanvas("c","Test", 800, 600)
ps = r.TPDF('%sGen%sdR_%s_%s.pdf' %(psfile, genPar, title, postfix),112)
print "saving file at: %sGen%sdR_%s_%s.pdf" %(psfile, genPar, title, postfix)

c.Divide(2,2)
c.cd(1)
r.gPad.SetLogy()
tmpHist3.SetTitle('%s tau1 dR from closest gen %s (%s); dR; events' %(title, genPar, postfix))
tmpHist3.Draw()
tmpHist1.SetLineColor(r.kRed)
tmpHist1.Draw("same")
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=histList1)
l1.Draw("same")
c.Update()
c.cd(2)
r.gPad.SetLogy()
tmpHist4.SetTitle('%s tau2 dR from closest gen %s (%s); dR; events' %(title, genPar, postfix))
tmpHist4.Draw("")
tmpHist2.SetLineColor(r.kRed)
tmpHist2.Draw("same")
l2 = tool.setMyLegend(lPosition=legendPosition, lHistList=histList2)
l2.Draw("same")

c.Update()
c.cd(3)
tmpHist5.SetMaximum(max1)
tmpHist5.Draw()
pEff1.Draw("P same")
c.Update()
c.cd(4)
tmpHist6.SetMaximum(max2)
tmpHist6.Draw()
pEff2.Draw("P same")
c.Update()
ps.Close()
