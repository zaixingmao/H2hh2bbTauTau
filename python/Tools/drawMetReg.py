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
    parser.add_option("--m", dest="max", default = 200, help="")
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
ran = [15, 0, 100]
ran2 = [20, -100, 100]
ran3 = [30, 0, 300]

yMax = int(options.max)


met = r.TH1F('met','', ran[0], ran[1], ran[2])
metReg = r.TH1F('metReg','', ran[0], ran[1], ran[2])
metInTauPair= r.TH1F('metInTauPair','', ran2[0], ran2[1], ran2[2])
metRegInTauPair= r.TH1F('metRegInTauPair','', ran2[0], ran2[1], ran2[2])

svMass = r.TH1F('svMass','', ran3[0], ran3[1], ran3[2])
mTauPair = r.TH1F('mTauPair','', ran3[0], ran3[1], ran3[2])
mTauPairWithMet = r.TH1F('mTauPairWithMet','', ran3[0], ran3[1], ran3[2])
mTauPairWithMetReg = r.TH1F('mTauPairWithMetReg','', ran3[0], ran3[1], ran3[2])

ifile = r.TFile(options.inputFile)
iTree = ifile.Get("eventTree")
total = iTree.GetEntries()

for i in range(total):
    r.gStyle.SetOptStat(0)
    tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample')
    iTree.GetEntry(i)
    if not passCut(iTree, options.cut):
        continue
    met.Fill(iTree.met.at(0), iTree.triggerEff)
    metReg.Fill(iTree.metReg, iTree.triggerEff)
    metInTauPair.Fill(iTree.metInTauPair, iTree.triggerEff)
    metRegInTauPair.Fill(iTree.metRegInTauPair, iTree.triggerEff)
    svMass.Fill(iTree.svMass.at(0), iTree.triggerEff)
    mTauPairWithMet.Fill(iTree.mTauPairWithMet, iTree.triggerEff)
    mTauPairWithMetReg.Fill(iTree.mTauPairWithMetReg, iTree.triggerEff)
    mTauPair.Fill(iTree.mTauPair, iTree.triggerEff)

legendPosition = (0.5, 0.7, 0.90, 0.88)
legendPosition3 = (0.1, 0.75, 0.95, 0.9)
legendHistos1 = [(met,"met"),
                (metReg,"met with regressed jet")]
legendHistos2 = [(metInTauPair,"met projected in tau pair direction"),
                (metRegInTauPair,"met with regressed jet projected in tau pair direction")]
legendHistos3 = [(mTauPairWithMet,"mTauPair with met info"), 
                (mTauPairWithMetReg,"mTauPair with regressed met info"),
                (svMass, "svMass"),
                (mTauPair, 'mTauTau')]

print ''

psfile = options.inputFile[0:options.inputFile.rfind('.')]+options.tail+'_'+options.cut+'_reg.pdf'

sampleName = options.inputFile[options.inputFile.find('TMVARegApp_'): options.inputFile.rfind('_new')]

c = r.TCanvas("c","Test", 800, 600)
c.Divide(2,2)
ps = r.TPDF(psfile,112)
c.cd(1)
met.SetTitle('%s met (%s); met (GeV); events / bin' %(sampleName,options.cut))
met.Draw()
met.SetMaximum(int(options.max))
met.SetFillColor(r.kAzure+8)
met.SetLineColor(r.kAzure+8)
met.SetFillStyle(3002)
metReg.Draw('same')
metReg.SetLineColor(r.kRed)
metReg.SetLineWidth(2)
l1 = tool.setMyLegend(lPosition=legendPosition3, lHistList=legendHistos1)
l1.Draw("same")
c.Update()
c.cd(2)
metInTauPair.SetTitle('%s met projected in tau pair direction (%s); met (GeV); events / bin' %(sampleName,options.cut))
metInTauPair.Draw()
metInTauPair.SetMaximum(int(options.max))
metInTauPair.SetFillColor(r.kAzure+8)
metInTauPair.SetLineColor(r.kAzure+8)
metInTauPair.SetFillStyle(3002)
metRegInTauPair.Draw('same')
metRegInTauPair.SetLineColor(r.kRed)
metRegInTauPair.SetLineWidth(2)
l2 = tool.setMyLegend(lPosition=legendPosition3, lHistList=legendHistos2)
l2.Draw("same")
c.Update()
c.cd(3)
mTauPairWithMet.SetTitle('%s mTauTau (%s); mTauTau (GeV); events / bin' %(sampleName,options.cut))
mTauPairWithMet.Draw()
mTauPairWithMet.SetMaximum(int(options.max2))
mTauPairWithMet.SetFillColor(r.kAzure+8)
mTauPairWithMet.SetLineColor(r.kAzure+8)
mTauPairWithMet.SetFillStyle(3002)
mTauPairWithMetReg.Draw('same')
mTauPairWithMetReg.SetLineColor(r.kRed)
mTauPairWithMetReg.SetLineWidth(2)
svMass.SetLineWidth(2)
svMass.SetLineStyle(2)
svMass.SetLineColor(r.kBlack)
svMass.Draw('same')
mTauPair.SetLineWidth(2)
mTauPair.SetLineStyle(2)
mTauPair.SetLineColor(r.kGreen)
mTauPair.Draw('same')
l3 = tool.setMyLegend(lPosition=legendPosition3, lHistList=legendHistos3)
l3.Draw("same")
c.Update()
ps.Close()

print 'saved plot at: %s' %psfile
