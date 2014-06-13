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
    parser.add_option("--l", dest="lep", default = "ele", help="")
    parser.add_option("--m", dest="max", default = 1000, help="")


    options, args = parser.parse_args()
    return options

def passCut(iTree):
    if iTree.J1CSVbtagCSVSort < 0.679 or iTree.J2CSVbtagCSVSort < 0.244:
        return False
    if iTree.pt2 < 45:
        return False
    return True

options = opts()
ran = [10, -4, 4]


yMax = float(options.max)


tauPt_hl = r.TH1F('tauPt_hl','', ran[0], ran[1], ran[2])
tauPt_ll = r.TH1F('tauPt_ll','', ran[0], ran[1], ran[2])
ZZ = r.TH1F('ZZ','', ran[0], ran[1], ran[2])

tauPt = r.TH1F('tauPt','', ran[0], ran[1], ran[2])
tauPtData = r.TH1F('tauPtData','', ran[0], ran[1], ran[2])

ifile1 = r.TFile('/nfs_scratch/ojalvo/LTau_12_2/TT_HL.root')
ifile2 = r.TFile('/nfs_scratch/ojalvo/LTau_12_2/TT_LL.root')
ifile3 = r.TFile('/nfs_scratch/ojalvo/LTau_12_2/ZZ-LLQQ.root')

dataFile = r.TFile('/nfs_scratch/ojalvo/LTau_12_2/DATA.root')


lepton = options.lep
LEPTON = "ET"
if lepton == "mu":
    LEPTON = "MT"

iTree1 = ifile1.Get("%sTauEventTreeFinal/eventTree" %lepton)
tmpHist1 = ifile1.Get("%s/results" %LEPTON)
initTT_hl = tmpHist1.GetBinContent(1)
iTree2 = ifile2.Get("%sTauEventTreeFinal/eventTree" %lepton)
tmpHist2 = ifile2.Get("%s/results" %LEPTON)
initTT_ll = tmpHist2.GetBinContent(1)
iTree3 = ifile3.Get("%sTauEventTreeFinal/eventTree" %lepton)
tmpHist3 = ifile3.Get("%s/results" %LEPTON)
initZZ = tmpHist3.GetBinContent(1)


dataTree = dataFile.Get("%sTauEventTreeFinal/eventTree" %lepton)
total1 = iTree1.GetEntries()
total2 = iTree2.GetEntries()
total3 = iTree3.GetEntries()
totalData = dataTree.GetEntries()

Lumi = 19.7
scale_hl = Lumi*109281/initTT_hl
scale_ll = Lumi*26197.5/initTT_ll
scale_ZZ = Lumi*2500/initZZ

for i in range(total1):
    r.gStyle.SetOptStat(0)
    tool.printProcessStatus(iCurrent=i, total=total1, processName = 'Looping sample')
    iTree1.GetEntry(i)
    if not passCut(iTree1):
        continue
    tauPt_hl.Fill(iTree1.phi2)
    tauPt.Fill(iTree1.phi2, scale_hl)
print ''
for i in range(total2):
    r.gStyle.SetOptStat(0)
    tool.printProcessStatus(iCurrent=i, total=total2, processName = 'Looping sample')
    iTree2.GetEntry(i)
    if not passCut(iTree2):
        continue
    tauPt_ll.Fill(iTree2.phi2)
    tauPt.Fill(iTree2.phi2, scale_ll)
print ''
print ''
for i in range(total3):
    r.gStyle.SetOptStat(0)
    tool.printProcessStatus(iCurrent=i, total=total3, processName = 'Looping sample')
    iTree3.GetEntry(i)
    if not passCut(iTree3):
        continue
    ZZ.Fill(iTree3.phi2)
    tauPt.Fill(iTree3.phi2, scale_ZZ)
print ''
for i in range(totalData):
    r.gStyle.SetOptStat(0)
    tool.printProcessStatus(iCurrent=i, total=totalData, processName = 'Looping sample')
    dataTree.GetEntry(i)
    if not passCut(dataTree):
        continue
    tauPtData.Fill(dataTree.phi2)

legendPosition = (0.5, 0.7, 0.90, 0.88)

legendHistos = [(tauPt_hl,"tt-semi"),
                (tauPt_ll,"tt-full"),
                (ZZ,"ZZ-llqq"),
                (tauPtData,"data")]
print ''

#scaling
tauPt_hl.Scale(scale_hl)
tauPt_ll.Scale(scale_ll)
ZZ.Scale(scale_ZZ)
stack = r.THStack()
tauPt_hl.SetFillColor(r.kAzure+7)
tauPt_ll.SetFillColor(r.kRed-7)
ZZ.SetFillColor(r.kYellow)
stack.Add(ZZ)
stack.Add(tauPt_hl)
stack.Add(tauPt_ll)

psfile = 'LTauMCValidation_%s.pdf' %lepton

c = r.TCanvas("c","Test", 800, 600)
stack.SetTitle('MC Validation; tau phi; events / bin')
stack.SetMaximum(yMax)
stack.Draw()
tauPtData.SetMarkerStyle(8)
tauPtData.SetMarkerSize(0.9)
tauPtData.Draw('sameE')
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos)
l1.Draw("same")

c.Update()
c.Print('%s(' %psfile)
c.Clear()
tauInfo = tauPtData.Clone()
tauInfo.Sumw2()
tauInfo.Divide(tauPt)
tauInfo.SetMarkerStyle(8)
tauInfo.SetMarkerSize(0.9)
tauInfo.SetMaximum(1.5)
tauInfo.SetMinimum(0.5)
tauInfo.Draw('E')
fitLine = r.TF1("fitLine","[0]", ran[1], ran[2])
tauInfo.Fit('fitLine','0ERM')
fitLine.SetLineColor(r.kRed)
fitLine.SetLineStyle(2)
fitLine.Draw('same')
lFit = tool.setMyLegend((0.63, 0.8, 0.93, 0.9),
                        [(fitLine,'Scale: %.3f \pm %.3f' %(fitLine.GetParameter(0), fitLine.GetParError(0)))])
lFit.Draw('same')
c.Update()
c.Print('%s)' %psfile)

print 'saved plot at: %s' %psfile
