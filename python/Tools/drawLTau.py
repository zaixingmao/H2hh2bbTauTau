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
    parser.add_option("--l", dest="lep", default = "mu", help="")
    parser.add_option("--m", dest="max", default = 500, help="")


    options, args = parser.parse_args()
    return options

def passCut(iTree):
    if iTree.J1CSVbtagCSVSort < 0.679 or iTree.J2CSVbtagCSVSort < 0.244:
        return False
    if iTree.charge != 0:
        return False
    if iTree.pt2 < 45:
        return False
    if 100 < iTree.svMass < 150:
        return False

    return True

options = opts()
ran = [22, 30, 250]


yMax = float(options.max)

background = []
files = []
trees = []
inits = []
stack = r.THStack()
legendHistos = []

Lumi = 19.7

preFix = '/nfs_scratch/ojalvo/LTau_12_2/'

fileList = [('ZZ', preFix + 'ZZ-LLQQ.root', 2500, 5),
            ('tt_full_lep',preFix + 'TT_LL.root', 26197.5, r.kRed-7),
            ('tt_semi_lep',preFix + 'TT_HL.root', 109281, r.kAzure+7)]

totalBkg = r.TH1F('totalBkg','', ran[0], ran[1], ran[2])
data = r.TH1F('data','', ran[0], ran[1], ran[2])

dataFile = r.TFile('/nfs_scratch/ojalvo/LTau_12_2/DATA.root')


lepton = options.lep
LEPTON = "ET"
if lepton == "mu":
    LEPTON = "MT"

dataTree = dataFile.Get("%sTauEventTreeFinal/eventTree" %lepton)
totalData = dataTree.GetEntries()

for i in range(totalData):
    r.gStyle.SetOptStat(0)
    tool.printProcessStatus(iCurrent=i, total=totalData, processName = 'Looping sample')
    dataTree.GetEntry(i)
    if not passCut(dataTree):
        continue
    data.Fill(dataTree.pt2)
legendHistos.append((data, 'data (%.0f)' %data.Integral()))
print ''

legendPosition = (0.5, 0.7, 0.90, 0.88)

i = 0
for iSample, iFile, iXS, iColor in fileList:
    background.append(r.TH1F(iSample,'', ran[0], ran[1], ran[2]))
    files.append(r.TFile(iFile))
    trees.append(files[i].Get("%sTauEventTreeFinal/eventTree" %lepton))
    inits.append(files[i].Get("%s/results" %LEPTON).GetBinContent(1))
    total = trees[i].GetEntries()
    scale = Lumi*iXS/inits[i]
    for j in range(total):
        tool.printProcessStatus(iCurrent=j, total=total, processName = 'Looping sample')
        trees[i].GetEntry(j)
        if not passCut(trees[i]):
            continue
        background[i].Fill(trees[i].pt2, scale)
        background[i].SetFillColor(iColor)
    stack.Add(background[i])
    legendHistos.append((background[i], '%s (%.1f)'%(iSample, background[i].Integral())))
    print ''
    totalBkg = totalBkg + background[i]
    i += 1



print ''

psfile = 'LTauMCValidation_%s.pdf' %lepton

c = r.TCanvas("c","Test", 800, 600)
stack.SetTitle('MC Validation 19.7 fb^{-1}; tau phi; events / bin')
stack.SetMaximum(yMax)
stack.Draw()
stack.GetYaxis().SetTitleOffset(1.4)
data.SetMarkerStyle(8)
data.SetMarkerSize(0.9)
data.Draw('sameE')
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHistos)
l1.Draw("same")

print 'data/MC %f'%(data.Integral()/totalBkg.Integral())

c.Update()
c.Print('%s(' %psfile)
c.Clear()
tauInfo = data.Clone()
tauInfo.Sumw2()
tauInfo.Divide(totalBkg)
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
