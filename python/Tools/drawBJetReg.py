#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import math
import optparse
import os

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
j1Reg = lvClass()
j2Reg = lvClass()

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--i", dest="inputFile", default = False, help="")
    parser.add_option("--m", dest="max", default = 1.5, help="")
    parser.add_option("--m2", dest="max2", default = 800, help="")
    parser.add_option("--t", dest="tail", default = '', help="")
    parser.add_option("--c", dest="cut", default = 'none', help="")

    options, args = parser.parse_args()
    return options

def passCut(iTree, cut):
    if 'bTag' in cut:
        if iTree.CSVJ1 < 0.679 or iTree.CSVJ2 < 0.244:
            return False
    if 'iso' in cut:
        if iTree.iso1.at(0) > 1.5 or iTree.iso2.at(0) > 1.5:
            return False
    if 'softLept0' in cut:
        if not (iTree.CSVJ1SoftLeptPt + iTree.CSVJ2SoftLeptPt == 0):
            return False
    if 'softLept1' in cut:
        if not (iTree.CSVJ1SoftLeptPt*iTree.CSVJ2SoftLeptPt == 0 and iTree.CSVJ1SoftLeptPt + iTree.CSVJ2SoftLeptPt != 0):
            return False
    if 'softLept2' in cut:
        if not (iTree.CSVJ1SoftLeptPt>0 and iTree.CSVJ2SoftLeptPt>0):
            return False
    return True

options = opts()
ran = [30, 0, 300]
ran2 = [15, 50, 200]

yMax = int(options.max)

jet1PtOverGenJet1Pt = r.TH2F('jet1PtOverGenJet1Pt','', ran[0], ran[1], ran[2], 30, 0, 2)
jet2PtOverGenJet2Pt = r.TH2F('jet2PtOverGenJet2Pt','', ran[0], ran[1], ran[2], 30, 0, 2)
regJet1PtOverGenJet1Pt = r.TH2F('regJet1PtOverGenJet1Pt','', ran[0], ran[1], ran[2], 30, 0, 2)
regJet2PtOverGenJet2Pt = r.TH2F('regJet2PtOverGenJet2Pt','', ran[0], ran[1], ran[2], 30, 0, 2)



mJJ = r.TH1F('mJJ','', ran2[0], ran2[1], ran2[2])
mJJReg = r.TH1F('mJJReg','', ran2[0], ran2[1], ran2[2])
genMJJReg = r.TH1F('genMJJReg','', ran2[0], ran2[1], ran2[2])

ifile = r.TFile(options.inputFile)
iTree = ifile.Get("eventTree")
total = iTree.GetEntries()

for i in range(total):
    r.gStyle.SetOptStat(0)
    tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample')
    iTree.GetEntry(i)
    if not passCut(iTree, options.cut):
        continue

    j1Reg.SetCoordinates(iTree.CSVJ1PtReg, iTree.CSVJ1Eta, iTree.CSVJ1Phi, iTree.CSVJ1Mass)
    j2Reg.SetCoordinates(iTree.CSVJ2PtReg, iTree.CSVJ2Eta, iTree.CSVJ2Phi, iTree.CSVJ2Mass)
    genJ1Pt = iTree.matchGenJet1Pt
    genJ2Pt = iTree.matchGenJet2Pt

    regJet1PtOverGenJet1Pt.Fill(genJ1Pt, iTree.CSVJ1PtReg/genJ1Pt, iTree.triggerEff)
    regJet2PtOverGenJet2Pt.Fill(genJ2Pt, iTree.CSVJ2PtReg/genJ2Pt, iTree.triggerEff)

    jet1PtOverGenJet1Pt.Fill(genJ1Pt, iTree.CSVJ1Pt/genJ1Pt, iTree.triggerEff)
    jet2PtOverGenJet2Pt.Fill(genJ2Pt, iTree.CSVJ2Pt/genJ2Pt, iTree.triggerEff)

    mJJ.Fill(iTree.mJJ, iTree.triggerEff)
    mJJReg.Fill((j1Reg+j2Reg).mass(), iTree.triggerEff)
    genMJJReg.Fill(iTree.matchGenMJJ, iTree.triggerEff)


