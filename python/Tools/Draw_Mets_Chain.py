#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import os
import enVars

psfile="Mets.eps"
Title = "MET info "

#Entries number in each sample
signalEntries = enVars.signalEntries
ttEntries = enVars.ttEntries
ZZEntries = enVars.ZZEntries
signalLocation = enVars.signalLocation
ttLocation = enVars.ttLocation
ZZLocation = enVars.ZZLocation

r.gStyle.SetOptStat(0)

#*******Open input file and find associated tree*******
HChain = r.TChain("ttTreeFinal/eventTree")
ttChain = r.TChain("ttTreeFinal/eventTree")
ZZChain = r.TChain("ttTreeFinal/eventTree")
tool.addFiles(HChain, signalLocation, signalEntries)
tool.addFiles(ttChain, ttLocation, ttEntries)
tool.addFiles(ZZChain, ZZLocation, ZZEntries)

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

#for normalization
HistNameList = [met_signal, met_tt, met_ZZ, metPhi_signal, metPhi_tt, metPhi_ZZ, met_signal_cut, met_tt_cut, met_ZZ_cut,
                metPhi_signal_cut, metPhi_tt_cut, metPhi_ZZ_cut]

ChainHistList = [(HChain, signalLocation, signalEntries, met_signal, metPhi_signal, met_signal_cut, metPhi_signal_cut),
                 (ttChain, ttLocation, ttEntries, met_tt, metPhi_tt, met_tt_cut, metPhi_tt_cut),
                 (ZZChain, ZZLocation, ZZEntries, met_ZZ, metPhi_ZZ, met_ZZ_cut, metPhi_ZZ_cut)]

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
J1 = lvClass()
J2 = lvClass()
J3 = lvClass()
J4 = lvClass()

for iChain, iLocation, iEntries, iHist_met, iHist_phi, iHist_met_cut, iHist_phi_cut in ChainHistList:
    total = iEntries if iEntries else iChain.GetEntriesFast()
    key =  "found" if not iEntries else "has"
    print "[%s] %s %d events" %(iLocation, key, total)
    for i in range(0, total):
        iChain.GetEntry(i)
        tool.printProcessStatus(iCurrent=i, total=total, processName = 'Looping sample')
        jetsList = [(iChain.J1CSVbtag, J1.SetCoordinates(iChain.J1Pt, iChain.J1Eta, iChain.J1Phi, iChain.J1Mass)),
            (iChain.J2CSVbtag, J2.SetCoordinates(iChain.J2Pt, iChain.J2Eta, iChain.J2Phi, iChain.J2Mass)),
            (iChain.J3CSVbtag, J3.SetCoordinates(iChain.J3Pt, iChain.J3Eta, iChain.J3Phi, iChain.J3Mass)),
            (iChain.J4CSVbtag, J4.SetCoordinates(iChain.J4Pt, iChain.J4Eta, iChain.J4Phi, iChain.J4Mass))]
        jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)

        for iMet in range(iChain.met.size()):
            iHist_met.Fill(iChain.met.at(iMet))
            if jetsList[0][0] > 0.679 and jetsList[1][0] > 0.244:
                iHist_met_cut.Fill(iChain.met.at(iMet))    
        for iMetPhi in range(iChain.metPhi.size()):
            iHist_phi.Fill(iChain.metPhi.at(iMet))
            if jetsList[0][0] > 0.679 and jetsList[1][0] > 0.244:
                iHist_phi_cut.Fill(iChain.metPhi.at(iMet))
    print ''

tool.unitNormHists(HistNameList)

legendHist1 = [(met_signal,"H->hh"), (met_ZZ,"ZZjets -> 2q2l"), (met_tt,"t#bar{t}")]
legendHist2 = [(metPhi_signal,"H->hh"), (metPhi_ZZ,"ZZjets -> 2q2l"), (metPhi_tt,"t#bar{t}")]
legendHist3 = [(met_signal_cut,"H->hh"), (met_ZZ_cut,"ZZjets -> 2q2l"), (met_tt_cut,"t#bar{t}")]
legendHist4 = [(metPhi_signal_cut,"H->hh"), (metPhi_ZZ_cut,"ZZjets -> 2q2l"), (metPhi_tt_cut,"t#bar{t}")]
legendPosition = (0.58, 0.7, 0.88, 0.80)

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

c.Divide(2,2)
c.cd(1)
tool.setDrawHists(sigHist=met_signal, ttHist=met_tt, ZZHist=met_ZZ)
l1 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHist1)
l1.Draw("same")

c.cd(2)
tool.setDrawHists(sigHist=metPhi_signal, ttHist=metPhi_tt, ZZHist=metPhi_ZZ)
l2 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHist2)
l2.Draw("same")

c.cd(3)
tool.setDrawHists(sigHist=met_signal_cut, ttHist=met_tt_cut, ZZHist=met_ZZ_cut)
l3 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHist3)
l3.Draw("same")

c.cd(4)
tool.setDrawHists(sigHist=metPhi_signal_cut, ttHist=metPhi_tt_cut, ZZHist=metPhi_ZZ_cut)
l4 = tool.setMyLegend(lPosition=legendPosition, lHistList=legendHist4)
l4.Draw("same")

ps.Close()
print "Plot saved at %s" %(psfile)