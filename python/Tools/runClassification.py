#!/user/bin/env python

import os as os

fileList = [# 'H2hh260',
#             'H2hh300',
#             'H2hh350',
#             'tt_eff',
#             'tt_semi_eff',
#             'ZZ_eff',
#             'DY1JetsToLL_eff2',
#             'DY2JetsToLL_eff2',
#             'DY3JetsToLL_eff2',
#             'W1JetsToLNu_eff2',
#             'W2JetsToLNu_eff2',
#             'W3JetsToLNu_eff2',
#             'WZJetsTo2L2Q_eff',
#             'dataTotal',
            'QCD_Pt-50to80',
            ]

location = '/scratch/zmao/relaxed_regression3/'

for iFile in fileList:
    rootCommand = "root -l -q  BJetRegressionApplication.C\(\\\"BDTG\\\",\\\"%s_all.root\\\",\\\"%s\\\"\)" %(iFile, location)
    os.system(rootCommand)    
    rootCommand = "root -l -q  TMVAClassificationApplication_new.C\(\\\"BDT\\\",\\\"TMVARegApp_%s_all.root\\\",\\\"EWK\\\",\\\"%s\\\"\)" %(iFile, location)
    os.system(rootCommand)
    rootCommand = "root -l -q  TMVAClassificationApplication_new.C\(\\\"BDT\\\",\\\"ClassApp_EWK_TMVARegApp_%s_all.root\\\",\\\"QCD\\\",\\\"%s\\\"\)" %(iFile, location)
    os.system(rootCommand)
    rootCommand = "root -l -q  TMVAClassificationApplication_new.C\(\\\"BDT\\\",\\\"ClassApp_QCD_ClassApp_EWK_TMVARegApp_%s_all.root\\\",\\\"both\\\",\\\"%s\\\"\)" %(iFile, location)
    os.system(rootCommand)
