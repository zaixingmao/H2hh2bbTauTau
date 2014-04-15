#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import math
import optparse
import os

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))

dR_tauEleMu_max = 0.2
dR_b_max = 0.5

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--i", dest="inputFile", default = False, help="")
    parser.add_option("--o", dest="option", default = '', help="")
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


def findGenMatch(dR1_tau, dR2_tau, dR1_b, dR2_b, dR1_ele, dR2_ele, dR1_mu, dR2_mu, option = ''):
    #for leg1
    leg1 = sorted([('tau',dR1_tau), ('b',dR1_b), ('e',dR1_ele), ('mu',dR1_mu)], key=itemgetter(1))    
    #for leg2
    leg2 = sorted([('tau',dR2_tau), ('b',dR2_b), ('e',dR2_ele), ('mu',dR2_mu)], key=itemgetter(1))
    leg1Match = leg1[0][0]
    leg2Match = leg2[0][0]

    if leg1[0][1] > dR_tauEleMu_max:
        leg1Match = 'None'
    if leg2[0][1] > dR_tauEleMu_max:
        leg2Match = 'None'

    if 'e(tau)' in option:
        if leg1Match == 'e' and leg1[1][0] == 'tau' and leg1[1][1] < dR_tauEleMu_max:
            leg1Match = 'e(tau)'
        if leg2Match == 'e' and leg2[1][0] == 'tau' and leg2[1][1] < dR_tauEleMu_max:
            leg2Match = 'e(tau)'
    
    if 'e(b)' in option:
        if leg1Match == 'e' and leg1[1][0] == 'b' and leg1[1][1] < dR_b_max:
            leg1Match = 'e(b)'
        if leg2Match == 'e' and leg2[1][0] == 'b' and leg2[1][1] < dR_b_max:
            leg2Match = 'e(b)'
        if 'e(tau)' in option:
            if leg1Match == 'e' and leg1[1][0] == 'tau' and leg1[1][1] < dR_tauEleMu_max:
                leg1Match = 'e(tau)'
            if leg2Match == 'e' and leg2[1][0] == 'tau' and leg2[1][1] < dR_tauEleMu_max:
                leg2Match = 'e(tau)'
    
    if 'tau(b)' in option:
        if leg1Match == 'tau':
            if leg1[1][0] == 'b' and leg1[1][1] < dR_b_max:
                leg1Match = 'tau(b)'
        if leg2Match == 'tau':
            if leg2[1][0] == 'b' and leg2[1][1] < dR_b_max:
                leg2Match = 'tau(b)'

    return '%s%s' %(leg1Match, leg2Match)

options = opts()
option = options.option

def passCut(tree, iso):
    if iso == 'tight':
        if tree.iso2.at(0) < 1.5:
            return True
        else:
            return False
    elif iso == 'relaxed':
        if 1.5 < tree.iso2.at(0) < 4.0:
            return True
        else:
            return False
    else:
        print 'Unsupported iso option !!! Please use \'tight\' or \'relaxed\''
        return False

