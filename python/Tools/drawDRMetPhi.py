#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import math
import optparse
import os

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--i", dest="inputFile", default = False, help="")
    options, args = parser.parse_args()
    return options


def findBCandsPhi(jetsList = []):
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    return jetsList[0][1].phi(), jetsList[1][1].phi()

options = opts()
ran = [20, 0, 6]

dPhiMetJ1_SS = r.TH1F('dPhiMetJ1_SS','', ran[0], ran[1], ran[2])
dPhiMetJ2_SS = r.TH1F('dPhiMetJ2_SS','', ran[0], ran[1], ran[2])
dPhiMetTau1_SS = r.TH1F('dPhiMetTau1_SS','', ran[0], ran[1], ran[2])
dPhiMetTau2_SS = r.TH1F('dPhiMetTau2_SS','', ran[0], ran[1], ran[2])

dPhiMetJ1_OS = r.TH1F('dPhiMetJ1_OS','', ran[0], ran[1], ran[2])
dPhiMetJ2_OS = r.TH1F('dPhiMetJ2_OS','', ran[0], ran[1], ran[2])
dPhiMetTau1_OS = r.TH1F('dPhiMetTau1_OS','', ran[0], ran[1], ran[2])
dPhiMetTau2_OS = r.TH1F('dPhiMetTau2_OS','', ran[0], ran[1], ran[2])

dPhiMetJ1_SS.SetTitle('dPhiMetJ1 Same Sign; abs(dPhiMet_J1);')
dPhiMetJ2_SS.SetTitle('dPhiMetJ1 Same Sign; abs(dPhiMet_J1);')
dPhiMetTau1_SS.SetTitle('dPhiMetTau1 Same Sign; abs(dPhiMet_Tau1);')
dPhiMetTau2_SS.SetTitle('dPhiMetTau1 Same Sign; abs(dPhiMet_Tau1);')
dPhiMetJ1_OS.SetTitle('dPhiMetJ1 Opposite Sign; abs(dPhiMet_J1);')
dPhiMetJ2_OS.SetTitle('dPhiMetJ1 Opposite Sign; abs(dPhiMet_J1);')
dPhiMetTau1_OS.SetTitle('dPhiMetTau1 Opposite Sign; abs(dPhiMet_Tau1);')
dPhiMetTau2_OS.SetTitle('dPhiMetTau1 Opposite Sign; abs(dPhiMet_Tau1);')

ifile = r.TFile(options.inputFile)
iTree = ifile.Get("eventTree")
total = iTree.GetEntries()

for i in range(total):
    tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample')
    iTree.GetEntry(i)

    jetsList = [(iTree.J1CSVbtag, J1.SetCoordinates(iTree.J1Pt, iTree.J1Eta, iTree.J1Phi, iTree.J1Mass)),
                (iTree.J2CSVbtag, J2.SetCoordinates(iTree.J2Pt, iTree.J2Eta, iTree.J2Phi, iTree.J2Mass)),
                (iTree.J3CSVbtag, J3.SetCoordinates(iTree.J3Pt, iTree.J3Eta, iTree.J3Phi, iTree.J3Mass)),
                (iTree.J4CSVbtag, J4.SetCoordinates(iTree.J4Pt, iTree.J4Eta, iTree.J4Phi, iTree.J4Mass))]

    CSVJ1Phi, CSVJ2Phi = findBCandsPhi(jetsList)

    #for same signs
    if iTree.charge1.at(0) == iTree.charge2.at(0):
        dPhiMetJ1_SS.Fill(abs(iTree.metphi.at(0) - CSVJ1Phi))        
        dPhiMetJ2_SS.Fill(abs(iTree.metphi.at(0) - CSVJ2Phi))  
        dPhiMetTau1_SS.Fill(abs(iTree.metphi.at(0) - iTree.phi1.at(0)))        
        dPhiMetTau2_SS.Fill(abs(iTree.metphi.at(0) - iTree.phi2.at(0))) 

    #for opposite signs
    elif iTree.charge1.at(0) == - iTree.charge2.at(0):
        dPhiMetJ1_OS.Fill(abs(iTree.metphi.at(0) - CSVJ1Phi))        
        dPhiMetJ2_OS.Fill(abs(iTree.metphi.at(0) - CSVJ2Phi))  
        dPhiMetTau1_OS.Fill(abs(iTree.metphi.at(0) - iTree.phi1.at(0)))        
        dPhiMetTau2_OS.Fill(abs(iTree.metphi.at(0) - iTree.phi2.at(0))) 

print ''

psfile = options.inputFile[0:options.inputFile.rfind('.')]+'_SS.pdf'
psfile2 = options.inputFile[0:options.inputFile.rfind('.')]+'_OS.pdf'

c = r.TCanvas("c","Test", 800, 600)
ps = r.TPDF(psfile,112)
c.Divide(2,2)
c.cd(1)
dPhiMetJ1_SS.Draw()
c.cd(2)
dPhiMetJ2_SS.Draw()
c.cd(3)
dPhiMetTau1_SS.Draw()
c.cd(4)
dPhiMetTau2_SS.Draw()
c.Update()
ps.Close()
c = r.TCanvas("c2","Test", 800, 600)
ps1 = r.TPDF(psfile2,112)
c.Divide(2,2)
c.cd(1)
dPhiMetJ1_OS.Draw()
c.cd(2)
dPhiMetJ2_OS.Draw()
c.cd(3)
dPhiMetTau1_OS.Draw()
c.cd(4)
dPhiMetTau2_OS.Draw()
c.Update()
ps1.Close()

print 'saved plot at: %s' %psfile