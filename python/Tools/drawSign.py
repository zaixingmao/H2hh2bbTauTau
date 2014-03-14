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

histRange = [46, 20, 250]
histRange2 = [50, -2.5, 2.5]
histRange3 = [50, 0, 5]

tmpHist1 = r.TH1F('tmpHist1', '', histRange[0], histRange[1], histRange[2])
tmpHist2 = r.TH1F('tmpHist2', '', histRange[0], histRange[1], histRange[2])
tmpHist3 = r.TH1F('tmpHist3', '', histRange[0], histRange[1], histRange[2])
tmpHist4 = r.TH1F('tmpHist4', '', histRange[0], histRange[1], histRange[2])
tmpHist5 = r.TH1F('tmpHist5', '', histRange[0], histRange[1], histRange[2])
tmpHist6 = r.TH1F('tmpHist6', '', histRange[0], histRange[1], histRange[2])
tmpHist7 = r.TH1F('tmpHist7', '', 5, 0, 5)
tmpHist8 = r.TH1F('tmpHist8', '', 5, 0, 5)
tmpHist_m1_s = r.TH1F('tmpHist_m1_s', '', histRange3[0], histRange3[1], histRange3[2])
tmpHist_m2_s = r.TH1F('tmpHist_m2_s', '', histRange3[0], histRange3[1], histRange3[2])
tmpHist_m1_t = r.TH1F('tmpHist_m1_o', '', histRange3[0], histRange3[1], histRange3[2])
tmpHist_m2_t = r.TH1F('tmpHist_m2_o', '', histRange3[0], histRange3[1], histRange3[2])
tmpHist_mEff = r.TH1F('tmpHist_mEff', '', histRange3[0], histRange3[1], histRange3[2])

tmpHist_total1 = r.TH1F('total1', '', histRange[0], histRange[1], histRange[2])
tmpHist_total2 = r.TH1F('total2', '', histRange[0], histRange[1], histRange[2])

tmpHist1_eta = r.TH1F('tmpHist1_eta', '', histRange2[0], histRange2[1], histRange2[2])
tmpHist2_eta = r.TH1F('tmpHist2_eta', '', histRange2[0], histRange2[1], histRange2[2])
tmpHist3_eta = r.TH1F('tmpHist3_eta', '', histRange2[0], histRange2[1], histRange2[2])
tmpHist4_eta = r.TH1F('tmpHist4_eta', '', histRange2[0], histRange2[1], histRange2[2])
tmpHist5_eta = r.TH1F('tmpHist5_eta', '', histRange2[0], histRange2[1], histRange2[2])
tmpHist6_eta = r.TH1F('tmpHist6_eta', '', histRange2[0], histRange2[1], histRange2[2])
tmpHist_eta_total1 = r.TH1F('total1_eta', '', histRange2[0], histRange2[1], histRange2[2])
tmpHist_eta_total2 = r.TH1F('total2_eta', '', histRange2[0], histRange2[1], histRange2[2])

tmpHist_sc = r.TH1F('tmpHist5_sc', '', 7, -3, 3)
tmpHist_oc = r.TH1F('tmpHist5_oc', '', 7, -3, 3)

title = options.title

psfile = 'chargeSignVS'

iFile = r.TFile(options.inputFile)
iTree = iFile.Get('eventTree')

legendPosition = (0.65, 0.8, 0.9, 0.9)
#draw from the highest histogram
legendList = []
histList1 = [(tmpHist1, 'Same Sign Events'),
            (tmpHist3, 'Opposite Sign Events')]
histList2 = [(tmpHist2, 'Same Sign Events'),
            (tmpHist4, 'Opposite Sign Events')]
histList3 = [(tmpHist1_eta, 'Same Sign Events'),
            (tmpHist3_eta, 'Opposite Sign Events')]
histList4 = [(tmpHist2_eta, 'Same Sign Events'),
            (tmpHist4_eta, 'Opposite Sign Events')]
histList5 = [(tmpHist_sc, 'Same Sign Events'),
            (tmpHist_oc, 'Opposite Sign Events')]

total = iTree.GetEntries()
for i in range(0, total):
    tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample')
    iTree.GetEntry(i)
    #for same signs
    if iTree.charge1.at(0) == iTree.charge2.at(0):
        tmpHist1.Fill(iTree.pt1.at(0))
        tmpHist2.Fill(iTree.pt2.at(0))
        tmpHist1_eta.Fill(iTree.eta1.at(0))
        tmpHist2_eta.Fill(iTree.eta2.at(0))
        tmpHist_sc.Fill(iTree.charge1.at(0)+iTree.charge2.at(0))
        if iTree.J4Pt > 0:
            tmpHist7.Fill(4)
        elif iTree.J3Pt > 0:
            tmpHist7.Fill(3)
        else:
            tmpHist7.Fill(2)
        tmpHist_m1_s.Fill(iTree.m1.at(0))
        tmpHist_m2_s.Fill(iTree.m2.at(0))

    elif iTree.charge1.at(0) == - iTree.charge2.at(0):
        tmpHist3.Fill(iTree.pt1.at(0))
        tmpHist4.Fill(iTree.pt2.at(0))
        tmpHist3_eta.Fill(iTree.eta1.at(0))
        tmpHist4_eta.Fill(iTree.eta2.at(0))
        tmpHist_oc.Fill(iTree.charge1.at(0)+iTree.charge2.at(0))

    if iTree.J4Pt > 0:
        tmpHist8.Fill(4)
    elif iTree.J3Pt > 0:
        tmpHist8.Fill(3)
    else:
        tmpHist8.Fill(2)

    tmpHist_total1.Fill(iTree.pt1.at(0))
    tmpHist_total2.Fill(iTree.pt2.at(0))    
    tmpHist_eta_total1.Fill(iTree.eta1.at(0))
    tmpHist_eta_total2.Fill(iTree.eta2.at(0))  
    tmpHist_m1_t.Fill(iTree.m1.at(0))
    tmpHist_m2_t.Fill(iTree.m2.at(0))