def getCaseList(iTree, iso):

    total = iTree.GetEntries()
    ssEvents = 0
    osEvents = 0

    tautau_ss = 0
    taub_ss = 0
    taue_ss = 0
    taue_b_ss = 0
    taue_tau_ss = 0
    taumu_ss = 0
    tauNone_ss = 0
    tau_btau_b_ss = 0
    tautau_b_ss = 0
    tau_bb_ss = 0
    tau_be_ss = 0
    tau_be_b_ss = 0
    tau_be_tau_ss = 0
    tau_bmu_ss = 0
    tau_bNone_ss = 0
    bb_ss = 0
    be_ss = 0
    be_b_ss = 0
    be_tau_ss=0
    bmu_ss = 0
    bNone_ss = 0
    ee_ss = 0
    ee_tau_ss = 0
    e_taue_tau_ss = 0
    e_taue_b_ss = 0
    ee_b_ss = 0
    e_be_b_ss = 0
    emu_ss = 0
    e_taumu_ss = 0
    e_bmu_ss = 0
    eNone_ss = 0
    e_tauNone_ss = 0
    e_bNone_ss = 0
    mumu_ss = 0
    muNone_ss = 0
    NoneNone_ss = 0

    tautau_os = 0
    taub_os = 0
    taue_os = 0
    taue_tau_os = 0
    taue_b_os = 0
    taumu_os = 0
    tauNone_os = 0
    tau_btau_b_os = 0
    tautau_b_os = 0
    tau_bb_os = 0
    tau_be_os = 0
    tau_be_b_os = 0
    tau_be_tau_os = 0
    tau_bmu_os = 0
    tau_bNone_os = 0
    bb_os = 0
    be_os = 0
    be_tau_os=0
    be_b_os=0
    bmu_os = 0
    bNone_os = 0
    ee_os = 0
    ee_tau_os = 0
    e_taue_tau_os = 0
    e_taue_b_os = 0
    ee_b_os = 0
    e_be_b_os = 0
    emu_os = 0
    e_taumu_os = 0
    e_bmu_os = 0
    eNone_os = 0
    e_tauNone_os = 0
    e_bNone_os = 0
    mumu_os = 0
    muNone_os = 0
    NoneNone_os = 0

    for i in range(0, total):
        tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample')
        iTree.GetEntry(i)

        if not passCut(iTree, iso):
            continue

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

        genMatch = findGenMatch(dR1_tau, dR2_tau, dR1_b, dR2_b, dR1_ele, dR2_ele, dR1_mu, dR2_mu, option)

        #for same signs
        if iTree.charge1.at(0) == iTree.charge2.at(0):
            ssEvents+=1
            if genMatch == 'tautau':
                tautau_ss+=1
            elif genMatch == 'taub' or genMatch == 'btau':
                taub_ss+=1
            elif genMatch == 'taue' or genMatch == 'etau':
                taue_ss+=1
            elif genMatch == 'taue(tau)' or genMatch == 'e(tau)tau':
                taue_tau_ss+=1
            elif genMatch == 'taue(b)' or genMatch == 'e(b)tau':
                taue_b_ss+=1
            elif genMatch == 'taumu' or genMatch == 'mutau':
                taumu_ss+=1
            elif genMatch == 'tauNone' or genMatch == 'Nonetau':
                tauNone_ss+=1
                
            elif genMatch == 'tau(b)tau(b)':
                tau_btau_b_ss+=1
            elif genMatch == 'tau(b)tau' or genMatch == 'tautau(b)':
                tautau_b_ss+=1
            elif genMatch == 'tau(b)b' or genMatch == 'btau(b)':
                tau_bb_ss+=1
            elif genMatch == 'tau(b)e' or genMatch == 'etau(b)':
                tau_be_ss+=1
            elif genMatch == 'tau(b)e(tau)' or genMatch == 'e(tau)tau(b)':
                tau_be_tau_ss+=1
            elif genMatch == 'tau(b)e(b)' or genMatch == 'e(b)tau(b)':
                tau_be_b_ss+=1
            elif genMatch == 'tau(b)mu' or genMatch == 'mutau(b)':
                tau_bmu_ss+=1
            elif genMatch == 'tau(b)None' or genMatch == 'Nonetau(b)':
                tau_bNone_ss+=1
                
            elif genMatch == 'bb':
                bb_ss+=1
            elif genMatch == 'be' or genMatch == 'eb':
                be_ss+=1
            elif genMatch == 'be(tau)' or genMatch == 'e(tau)b':
                be_tau_ss+=1
            elif genMatch == 'be(b)' or genMatch == 'e(b)b':
                be_b_ss+=1
            elif genMatch == 'bmu' or genMatch == 'mub':
                bmu_ss+=1
            elif genMatch == 'bNone' or genMatch == 'Noneb':
                bNone_ss+=1
                
            elif genMatch == 'ee' or genMatch == 'ee':
                ee_ss+=1
            elif genMatch == 'ee(tau)' or genMatch == 'e(tau)e':
                ee_tau_ss+=1
            elif genMatch == 'e(tau)e(tau)':
                e_taue_tau_ss+=1
            elif genMatch == 'e(tau)e(b)' or genMatch == 'e(b)e(tau)':
                e_taue_b_ss+=1
            elif genMatch == 'ee(b)' or genMatch == 'e(b)e':
                ee_b_ss+=1
            elif genMatch == 'e(b)e(b)':
                e_be_b_ss+=1
            elif genMatch == 'emu' or genMatch == 'mue':
                emu_ss+=1
            elif genMatch == 'e(tau)mu' or genMatch == 'mue(tau)':
                e_taumu_ss+=1
            elif genMatch == 'e(b)mu' or genMatch == 'mue(b)':
                e_bmu_ss+=1
            elif genMatch == 'eNone' or genMatch == 'Nonee':
                eNone_ss+=1
            elif genMatch == 'e(tau)None' or genMatch == 'Nonee(tau)':
                e_tauNone_ss+=1
            elif genMatch == 'e(b)None' or genMatch == 'Nonee(b)':
                e_bNone_ss+=1
                
            elif genMatch == 'mumu':
                mumu_ss+=1
            elif genMatch == 'muNone' or genMatch == 'Nonemu':
                muNone_ss+=1
                
            elif genMatch == 'NoneNone':
                NoneNone_ss+=1
                
        #for opposite signs
        elif iTree.charge1.at(0) == - iTree.charge2.at(0):
            osEvents+=1
            if genMatch == 'tautau':
                tautau_os+=1
            elif genMatch == 'taub' or genMatch == 'btau':
                taub_os+=1
            elif genMatch == 'taue' or genMatch == 'etau':
                taue_os+=1
            elif genMatch == 'taue(tau)' or genMatch == 'e(tau)tau':
                taue_tau_os+=1
            elif genMatch == 'taue(b)' or genMatch == 'e(b)tau':
                taue_b_os+=1
            elif genMatch == 'taumu' or genMatch == 'mutau':
                taumu_os+=1
            elif genMatch == 'tauNone' or genMatch == 'Nonetau':
                tauNone_os+=1
                
            elif genMatch == 'tau(b)tau(b)':
                tau_btau_b_os+=1
            elif genMatch == 'tau(b)tau' or genMatch == 'tautau(b)':
                tautau_b_os+=1
            elif genMatch == 'tau(b)b' or genMatch == 'btau(b)':
                tau_bb_os+=1
            elif genMatch == 'tau(b)e' or genMatch == 'etau(b)':
                tau_be_os+=1
            elif genMatch == 'tau(b)e(tau)' or genMatch == 'e(tau)tau(b)':
                tau_be_tau_os+=1
            elif genMatch == 'tau(b)e(b)' or genMatch == 'e(b)tau(b)':
                tau_be_b_os+=1
            elif genMatch == 'tau(b)mu' or genMatch == 'mutau(b)':
                tau_bmu_os+=1
            elif genMatch == 'tau(b)None' or genMatch == 'Nonetau(b)':
                tau_bNone_os+=1
                
            elif genMatch == 'bb':
                bb_os+=1
            elif genMatch == 'be' or genMatch == 'eb':
                be_os+=1
            elif genMatch == 'be(tau)' or genMatch == 'e(tau)b':
                be_tau_os+=1
            elif genMatch == 'be(b)' or genMatch == 'e(b)b':
                be_b_os+=1
            elif genMatch == 'bmu' or genMatch == 'mub':
                bmu_os+=1
            elif genMatch == 'bNone' or genMatch == 'Noneb':
                bNone_os+=1
                
            elif genMatch == 'ee' or genMatch == 'ee':
                ee_os+=1
            elif genMatch == 'ee(tau)' or genMatch == 'e(tau)e':
                ee_tau_os+=1
            elif genMatch == 'e(tau)e(tau)':
                e_taue_tau_os+=1
            elif genMatch == 'e(tau)e(b)' or genMatch == 'e(b)e(tau)':
                e_taue_b_os+=1
            elif genMatch == 'ee(b)' or genMatch == 'e(b)e':
                ee_b_os+=1
            elif genMatch == 'e(b)e(b)':
                e_be_b_os+=1
            elif genMatch == 'emu' or genMatch == 'mue':
                emu_os+=1
            elif genMatch == 'e(tau)mu' or genMatch == 'mue(tau)':
                e_taumu_os+=1
            elif genMatch == 'e(b)mu' or genMatch == 'mue(b)':
                e_bmu_os+=1
            elif genMatch == 'eNone' or genMatch == 'Nonee':
                eNone_os+=1
            elif genMatch == 'e(tau)None' or genMatch == 'Nonee(tau)':
                e_tauNone_os+=1
            elif genMatch == 'e(b)None' or genMatch == 'Nonee(b)':
                e_bNone_os+=1
                
            elif genMatch == 'mumu':
                mumu_os+=1
            elif genMatch == 'muNone' or genMatch == 'Nonemu':
                muNone_os+=1
                
            elif genMatch == 'NoneNone':
                NoneNone_os+=1

    print''
    counterList = [ ('total', ssEvents, osEvents),
                    ('tau tau', tautau_ss, tautau_os),
                    ('tau b', taub_ss, taub_os),
                    ('tau e', taue_ss, taue_os),
                    ('tau mu', taumu_ss, taumu_os),
                    ('tau None', tauNone_ss, tauNone_os),
                    ('b b', bb_ss, bb_os),
                    ('b e', be_ss, be_os),
                    ('b mu', bmu_ss, bmu_os),
                    ('b None', bNone_ss, bNone_os),
                    ('e e', ee_ss, ee_os),
                    ('e mu', emu_ss, emu_os),
                    ('e None', eNone_ss, eNone_os),
                    ('mu mu', mumu_ss, mumu_os),
                    ('mu None', muNone_ss, muNone_os),
                    ('None None', NoneNone_ss, NoneNone_os)]
        
    tau_bList = [('tau(b) tau(b)', tau_btau_b_ss, tau_btau_b_os),
                 ('tau tau(b)', tautau_b_ss, tautau_b_os),
                 ('tau(b) b', tau_bb_ss, tau_bb_os),
                 ('tau(b) e', tau_be_ss, tau_be_os),
                 ('tau(b) e(tau)', tau_be_tau_ss, tau_be_tau_os),
                 ('tau(b) e(b)', tau_be_b_ss, tau_be_b_os),
                 ('tau(b) mu', tau_bmu_ss, tau_bmu_os),
                 ('tau(b) None', tau_bNone_ss, tau_bNone_os)]
        
    e_tauList = [('tau e(tau)', taue_tau_ss, taue_tau_os),
                 ('b e(tau)', be_tau_ss, be_tau_os),
                 ('e(tau) e', ee_tau_ss, ee_tau_os),
                 ('e(tau) e(tau)', e_taue_tau_ss, e_taue_tau_os),
                 ('e(tau) mu', e_taumu_ss, e_taumu_os),
                 ('e(tau) None', e_tauNone_ss, e_tauNone_os)
                 ]
        
    e_bList = [('tau e(b)', taue_b_ss, taue_b_os),
               ('b e(b)', be_b_ss, be_b_os),
               ('e(b) e', ee_b_ss, ee_b_os),
               ('e(b) e(b)', e_be_b_ss, e_be_b_os),
               ('e(b) mu', e_bmu_ss, e_bmu_os),
               ('e(b) None', e_bNone_ss, e_bNone_os),
               ]
    e_taue_bList = [('e(tau) e(b)', e_taue_b_ss, e_taue_b_os)]
        
    if 'tau(b)' in option:
        for i in range(len(tau_bList)):
            counterList.append(tau_bList[i])
    if 'e(b)' in option:
        for i in range(len(e_bList)):
            counterList.append(e_bList[i])
        if 'e(tau)' in option:
            counterList.append(e_taue_bList[0])
    if 'e(tau)' in option:
        for i in range(len(e_tauList)):
            counterList.append(e_tauList[i])
    return counterList