legendPosition = (0.5, 0.7, 0.90, 0.88)
legendPosition3 = (0.3, 0.7, 0.90, 0.88)
legendHistos1 = [(jet1PtOverGenJet1Pt,"jet pt vs gen jet pt"),
                (regJet1PtOverGenJet1Pt,"regressed jet pt vs gen jet pt")]
legendHistos2 = [(jet2PtOverGenJet2Pt,"jet pt vs gen jet pt"),
                (regJet2PtOverGenJet2Pt,"regressed jet pt vs gen jet pt")]
legendHistos3 = [(mJJ,"mJJ (mean: %.1f  RMS: %.1f)" %(mJJ.GetMean(), mJJ.GetRMS())), 
                (mJJReg,"regressed mJJ (mean: %.1f  RMS: %.1f)" %(mJJReg.GetMean(), mJJReg.GetRMS())),
                (genMJJReg,"gen mJJ (mean: %.1f  RMS: %.1f)" %(genMJJReg.GetMean(), genMJJReg.GetRMS()))
                ]

print ''

psfile = options.inputFile[0:options.inputFile.rfind('.')]+options.tail+'_'+options.cut+'_reg.pdf'

sampleName = options.inputFile[options.inputFile.find('TMVARegApp'): options.inputFile.rfind('.')]

c = r.TCanvas("c","Test", 800, 600)
ps = r.TPDF(psfile,112)
c.Divide(2,2)
c.cd(1)
jet1PtOverGenJet1Pt.SetTitle('%s b jet regression (%s); gen pt1 (GeV); pt1 / gen pt1' %(sampleName,options.cut))
jet1PtOverGenJet1Pt.Draw("P")
print 'events %i' %jet1PtOverGenJet1Pt.Integral()
jet1PtOverGenJet1Pt.SetMarkerColor(r.kAzure+8)
jet1PtOverGenJet1Pt.SetMarkerStyle(2)
regJet1PtOverGenJet1Pt.SetMarkerColor(r.kRed)
regJet1PtOverGenJet1Pt.SetMarkerStyle(5)
regJet1PtOverGenJet1Pt.Draw('same')
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos1)
l1.Draw("same")
line = r.TLine(ran[1],1,ran[2],1)
line.SetLineStyle(2)
line.SetLineColor(r.kBlack)
line.Draw('same')
c.cd(2)
jet2PtOverGenJet2Pt.SetTitle('%s b jet regression (%s); gen pt2 (GeV); pt2 / gen pt2' %(sampleName,options.cut))
jet2PtOverGenJet2Pt.Draw("P")
jet2PtOverGenJet2Pt.SetMarkerColor(r.kAzure+8)
jet2PtOverGenJet2Pt.SetMarkerStyle(2)
regJet2PtOverGenJet2Pt.SetMarkerColor(r.kRed)
regJet2PtOverGenJet2Pt.SetMarkerStyle(5)
regJet2PtOverGenJet2Pt.Draw('same')
l2 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos2)
l2.Draw("same")
line.Draw('same')
c.cd(3)
mJJ.SetTitle('%s b jet regression (%s); mJJ (GeV); events / bin' %(sampleName,options.cut))
mJJ.Draw()
mJJ.SetMaximum(int(options.max2))
mJJ.SetFillColor(r.kAzure+8)
mJJ.SetLineColor(r.kAzure+8)
mJJ.SetFillStyle(3002)
mJJReg.Draw('same')
mJJReg.SetLineColor(r.kRed)
mJJReg.SetLineWidth(2)
genMJJReg.Draw('same')
genMJJReg.SetLineColor(r.kBlack)
genMJJReg.SetLineWidth(2)
genMJJReg.SetLineStyle(2)
l3 = tool.setMyLegend(lPosition=legendPosition3, lHistList=legendHistos3)
l3.Draw("same")
c.Update()
ps.Close()

print 'saved plot at: %s' %psfile