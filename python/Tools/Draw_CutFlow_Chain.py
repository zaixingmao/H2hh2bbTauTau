#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter
import enVars
import os

psfile="CutFlow.eps"

r.gStyle.SetOptStat(0)

Z_xs = 2.502 * 1000.
h_xs = 15.8991453481
tt_xs =  26197.5 #3110.90625

Title = "Require "

signalEntries = enVars.signalEntries
ttEntries = enVars.ttEntries
ZZEntries = enVars.ZZEntries
signalLocation = enVars.signalLocation
ttLocation = enVars.ttLocation
ZZLocation = enVars.ZZLocation

#*******Open input file and find associated tree*******


CutFlow_sig = r.TH1F()
CutFlow_tt = r.TH1F()
CutFlow_zz = r.TH1F()
xLabels = ['processedEvents', 'PATSkimmedEvents', 'atLeastOneDiTau',
           'ptEta1', 'ptEta2', 'Os', 'tau1Hadronic', 'tau2Hadronic',
           'muonVeto1', 'muonVeto2', 'eleVeto1', 'eleVeto2',
           'isolation1', 'isolation2', 'final']

tool.addHistFromFiles(dirName = signalLocation, histName = "TT/results", hist = CutFlow_sig, xAxisLabels=xLabels)
tool.addHistFromFiles(dirName = ttLocation, histName = "TT/results", hist = CutFlow_tt, xAxisLabels=xLabels)
tool.addHistFromFiles(dirName = ZZLocation, histName = "TT/results", hist = CutFlow_zz, xAxisLabels=xLabels)


CutFlow_sig.SetTitle("Cut Flow;;")
CutFlow_tt.SetTitle("Cut Flow;;Events/bin/20 fb^{-1}")
CutFlow_tt.GetYaxis().SetTitleOffset(1.2)

legendPosition = (0.75, 0.73, 1, 0.88)
l1 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l1.SetFillStyle(0)
l1.SetBorderSize(0)
l1.AddEntry(CutFlow_sig, "H->hh")
l1.AddEntry(CutFlow_tt, "tt")
l1.AddEntry(CutFlow_zz, "ZZ")
l2 = r.TLegend(legendPosition[0], legendPosition[1], legendPosition[2], legendPosition[3])
l2.SetFillStyle(0)
l2.SetBorderSize(0)

CutFlow_sig.SetLineColor(4)
CutFlow_sig.SetLineWidth(2)
CutFlow_tt.SetLineColor(2)
CutFlow_tt.SetLineWidth(2)
CutFlow_zz.SetLineColor(1)
CutFlow_zz.SetLineWidth(2)
CutFlow_zz.SetLineStyle(2)

Scale_sig = CutFlow_sig.GetBinContent(1)
CutFlow_sig.Scale(1/Scale_sig)
Scale_tt = CutFlow_tt.GetBinContent(1)
CutFlow_tt.Scale(1/Scale_tt)
Scale_zz = CutFlow_zz.GetBinContent(1)
CutFlow_zz.Scale(1/Scale_zz)

psfile = os.environ['PYPATH']+'/Plots/'+psfile
c = r.TCanvas("c","Test", 800, 600)
c.Divide(2,2)
ps = r.TPostScript(psfile,112)

c.cd(1)
CutFlow_sig.GetXaxis().SetRange(0,15)
r.gPad.SetTickx()
r.gPad.SetTicky()
r.gPad.SetLogy()
CutFlow_sig.SetMinimum(0.001)
CutFlow_sig.Draw()
CutFlow_tt.Draw("same")
CutFlow_zz.Draw("same")
l1.Draw("same")
c.Update()

c.cd(3)
CutFlow_sig.SetTitle("Cut Flow (Close);;")
r.gPad.SetLogy()
CutFlow_sig.GetXaxis().SetRange(12,15)
CutFlow_sig.SetMinimum(0.004)
CutFlow_sig.Draw()
CutFlow_tt.Draw("same")
CutFlow_zz.Draw("same")
l1.Draw("same")
c.Update()

CutFlow_sig.Scale(h_xs*20)
CutFlow_tt.Scale(tt_xs*20)
CutFlow_zz.Scale(Z_xs*20)

c.cd(2)
CutFlow_tt.GetXaxis().SetRange(0,14)
r.gPad.SetTickx()
r.gPad.SetTicky()
r.gPad.SetLogy()
CutFlow_sig.GetXaxis().SetRange(0,15)
CutFlow_tt.SetMinimum(1)
CutFlow_tt.Draw()
CutFlow_sig.Draw("same")
CutFlow_zz.Draw("same")
l1.Draw("same")
c.Update()

c.cd(4)
CutFlow_tt.SetTitle("Cut Flow (Close);;Events/bin/20 fb^{-1}")
r.gPad.SetLogy()
CutFlow_tt.GetXaxis().SetRange(12,15)
CutFlow_tt.SetMinimum(10)
CutFlow_tt.Draw()
CutFlow_sig.Draw("same")
CutFlow_zz.Draw("same")
l1.Draw("same")

ps.Close()
print "Plot saved at %s" %(psfile)