iFile = r.TFile(options.inputFile)
iTree = iFile.Get('eventTree')

counterList = getCaseList(iTree=iTree, iso='tight')
counterList2 = getCaseList(iTree=iTree, iso='relaxed')

sampleName = options.inputFile[0:options.inputFile.rfind('_')]
if len(sampleName) < 8:
    align = '\t'
else:
    align = ''

f = open('genMatch_%s.txt' %(options.inputFile[0:options.inputFile.rfind('.')]),'w')
f.write('%s%s\t\t  Tight\t\t\t\t|\t\t Relaxed\t\t\t\t\t\n' %(sampleName,align))
f.write('\t\tSame Sign\tOpposite Sign\t\t|\tSame Sign\tOpposite Sign\t\t\n')
sumSS = 0
sumOS = 0
sumSS2 = 0
sumOS2 = 0
for i in range(len(counterList)):
    if counterList[i][0] in ['tau(b) tau(b)', 'tau tau(b)','tau e(tau)', 'b e(tau)', 'e(tau) e', 'e(tau) e(tau)',
                            'e(tau) mu', 'e(tau) None', 'tau None', 'None None', 'tau e(b)',
                            'e(b) e(b)', 'e(b) None', 'tau(b) b', 'tau(b) e', 'tau(b) e(tau)', 'tau(b) e(b)',
                            'tau(b) mu', 'tau(b) None', 'e(tau) e(b)']:
        f.write('%s\t%i\t\t%i\t\t\t|\t%i\t\t%i\t\t\t\n' %(counterList[i][0], counterList[i][1], counterList[i][2], counterList2[i][1], counterList2[i][2]))   
    else: 
        f.write('%s\t\t%i\t\t%i\t\t\t|\t%i\t\t%i\t\t\t\n' %(counterList[i][0], counterList[i][1], counterList[i][2], counterList2[i][1], counterList2[i][2]))
    if i > 0:
        sumSS+=counterList[i][1]
        sumOS+=counterList[i][2]
        sumSS2+=counterList2[i][1]
        sumOS2+=counterList2[i][2]
f.write('Sum\t\t%i\t\t%i\t\t\t|\t%i\t\t%i\n' %(sumSS, sumOS, sumSS2, sumOS2))
f.close()
