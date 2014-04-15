#!/usr/bin/env python

import sys
import os

import ROOT 
from ROOT import TFile
from ROOT import *

from array import array

from math import sqrt
from copy import copy

#from printcolor import printc

lumi = 20
#lumi = 5100
nbins = 25

def FOM(S,B):

    if B > 0:    
        return ( S / ( 1.5 + sqrt(B) + 0.2*B )  )
    else:
        return 0


def getScale(Type,nEVT):

    xsec = {}
    Nevents = {}

    xsec['tt_fLep'] = 26.1975*1000
    xsec['tt_sLep'] = 109.281*1000
    xsec['ZZ'] = 2.502*1000
    xsec['H260'] = 14.76 #fb
    xsec['H300'] = 179.92 #fb
    xsec['H350'] = 97.73 #fb

    print nEVT
    return lumi*xsec[Type]/nEVT


def getHisto(_file, _name, _cut=-1.0):

    input = TFile.Open(_file)
    h = input.Get("preselection")
    nEVT=int(h.GetBinContent(1))
    hist = input.Get("MVA_BDT")
    hist.GetXaxis().SetRangeUser(_cut,1.0)
    hist.Sumw2()
    hist.Scale(getScale(_name,nEVT))
    hist.SetName(_name)

    print "%s\033[1;32m\t integral = %s\033[1;m"%(_name, hist.Integral())
    #printc('green','', "\t"+_type+" integral = %s"%hist.Integral())  
    return hist

def getDataHisto(_file, _cut=-1.0):
    input = TFile.Open(_file)
    data_obs = TH1F('data_obs', 'data_obs', nbins, _cut, 1)
    data_obs.Sumw2()
    data_obs.SetName('data_obs')
    data_obs = input.Get("MVA_BDT")
    data_obs.GetXaxis().SetRangeUser(_cut,1.0)
    data_obs.Scale(0.001)

    print "data_obs\033[1;32m\t integral = %s\033[1;m"%data_obs.Integral()
    return data_obs

cut = 0.4

histSig = getHisto(_file='/scratch/zmao/test_cutflow/TMVApp_H2hh260_all.root', _name = 'H260', _cut = cut)
histZZ = getHisto(_file='/scratch/zmao/test_cutflow/TMVApp_ZZ_all.root', _name = 'ZZ', _cut = cut) 
histtt = getHisto(_file='/scratch/zmao/test_cutflow/TMVApp_tt_all.root', _name = 'tt_fLep', _cut = cut)
histData = getDataHisto(_file='/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/TMVApp_H260_test.root', _cut = cut)
        
#background = histSig.Integral()+histWjetsLF.Integral()+histWjetsHF.Integral()+histZjetsLF.Integral()+0+histZjetsHF.Integral()+histTTbar.Integral()+histT_s.Integral()+histWW.Integral()
background = histZZ.Integral()+histtt.Integral()

print "\033[1;32m\tTotal background integral = %s\033[1;m"%background
print "\033[1;32m\tData / MC = %s\033[1;m"%(histData.Integral()/background)
print '\033[1;32m\tFOM = %s\033[1;m'%(round(FOM(histSig.Integral(),background),5))



#write DATAcard:
bin = 'H2hh2tauhtauh'

print 'Writing to file: test_dataCard.txt'

f = open('test_dataCard.txt','w')
f.write('imax\t1\tnumber of channels\n')
f.write('jmax\t2\tnumber of backgrounds (\'*\' = automatic)\n')
f.write('kmax\t*\tnumber of nuisance parameters (sources of systematical uncertainties)\n\n')
#f.write('shapes * * %s.root $CHANNEL:$PROCESS $CHANNEL:$PROCESS$SYSTEMATIC\n\n'%ROOToutname)
f.write('bin\t%s\n\n'%bin)
f.write('observation\t%s\n\n'%histData.Integral())
f.write('bin\t%s\t%s\t%s\n'%(bin,bin,bin))
f.write('process\tVH\ttt\tZZ\n')
f.write('process\t0\t1\t2\n')
f.write('rate\t%s\t%s\t%s\n'%(histSig.Integral(), histZZ.Integral(), histtt.Integral())) 
f.write('lumi\tlnN\t1.05\t-\t-\n')

    #SYST
    # f.write('CMS_SCALE\tlnN\t1.03\t1.03\t1.03\t1.03\t-\t1.03\t1.03\t1.03\t1.03\t-\n')
#     f.write('CMS_RES\tlnN\t1.06\t1.06\t1.06\t1.06\t-\t1.06\t1.06\t1.06\t1.06\t-\n')
#     f.write('CMS_beff\tlnN\t1.075\t1.075\t1.075\t1.075\t-\t1.075\t1.075\t1.075\t1.075\t-\n')
#     f.write('CMS_bmis\tlnN\t1.10\t1.10\t1.10\t1.10\t-\t1.10\t1.10\t1.10\t1.10\t-\n')

f.close()
    




