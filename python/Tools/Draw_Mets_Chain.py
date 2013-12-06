#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os

psfile="Mets.eps"

Title = "MET info "

#Entries number in each sample
Htotal = 8361
ttTotal = 25553
ZZTotal = 5358

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******
HChain = r.TChain("ttTreeFinal/eventTree")
ttChain = r.TChain("ttTreeFinal/eventTree")
ZZChain = r.TChain("ttTreeFinal/eventTree")
tool.addFiles(HChain, "/hdfs/store/user/zmao/H2hh-SUB-TT", Htotal)
tool.addFiles(ttChain, "/hdfs/store/user/zmao/tt-SUB-TT", ttTotal)
tool.addFiles(ZZChain, "/hdfs/store/user/zmao/ZZ2-SUB-TT", ZZTotal)

met_signal = r.TH1F("met_signal"," ", 125, 0, 250)
met_tt = r.TH1F("met_tt"," ", 125, 0, 250)
met_ZZ = r.TH1F("met_ZZ"," ", 125, 0, 250)
metPhi_signal = r.TH1F("metPhi_signal"," ", 64, -3.2, 3.2)
metPhi_tt = r.TH1F("metPhi_tt"," ", 64, -3.2, 3.2)
metPhi_ZZ = r.TH1F("metPhi_ZZ"," ", 64, -3.2, 3.2)

met_signal_cut = r.TH1F("met_signal_cut"," ", 125, 0, 250)
met_tt_cut = r.TH1F("met_tt_cut"," ", 125, 0, 250)
met_ZZ_cut = r.TH1F("met_ZZ_cut"," ", 125, 0, 250)
metPhi_signal_cut = r.TH1F("metPhi_signal_cut"," ", 64, -3.2, 3.2)
metPhi_tt_cut = r.TH1F("metPhi_tt_cut"," ", 64, -3.2, 3.2)
metPhi_ZZ_cut = r.TH1F("metPhi_ZZ_cut"," ", 64, -3.2, 3.2)

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()

if not Htotal:
    print 'Getting nEntries in signal sample...'
    Htotal = HChain.GetEntriesFast()
print '%d entries in signal sample' %Htotal
for i in range(0, Htotal):
    HChain.GetEntry(i)
    tool.printProcessStatus(iCurrent=i, total=Htotal, processName = 'Looping signal sample')