print''

pEff1 = r.TEfficiency(tmpHist1, tmpHist_total1)
pEff2 = r.TEfficiency(tmpHist2, tmpHist_total2)
pEff3 = r.TEfficiency(tmpHist1_eta, tmpHist_eta_total1)
pEff4 = r.TEfficiency(tmpHist2_eta, tmpHist_eta_total2)
pEff5 = r.TEfficiency(tmpHist_m1_s, tmpHist_m1_t)
pEff6 = r.TEfficiency(tmpHist_m2_s, tmpHist_m2_t)

pEff_jetMult = r.TEfficiency(tmpHist7, tmpHist8)
# 
# for i in range(1,histRange2[0]+1):

#     tmpHist5_eta.SetBinContent(i, frac1)
#     tmpHist6_eta.SetBinContent(i, frac2)

c = r.TCanvas("c","Test", 800, 600)
ps = r.TPDF('%sPt_%s.pdf' %(psfile, title),112)
c.Divide(2,2)
c.cd(1)
r.gPad.SetLogy()
tmpHist3.SetTitle('%s tau1 pt; pt1; events' %(title))
tmpHist3.Draw()
tmpHist1.SetLineColor(r.kRed)
tmpHist1.Draw("same")
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=histList1)
l1.Draw("same")
c.Update()
c.cd(2)
r.gPad.SetLogy()
tmpHist4.SetTitle('%s tau2 pt; pt2; events' %(title))
tmpHist4.Draw("")
tmpHist2.SetLineColor(r.kRed)
tmpHist2.Draw("same")
l2 = tool.setMyLegend(lPosition=legendPosition, lHistList=histList2)
l2.Draw("same")
c.Update()
c.cd(3)
tmpHist5.SetTitle('tau1 same charge rate; pt1; SS/(SS+OS)')
tmpHist5.SetMaximum(1.0)
tmpHist5.SetMinimum(0.0)
tmpHist5.Draw()
pEff1.Draw('P same')
c.Update()
c.cd(4)
tmpHist6.SetMaximum(1.0)
tmpHist6.SetMinimum(0.0)
tmpHist6.SetTitle('tau2 same charge rate; pt2; SS/(SS+OS)')
tmpHist6.Draw()
pEff2.Draw('P same')
c.Update()
ps.Close()

c2 = r.TCanvas("c2","Test", 800, 600)
ps = r.TPDF('%sEta_%s.pdf' %(psfile, title),112)
c2.Divide(2,2)
c2.cd(1)
r.gPad.SetLogy()
tmpHist3_eta.SetTitle('%s tau1 eta; eta1; events' %(title))
tmpHist3_eta.SetMinimum(0.1)
tmpHist3_eta.Draw()
tmpHist1_eta.SetLineColor(r.kRed)
tmpHist1_eta.Draw("same")
l3 = tool.setMyLegend(lPosition=legendPosition, lHistList=histList3)
l3.Draw("same")
c2.Update()
c2.cd(2)
r.gPad.SetLogy()
tmpHist4_eta.SetTitle('%s tau2 eta; eta2; events' %(title))
tmpHist4_eta.SetMinimum(0.1)
tmpHist4_eta.Draw("")
tmpHist2_eta.SetLineColor(r.kRed)
tmpHist2_eta.Draw("same")
l4 = tool.setMyLegend(lPosition=legendPosition, lHistList=histList4)
l4.Draw("same")
c2.Update()
c2.cd(3)
tmpHist5_eta.SetTitle('tau1 same charge rate; eta1; SS/(SS+OS)')
tmpHist5_eta.SetMaximum(0.4)
tmpHist5_eta.SetMinimum(0.0)
tmpHist5_eta.Draw()
pEff3.Draw('P same')
c2.Update()
c2.cd(4)
tmpHist6_eta.SetTitle('tau2 same charge rate; eta2; SS/(SS+OS)')
tmpHist6_eta.SetMaximum(0.4)
tmpHist6_eta.SetMinimum(0.0)
tmpHist6_eta.Draw()
pEff4.Draw('P same')
c2.Update()
ps.Close()

c3 = r.TCanvas("c3","Test", 800, 600)
ps = r.TPDF('%sOther_%s.pdf' %(psfile, title),112)
c3.Divide(2,2)
c3.cd(1)
r.gPad.SetLogy()
tmpHist_oc.SetMinimum(0.5)
tmpHist_oc.SetTitle('diTau Charge; diTau charge; events')
tmpHist_oc.Draw()
tmpHist_sc.SetLineColor(r.kRed)
tmpHist_sc.Draw("same")
l5 = tool.setMyLegend(lPosition=legendPosition, lHistList=histList5)
l5.Draw("same")
c3.Update()
c3.cd(2)
pEff_jetMult.Draw("AP")
c3.Update()
c3.cd(3)
pEff5.Draw("AP")
c3.Update()
c3.cd(4)
pEff6.Draw("AP")
c3.Update()
ps.Close()

