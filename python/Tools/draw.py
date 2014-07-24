#!/usr/bin/env python

import varsList
import os
import ROOT as r
import drawVarsData_new2

#getHistos(varName, signalSelection, logY, sigBoost, nbins, useData, max, rangeMin, rangeMax, location):
region = 'LL'

for varName, varConfig in varsList.varsRange.items():
#    output = 'python  ~/myScripts/H2hh2bbTauTau/python/Tools/compareIso.py --location /scratch/zmao/relaxed_regression2/plots  --signal H350'
#     output = 'python  ~/myScripts/H2hh2bbTauTau/python/Tools/drawVarsData_Xsquare.py --location /scratch/zmao/relaxed_regression3/XS_%s_fix  --signal H350' %region
#     output = 'python  ~/myScripts/H2hh2bbTauTau/python/Tools/drawVarsData_KS.py --location /scratch/zmao/relaxed_regression3/new2_%s  --signal H350' %region
    output = 'python  ~/myScripts/H2hh2bbTauTau/python/Tools/drawVarsData_KS_CheckFlat.py --location /scratch/zmao/relaxed_regression3/new2_%s  --signal H350' %region

#     output = 'python  ~/myScripts/H2hh2bbTauTau/python/Tools/drawVarsData_new2.py --location /scratch/zmao/relaxed_regression3/test_qcd  --signal H350'

#     output = 'python  ~/myScripts/H2hh2bbTauTau/python/Tools/drawVarsData_new9.py --location /scratch/zmao/relaxed_regression2/plots  --signal H350'
    output += ' --variable %s --nbins %i --setRangeMin %f --setRangeMax %f' %(varName, varConfig[0], varConfig[1], varConfig[2])
    output += ' --setMax %i' %varConfig[3]
    output += ' --sigBoost %i' %varConfig[4]
    output += ' --logY %s' %varConfig[5]
    output += ' --bTag True'
    output += ' --predict %s' %varConfig[6]
    output += ' --useData True'
    output += ' --region %s' %region
#     output += ' --unit %s' %varConfig[7]

    os.system(output)
#drawVarsData_new2.getHistos('dPhiMetTauPair', 'H300', True, 20, 11, 'True', 100, 0, 3.3, '/scratch/zmao/relaxed/plots')
