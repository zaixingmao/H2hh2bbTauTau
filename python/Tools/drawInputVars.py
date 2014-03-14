#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool

r.gStyle.SetOptStat(0)


def setHistStyles(tmpHist1, tmpHist2, tmpHist3, tmpHist4):
    tmpHist1.SetLineWidth(2)
    tmpHist1.SetLineStyle(2)
    tmpHist1.SetLineColor(r.kBlue)

    tmpHist2.SetLineWidth(2)
    tmpHist2.SetLineStyle(2)
    tmpHist3.SetLineColor(r.kRed)

    tmpHist3.SetLineWidth(2)
    tmpHist3.SetLineColor(r.kBlue)
    tmpHist3.SetLineStyle(4)

    tmpHist4.SetLineWidth(2)
    tmpHist4.SetLineColor(r.kRed)
    tmpHist4.SetLineStyle(4)

#*******Open input file and find associated tree*******

tmpHist1 = r.TH1F()
tmpHist2 = r.TH1F()
tmpHist3 = r.TH1F()
tmpHist4 = r.TH1F()

varsList = ['svMass', 'dRTauTau', 'dRJJ', 'svPt', 'dRhh', 'pZ_M_pZV', 'met', 'mJJ', 'fMass']

trainMass = '300'

oldStatsList = {'260': 6039, '300': 4708, '350': 12597, 'ZZ': 3978, 'tt': 22182}
statsList = {'260': 920, '300': 1066, '350': 3885, 'ZZ': 905, 'tt': 6910}
statsList = {'260': 5843, '300': 4651, '350': 12485, 'ZZ': 3902, 'tt': 21840}

varRanges = {'svMass': [0,500], 'dRTauTau': [0, 5], 'dRJJ': [0, 5], 'svPt': [0,400], 'dRhh': [0, 6], 'pZ_M_pZV': [-200, 200],
             'met': [0, 200], 'mJJ': [0, 450], 'fMass': [0, 800]}


psfile="inputVars_%s.pdf" %(trainMass)

iFile_1 = r.TFile('/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/oldROOT/TMVA_H2hh%s_new.root' %(trainMass))
iFile_2 = r.TFile('/scratch/zmao/test_ptJet/TMVA%s_%s_new.root' %(trainMass, statsList[trainMass]))
iFile_3 = r.TFile('/scratch/zmao/test_pt/TMVA%s_%i_old.root' %(trainMass, statsList[trainMass]))

legendPosition = (0.6, 0.6, 0.85, 0.85)
#draw from the highest histogram
legendList = []

c = r.TCanvas("c","Test", 1000, 600)
ps = r.TPDF(psfile,112)
c.Divide(3,2)
for i in range(6):
    c.cd(i+1)
    tmpHist1 = iFile_2.Get("InputVariables_Id/%s__Signal_Id" %(varsList[i]))
    tmpHist2 = iFile_2.Get("InputVariables_Id/%s__Background_Id" %(varsList[i]))    
    tmpHist3 = iFile_1.Get("InputVariables_Id/%s__Signal_Id" %(varsList[i]))
    tmpHist4 = iFile_1.Get("InputVariables_Id/%s__Background_Id" %(varsList[i]))    

    tool.unitNormHists([tmpHist1, tmpHist2, tmpHist3, tmpHist4])
    tool.setDrawHists4(tmpHist3, tmpHist4, tmpHist1, tmpHist2)
    tmpHist1.SetTitle('%s; %s; Unit Normalized' %(varsList[i], varsList[i]))
    tmpHist2.SetTitle('%s; %s; Unit Normalized' %(varsList[i], varsList[i]))
    tmpHist3.SetTitle('%s; %s; Unit Normalized' %(varsList[i], varsList[i]))
    tmpHist4.SetTitle('%s; %s; Unit Normalized' %(varsList[i], varsList[i]))
    tmpHist1.GetXaxis().SetRangeUser(varRanges[varsList[i]][0],varRanges[varsList[i]][1])
    tmpHist2.GetXaxis().SetRangeUser(varRanges[varsList[i]][0],varRanges[varsList[i]][1])
    tmpHist3.GetXaxis().SetRangeUser(varRanges[varsList[i]][0],varRanges[varsList[i]][1])
    tmpHist4.GetXaxis().SetRangeUser(varRanges[varsList[i]][0],varRanges[varsList[i]][1])


    legendList.append(tool.setMyLegend(lPosition=legendPosition, lHistList = [(tmpHist1, '%s_pt45: Sig' %(trainMass)),
                                                                (tmpHist2, '%s_pt45: Bkg' %(trainMass)),
                                                                (tmpHist3, '%s_old:  Sig' %(trainMass)),
                                                                (tmpHist4, '%s_old:  Bkg' %(trainMass))]))
    legendList[i].Draw("same")
    c.Update()
ps.Close()

c2 = r.TCanvas("c2","Test", 1000, 600)
ps = r.TPDF('%s_2.pdf' %(psfile[0: psfile.rfind('.')]),112)
c2.Divide(3,2)
for i in range(6, len(varsList)):
    c2.cd(i%6 +1)
    tmpHist1 = iFile_2.Get("InputVariables_Id/%s__Signal_Id" %(varsList[i]))
    tmpHist2 = iFile_2.Get("InputVariables_Id/%s__Background_Id" %(varsList[i]))    
    tmpHist3 = iFile_1.Get("InputVariables_Id/%s__Signal_Id" %(varsList[i]))
    tmpHist4 = iFile_1.Get("InputVariables_Id/%s__Background_Id" %(varsList[i]))    

    tool.unitNormHists([tmpHist1, tmpHist2, tmpHist3, tmpHist4])

    tmpHist1.SetTitle('%s; %s; Unit Normalized' %(varsList[i], varsList[i]))
    tmpHist2.SetTitle('%s; %s; Unit Normalized' %(varsList[i], varsList[i]))
    tmpHist3.SetTitle('%s; %s; Unit Normalized' %(varsList[i], varsList[i]))
    tmpHist4.SetTitle('%s; %s; Unit Normalized' %(varsList[i], varsList[i]))
    tmpHist1.GetXaxis().SetRangeUser(varRanges[varsList[i]][0],varRanges[varsList[i]][1])
    tmpHist2.GetXaxis().SetRangeUser(varRanges[varsList[i]][0],varRanges[varsList[i]][1])
    tmpHist3.GetXaxis().SetRangeUser(varRanges[varsList[i]][0],varRanges[varsList[i]][1])
    tmpHist4.GetXaxis().SetRangeUser(varRanges[varsList[i]][0],varRanges[varsList[i]][1])
    tool.setDrawHists4(tmpHist3, tmpHist4, tmpHist1, tmpHist2)

    legendList.append(tool.setMyLegend(lPosition=legendPosition, lHistList = [(tmpHist1, '%s_pt45: Sig' %(trainMass)),
                                                                (tmpHist2, '%s_pt45: Bkg' %(trainMass)),
                                                                (tmpHist3, '%s_old:  Sig' %(trainMass)),
                                                                (tmpHist4, '%s_old:  Bkg' %(trainMass))]))
    legendList[i].Draw("same")
    c2.Update()
ps.Close()