#     for iMet in range(HChain.met.size()):
#         met_signal.Fill(HChain.met.at(iMet))
#     for iMetPhi in range(HChain.metPhi.size()):
#         metPhi_signal.Fill(HChain.metPhi.at(iMet))
    met_signal.Fill(HChain.met)
    metPhi_signal.Fill(HChain.metPhi)
    jetsList = [(HChain.J1CSVbtag, J1.SetCoordinates(HChain.J1Pt, HChain.J1Eta, HChain.J1Phi, HChain.J1Mass)),
                (HChain.J2CSVbtag, J2.SetCoordinates(HChain.J2Pt, HChain.J2Eta, HChain.J2Phi, HChain.J2Mass)),
                (HChain.J3CSVbtag, J3.SetCoordinates(HChain.J3Pt, HChain.J3Eta, HChain.J3Phi, HChain.J3Mass)),
                (HChain.J4CSVbtag, J4.SetCoordinates(HChain.J4Pt, HChain.J4Eta, HChain.J4Phi, HChain.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    if jetsList[0][0] > 0.679 and jetsList[1][0] > 0.244:
        met_signal_cut.Fill(HChain.met)
        metPhi_signal_cut.Fill(HChain.metPhi)
print ''
if not ttTotal:
    print "Getting nEntries in tt sample..."
    ttTotal = ttChain.GetEntriesFast()
print '%d entries in tt sample' %ttTotal
for i in range(0, ttTotal):
    ttChain.GetEntry(i)
    tool.printProcessStatus(iCurrent=i, total=ttTotal, processName = 'Looping tt sample')
#     for iMet in range(ttChain.met.size()):
#         met_tt.Fill(ttChain.met.at(iMet))
#     for iMetPhi in range(ttChain.metPhi.size()):
#         metPhi_tt.Fill(ttChain.metPhi.at(iMet))
    met_tt.Fill(ttChain.met)
    metPhi_tt.Fill(ttChain.metPhi)
    jetsList = [(ttChain.J1CSVbtag, J1.SetCoordinates(ttChain.J1Pt, ttChain.J1Eta, ttChain.J1Phi, ttChain.J1Mass)),
                (ttChain.J2CSVbtag, J2.SetCoordinates(ttChain.J2Pt, ttChain.J2Eta, ttChain.J2Phi, ttChain.J2Mass)),
                (ttChain.J3CSVbtag, J3.SetCoordinates(ttChain.J3Pt, ttChain.J3Eta, ttChain.J3Phi, ttChain.J3Mass)),
                (ttChain.J4CSVbtag, J4.SetCoordinates(ttChain.J4Pt, ttChain.J4Eta, ttChain.J4Phi, ttChain.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    if jetsList[0][0] > 0.679 and jetsList[1][0] > 0.244:
        met_tt_cut.Fill(ttChain.met)
        metPhi_tt_cut.Fill(ttChain.metPhi)
print ''
if not ZZTotal:
    print  'Getting nEntries in ZZ sample...'
    ZZTotal = ZZChain.GetEntriesFast()
print '%d entries in ZZ sample' %ZZTotal
for i in range(0, ZZTotal):
    ZZChain.GetEntry(i)
    tool.printProcessStatus(iCurrent=i, total=ZZTotal, processName = 'Looping ZZ sample')
#     for iMet in range(ZZChain.met.size()):
#         met_ZZ.Fill(ZZChain.met.at(iMet))
#     for iMetPhi in range(ZZChain.metPhi.size()):
#         metPhi_ZZ.Fill(ZZChain.metPhi.at(iMet))
    met_ZZ.Fill(ZZChain.met)
    metPhi_ZZ.Fill(ZZChain.metPhi)
    jetsList = [(ZZChain.J1CSVbtag, J1.SetCoordinates(ZZChain.J1Pt, ZZChain.J1Eta, ZZChain.J1Phi, ZZChain.J1Mass)),
                (ZZChain.J2CSVbtag, J2.SetCoordinates(ZZChain.J2Pt, ZZChain.J2Eta, ZZChain.J2Phi, ZZChain.J2Mass)),
                (ZZChain.J3CSVbtag, J3.SetCoordinates(ZZChain.J3Pt, ZZChain.J3Eta, ZZChain.J3Phi, ZZChain.J3Mass)),
                (ZZChain.J4CSVbtag, J4.SetCoordinates(ZZChain.J4Pt, ZZChain.J4Eta, ZZChain.J4Phi, ZZChain.J4Mass))
                ]
    jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)
    if jetsList[0][0] > 0.679 and jetsList[1][0] > 0.244:
        met_ZZ_cut.Fill(ZZChain.met)
        metPhi_ZZ_cut.Fill(ZZChain.metPhi)

print ''

histList = [met_signal, met_ZZ, met_tt, metPhi_signal, metPhi_ZZ, metPhi_tt,
            met_signal_cut, met_ZZ_cut, met_tt_cut, metPhi_signal_cut, metPhi_ZZ_cut, metPhi_tt_cut]
tool.unitNormHists(histList)

legendPosition = (0.58, 0.7, 0.88, 0.80)
l1 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l1.SetFillStyle(0)
l1.SetBorderSize(0)
l2 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l2.SetFillStyle(0)
l2.SetBorderSize(0)
l3 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l3.SetFillStyle(0)
l3.SetBorderSize(0)
l4 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l4.SetFillStyle(0)
l4.SetBorderSize(0)


met_ZZ.SetTitle("%s; met; Unit Normalized" % (Title))
met_ZZ.GetYaxis().SetTitleOffset(1.3)
metPhi_ZZ.SetTitle("%s; metPhi; Unit Normalized" % (Title))
metPhi_ZZ.GetYaxis().SetTitleOffset(1.3)
met_ZZ_cut.SetTitle("%s with 1 medium 1 loose b tag; met; Unit Normalized" % (Title))
met_ZZ_cut.GetYaxis().SetTitleOffset(1.3)
metPhi_ZZ_cut.SetTitle("%s with 1 medium 1 loose b tag; metPhi; Unit Normalized" % (Title))
metPhi_ZZ_cut.GetYaxis().SetTitleOffset(1.3)
c = r.TCanvas("c","Test", 800, 600)
r.gPad.SetTickx()
r.gPad.SetTicky()

psfile = os.environ['PYPATH']+'/Plots/'+psfile
ps = r.TPostScript(psfile,112)

l1.AddEntry(met_signal,"H->hh")
l1.AddEntry(met_ZZ,"ZZjets -> 2q2l")
l1.AddEntry(met_tt,"t#bar{t}")
l2.AddEntry(metPhi_signal,"H->hh")
l2.AddEntry(metPhi_ZZ,"ZZjets -> 2q2l")
l2.AddEntry(metPhi_tt,"t#bar{t}")
l3.AddEntry(met_signal_cut,"H->hh")
l3.AddEntry(met_ZZ_cut,"ZZjets -> 2q2l")
l3.AddEntry(met_tt_cut,"t#bar{t}")
l4.AddEntry(metPhi_signal_cut,"H->hh")
l4.AddEntry(metPhi_ZZ_cut,"ZZjets -> 2q2l")
l4.AddEntry(metPhi_tt_cut,"t#bar{t}")
met_ZZ.SetLineWidth(2)
met_signal.SetLineWidth(2)
met_tt.SetLineWidth(2)
met_ZZ.SetLineStyle(2)
met_ZZ.SetLineColor(1)
met_signal.SetFillStyle(3001)
met_signal.SetFillColor(4)
met_tt.SetFillStyle(3001)
met_tt.SetFillColor(2)
met_tt.SetLineColor(2)
metPhi_ZZ.SetLineWidth(2)
metPhi_signal.SetLineWidth(2)
metPhi_tt.SetLineWidth(2)
metPhi_ZZ.SetLineStyle(2)
metPhi_ZZ.SetLineColor(1)
metPhi_signal.SetFillStyle(3001)
metPhi_signal.SetFillColor(4)
metPhi_tt.SetFillStyle(3001)
metPhi_tt.SetFillColor(2)
metPhi_tt.SetLineColor(2)

met_ZZ_cut.SetLineWidth(2)
met_signal_cut.SetLineWidth(2)
met_tt_cut.SetLineWidth(2)
met_ZZ_cut.SetLineStyle(2)
met_ZZ_cut.SetLineColor(1)
met_signal_cut.SetFillStyle(3001)
met_signal_cut.SetFillColor(4)
met_tt_cut.SetFillStyle(3001)
met_tt_cut.SetFillColor(2)
met_tt_cut.SetLineColor(2)
metPhi_ZZ_cut.SetLineWidth(2)
metPhi_signal_cut.SetLineWidth(2)
metPhi_tt_cut.SetLineWidth(2)
metPhi_ZZ_cut.SetLineStyle(2)
metPhi_ZZ_cut.SetLineColor(1)
metPhi_signal_cut.SetFillStyle(3001)
metPhi_signal_cut.SetFillColor(4)
metPhi_tt_cut.SetFillStyle(3001)
metPhi_tt_cut.SetFillColor(2)
metPhi_tt_cut.SetLineColor(2)

c.Divide(2,2)
c.cd(1)
met_ZZ.Draw()
met_tt.Draw("same")
met_signal.Draw("same")
l1.Draw("same")

c.cd(2)
metPhi_ZZ.Draw()
metPhi_tt.Draw("same")
metPhi_signal.Draw("same")
l2.Draw("same")

c.cd(3)
met_ZZ_cut.Draw()
met_tt_cut.Draw("same")
met_signal_cut.Draw("same")
l3.Draw("same")

c.cd(4)
metPhi_ZZ_cut.Draw()
metPhi_tt_cut.Draw("same")
metPhi_signal_cut.Draw("same")
l4.Draw("same")

ps.Close()
