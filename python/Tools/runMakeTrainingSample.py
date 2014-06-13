#!/user/bin/env python

import os as os

fileList = [#'H2hh260',
#             'H2hh300',
#             'H2hh350',
            'tt_eff',
            'tt_semi_eff',
            'ZZ_eff',
            'DY2JetsToLL_eff',
            'DY3JetsToLL_eff',
            'W1JetsToLNu_eff',
            'W2JetsToLNu_eff',
            'W3JetsToLNu_eff',
#             'dataTotal',
            ]

location = '/scratch/zmao/relaxed_regression2/'

for iFile in fileList:
    rootCommand = "python ~/myScripts/H2hh2bbTauTau/python/Tools/makeTrainingSample.py --i %sTMVARegApp_%s_all.root --c tightoppositebTag --o %sTMVARegApp_%s_all" %(location, iFile, location, iFile)
    os.system(rootCommand)    

