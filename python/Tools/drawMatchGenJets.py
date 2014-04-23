#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import math
import optparse

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--i", dest="inputFile", default = False, help="")
    parser.add_option("--t", dest="title", default = False, help="")
    options, args = parser.parse_args()
    return options

options = opts()

r.gStyle.SetOptStat(0)

histRange = [20, 0, 400]
histRange2 = [20, 0, 0.5]

j1pt = r.TH1F('j1pt', '', histRange[0], histRange[1], histRange[2])
j2pt = r.TH1F('j2pt', '', histRange[0], histRange[1], histRange[2])
genJ1pt = r.TH1F('genJ1pt', '', histRange[0], histRange[1], histRange[2])
genJ2pt = r.TH1F('genJ2pt', '', histRange[0], histRange[1], histRange[2])

j1dR = r.TH1F('j1dR', '', histRange2[0], histRange2[1], histRange2[2])
j2dR = r.TH1F('j2dR', '', histRange2[0], histRange2[1], histRange2[2])

title = options.title

psfile = 'genJetMatch'

iFile = r.TFile(options.inputFile)
iTree = iFile.Get('eventTree')

legendPosition = (0.65, 0.8, 0.9, 0.9)

legendList = []
histList1 = [(j1pt, 'first CSV jet'),
            (genJ1pt, 'matched gen jet')]
histList2 = [(j2pt, 'second CSV jet'),
            (genJ2pt, 'matched gen jet')]

total = iTree.GetEntries()
for i in range(0, total):
    tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample')
    iTree.GetEntry(i)
    #for same signs
    
    if not (iTree.CSVJ1 > 0.679 and iTree.CSVJ2 > 0.244):
        continue
    if iTree.charge1.at(0) + iTree.charge2.at(0) == 0:
        j1pt.Fill(iTree.CSVJ1Pt, iTree.triggerEff)
        j2pt.Fill(iTree.CSVJ2Pt, iTree.triggerEff)
        genJ1pt.Fill(iTree.matchGenJet1Pt, iTree.triggerEff)
        genJ2pt.Fill(iTree.matchGenJet2Pt, iTree.triggerEff)
        j1dR.Fill(iTree.dRGenJet1Match, iTree.triggerEff)
        j2dR.Fill(iTree.dRGenJet2Match, iTree.triggerEff)

print''


c = r.TCanvas("c","Test", 800, 600)
ps = r.TPDF('%s_%s.pdf' %(psfile, title),112)
c.Divide(2,2)
c.cd(1)
r.gPad.SetLogy()
j1pt.SetTitle('%s gen jet match dR < 0.2 pt; pt1; events / bins' %(title))
j1pt.Draw()
genJ1pt.SetLineColor(r.kRed)
genJ1pt.Draw("same")
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=histList1)
l1.Draw("same")
c.Update()
c.cd(2)
r.gPad.SetLogy()
j2pt.SetTitle('%s gen jet match dR < 0.2 pt; pt2; events / bin' %(title))
j2pt.Draw("")
genJ2pt.SetLineColor(r.kRed)
genJ2pt.Draw("same")
l2 = tool.setMyLegend(lPosition=legendPosition, lHistList=histList2)
l2.Draw("same")
c.Update()
c.cd(3)
j1dR.SetTitle('dR between genJet and jet1; dR; events / bins')
j1dR.Draw()
c.Update()
c.cd(4)
j2dR.SetTitle('dR between genJet and jet2; dR; events / bins')
j2dR.Draw()
c.Update()
ps.Close()



