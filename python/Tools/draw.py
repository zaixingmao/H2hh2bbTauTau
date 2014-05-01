#!/usr/bin/env python

import varsList
import os
import ROOT as r
import drawVarsData_new2

#getHistos(varName, signalSelection, logY, sigBoost, nbins, useData, max, rangeMin, rangeMax, location):


for varName, varConfig in varsList.varsRange.items():
    output = 'python  ~/myScripts/H2hh2bbTauTau/python/Tools/drawVarsData_new.py --location /scratch/zmao/relaxed_regression/plots  --signal H260'
    output += ' --variable %s --nbins %i --setRangeMin %f --setRangeMax %f' %(varName, varConfig[0], varConfig[1], varConfig[2])
    output += ' --setMax %i' %varConfig[3]
    output += ' --sigBoost %i' %varConfig[4]
    output += ' --logY %s' %varConfig[5]
    output += ' --bTag True'
    output += ' --predict False'
    os.system(output)
#drawVarsData_new2.getHistos('dPhiMetTauPair', 'H300', True, 20, 11, 'True', 100, 0, 3.3, '/scratch/zmao/relaxed/plots')
