#!/user/bin/env python

import os as os

fileList = ['H2hh260',
            'H2hh300',
            'H2hh350',
            'tt_eff',
            'tt_semi_eff',
            'ZZ_eff',
            'DY2JetsToLL_eff',
            'DY3JetsToLL_eff',
            'W1JetsToLNu_eff',
            'W2JetsToLNu_eff',
            'W3JetsToLNu_eff',
            'dataTotal',
            ]

location = '/scratch/zmao/BDT_16/'

for iFile in fileList:
#     rootCommand = "root -l -q  BJetRegressionApplication.C\(\\\"BDTG\\\",\\\"%s_all.root\\\",\\\"%s\\\"\)" %(iFile, location)
#     os.system(rootCommand)    
    rootCommand = "root -l -q  TMVAClassificationApplication_new.C\(\\\"BDT\\\",\\\"TMVARegApp_%s_all.root\\\",\\\"EWK\\\",\\\"%s\\\"\)" %(iFile, location)
    os.system(rootCommand)
    rootCommand = "root -l -q  TMVAClassificationApplication_new.C\(\\\"BDT\\\",\\\"ClassApp_EWK_TMVARegApp_%s_all.root\\\",\\\"QCD\\\",\\\"%s\\\"\)" %(iFile, location)
    os.system(rootCommand)
    rootCommand = "root -l -q  TMVAClassificationApplication_new.C\(\\\"BDT\\\",\\\"ClassApp_QCD_ClassApp_EWK_TMVARegApp_%s_all.root\\\",\\\"both\\\",\\\"%s\\\"\)" %(iFile, location)
    os.system(rootCommand)
