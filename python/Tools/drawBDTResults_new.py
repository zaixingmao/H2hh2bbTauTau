#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import optparse

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******
def opts():
    parser = optparse.OptionParser()
    parser.add_option("-m", dest="trainMass", default="260", help="mass of trained H")
    options, args = parser.parse_args()
    return options

options = opts()

trainMass = options.trainMass

fileList = [('1000 Events', '/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVA_H2hh%s_new_1000.root' %(trainMass)),
            ('2000 Events', '/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVA_H2hh%s_new_2000.root' %(trainMass)),
            ('3000 Events', '/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVA_H2hh%s_new_3000.root' %(trainMass)),
            ('4000 Events', '/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVA_H2hh%s_new_4000.root' %(trainMass))]

branchName = "Method_BDT/BDT/MVA_BDT_rejBvsS"
psfile="BDT_diff_%s.pdf" %(trainMass)
titles = "Background rejection versus Signal efficiency (mH%s); Signal efficiency; Background rejection" %(trainMass)

colorList = [r.kGreen, r.kRed, r.kBlue, 1]
histRange = [100, 0 , 1]

tmpHist = []
tmpFile = []
histList = []
for i in range(len(fileList)):
    tmpFile.append(r.TFile(fileList[i][1]))
    tmpHist.append(r.TH1D("tmp%s" %(i), "tmp%s" %(i), histRange[0], histRange[1], histRange[2]))
    tmpHist[i] = tmpFile[i].Get(branchName)
    tmpHist[i].SetLineColor(colorList[i])
    histList.append((tmpHist[i], fileList[i][0]))


legendPosition = (0.25, 0.3, 0.5, 0.47)
index = 0
c = r.TCanvas("c","Test", 800, 600);
ps = r.TPDF(psfile,112)
r.gPad.SetTickx()
r.gPad.SetTicky()

r.gPad.SetGrid()

tmpHist[0].SetTitle(titles)
tmpHist[3].SetLineStyle(2)
tmpHist[0].SetMaximum(1.05)
tmpHist[0].SetMinimum(0.1)
tmpHist[0].Draw()
for i in range(1,len(tmpHist)):
    tmpHist[i].Draw("same")

l = tool.setMyLegend(lPosition=legendPosition, lHistList=histList)
l.Draw("same")
ps.Close()

print "Plot saved at: %s" %(psfile)