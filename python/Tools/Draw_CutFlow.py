#!/usr/bin/env python

import ROOT as r
import tool
from operator import itemgetter

psfile="/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/Plots/CutFlow.eps"

r.gStyle.SetOptStat(0)

Z_xs = 2.502 * 1000.
h_xs = 15.8991453481
tt_xs =  3110.90625

#*******Open input file and find associated tree*******
ifile_sig = r.TFile("/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/analysis_signal.root")
ifile_tt = r.TFile("/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/analysis_tt.root")
ifile_zz = r.TFile("/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/analysis_zz.root")

CutFlow_sig = r.TH1F("CutFlow_sig"," ", 15, 0, 14)
CutFlow_tt = r.TH1F("CutFlow_tt"," ", 15, 0, 14)
CutFlow_zz = r.TH1F("CutFlow_zz"," ", 15, 0, 14)

CutFlow_sig = ifile_sig.Get("TT/results")
CutFlow_tt = ifile_tt.Get("TT/results")
CutFlow_zz = ifile_zz.Get("TT/results")

CutFlow_sig.SetTitle("Cut Flow;;")
CutFlow_tt.SetTitle("Cut Flow;;Events/bin/20 fb^{-1}")
CutFlow_tt.GetYaxis().SetTitleOffset(1.2)

legendPosition = (0.65, 0.7, 1, 0.85)
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


c = r.TCanvas("c","Test", 800, 600)
c.Divide(2,2)
ps = r.TPostScript(psfile,112)

c.cd(1)
r.gPad.SetLogy()
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
r.gPad.SetLogy()
CutFlow_sig.GetXaxis().SetRange(0,15)
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