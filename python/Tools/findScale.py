#!/usr/bin/env python

import os
import ROOT as r
import optparse

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--region", dest="region", default = 'LL', help="")
    options, args = parser.parse_args()
    return options

op = opts()

varConfig = [20, 0, 400, 10000, 100, True, True]

region = op.region

for i in [1, 2]:
    if region == 'LL':
        output = 'python  ~/myScripts/H2hh2bbTauTau/python/Tools/findTauPtScale_new.py --location /scratch/zmao/relaxed_regression3/%s_new  --signal H350' %region
    else:
        output = 'python  ~/myScripts/H2hh2bbTauTau/python/Tools/findTauPtScale.py --location /scratch/zmao/relaxed_regression3/%s_new  --signal H350' %region
    output += ' --variable tauPt --nbins %i --setRangeMin %f --setRangeMax %f' %(varConfig[0], varConfig[1], varConfig[2])
    output += ' --setMax %i' %varConfig[3]
    output += ' --sigBoost %i' %varConfig[4]
    output += ' --logY %s' %varConfig[5]
    output += ' --bTag True'
    output += ' --predict %s' %varConfig[6]
    output += ' --scale %i' %i
    output += ' --region %s' %region
    os.system(output)
