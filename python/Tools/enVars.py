#!/usr/bin/env python

import ROOT as r
import os

#signalLocation = "/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/sig"
#ttLocation = "/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/tt"
#ZZLocation = "/Users/zmao/M-Data/School/Brown/Work/Analysis/H->TauTau/MC/zz"

signalEntries = 0
ttEntries = 0
ZZEntries = 0
# 
# signalEntries = 8361
#ttEntries = 25633
#ZZEntries = 5358

signalLocation = "/hdfs/store/user/zmao/H2hh2-SUB-TT"
ttLocation = "/hdfs/store/user/zmao/tt_3-SUB-TT"
ZZLocation = "/hdfs/store/user/zmao/ZZ_3-SUB-TT"

signal1Location = "/hdfs/store/user/zmao/H2hh260_3-SUB-TT"
signal2Location = "/hdfs/store/user/zmao/H2hh300_3-SUB-TT"
signal3Location = "/hdfs/store/user/zmao/H2hh350_3-SUB-TT"

sampleLocations = [
#                     ("H2hh260",  "/hdfs/store/user/zmao/H2hh260_newMET-SUB-TT"), 
#                     ("H2hh300",  "/hdfs/store/user/zmao/H2hh300_newMET-SUB-TT"),
#                     ("H2hh350",  "/hdfs/store/user/zmao/H2hh350_newMET-SUB-TT"),
#                     ("tt_eff", "/hdfs/store/user/zmao/tt_newMET-SUB-TT"),
#                     ("ZZ_eff", "/hdfs/store/user/zmao/ZZ_newMET-SUB-TT"),
#                     ("tt_semi_eff", "/hdfs/store/user/zmao/tt_SemiLep_newMET-SUB-TT"),
#                     ('QCD_Pt-30to50', '/hdfs/store/user/zmao/QCD_Pt-30to50_newMET-SUB-TT'),
#                     ('QCD_Pt-50to80', '/hdfs/store/user/zmao/QCD_Pt-50to80_newMET-SUB-TT'),
#                     ('QCD_Pt-80to120', '/hdfs/store/user/zmao/QCD_Pt-80to120_newMET-SUB-TT'),
#                     ('QCD-120to170', '/hdfs/store/user/zmao/QCD_Pt-120to170_newMET-SUB-TT'),
#                     ('QCD_Pt-30To50_bEnriched', '/hdfs/store/user/zmao/QCD_Pt-30To50_bEnriched_newMET-SUB-TT'),
#                     ('QCD_Pt-50To150_bEnriched', '/hdfs/store/user/zmao/QCD_Pt-50To150_bEnriched_newMET-SUB-TT'),
#                     ('QCD_Pt-150_bEnriched', '/hdfs/store/user/zmao/QCD_Pt-150_bEnriched_newMET-SUB-TT'),
#                     ('dataA', '/hdfs/store/user/zmao/Tau_Run2012A_newMET2-SUB-TT-data/'),
#                     ('dataB', '/hdfs/store/user/zmao/TauParked_Run2012B_newMET2-SUB-TT-data/'),
#                     ('dataC', '/hdfs/store/user/zmao/TauParked_Run2012C_newMET3-SUB-TT-data/'),
#                     ('dataD', '/hdfs/store/user/zmao/TauParked_Run2012D_newMET3-SUB-TT-data/'),
#                     ('dataTotal', '/scratch/zmao/relaxed_regression4/data' ),
#                     ('QCDtotal', '/scratch/zmao/QCD/qcd' ),
#                     ('QCDtotal_bEnriched', '/scratch/zmao/QCD/bEnriched' ),
#                     ('DYJetsToLL_eff', '/hdfs/store/user/zmao/DYJetsToLL_newMET-SUB-TT'),
#                     ('DY1JetsToLL_eff2', '/hdfs/store/user/zmao/DY1JetsToLL_newMET2-SUB-TT'),
#                     ('DY2JetsToLL_eff2', '/hdfs/store/user/zmao/DY2JetsToLL_newMET2-SUB-TT'),
#                     ('DY3JetsToLL_eff2', '/hdfs/store/user/zmao/DY3JetsToLL_newMET2-SUB-TT'),
#                     ('W1JetsToLNu_eff2', '/hdfs/store/user/zmao/W1JetsToLNu_newMET2-SUB-TT'),
#                     ('W2JetsToLNu_eff2', '/hdfs/store/user/zmao/W2JetsToLNu_newMET-SUB-TT'),
#                     ('W3JetsToLNu_eff2', '/hdfs/store/user/zmao/W3JetsToLNu_newMET-SUB-TT'),
#                     ('WZJetsTo2L2Q_eff', '/hdfs/store/user/zmao/WZJetsTo2L2Q_newMET-SUB-TT'),
#                     ('H2hh300', '/hdfs/store/user/zmao/H2hh300_pt20WithInit-SUB-TT'),
#                       ('VBF_HToTauTau', '/hdfs/store/user/zmao/VBF_HToTauTau-SUB-TT'),
#                       ('TTJets_MSDecays', '/hdfs/store/user/zmao/TTJets_MSDecays-SUB-TT'),
#                       ('GluGluToHToTauTau', '/hdfs/store/user/zmao/GluGluToHToTauTau-SUB-TT'),
#                       ('WH_ZH_TTH_HToTauTau', '/hdfs/store/user/zmao/WH_ZH_TTH_HToTauTau-SUB-TT'),
#                     ("H2hh300",  "/hdfs/store/user/zmao/H2hh300_syncNew-SUB-TT"),
                    ("H2hh300_newTauID", "/hdfs/store/user/zmao/H2hh300_newTauID-SUB-TT"),
                  ]


vecVarList = ['pt1', 'pt2', 'iso1', 'iso2', 'eta1', 'eta2', 'phi1', 'phi2', 'svEta', 'svMass', 'svPhi', 'svPt']

corruptedROOTfiles = ["/hdfs/store/user/zmao/H2hh260_7-SUB-TT/SUB-TT-patTuple_cfg-1C0253DE-53FA-E211-8D12-003048D4DEBC.root", 
                      "/hdfs/store/user/zmao/H2hh260_7-SUB-TT/SUB-TT-patTuple_cfg-9073B1D0-59FA-E211-BFBF-0025904B144A.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-0E9D378A-2A98-E211-A1F6-002590593876.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-185E02AB-4198-E211-BD58-003048FFCBFC.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-1E08CA64-6A98-E211-811E-00261894388A.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-1E311D72-2298-E211-8A84-003048678F62.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-22C3CAA7-6C98-E211-B172-0030486792AC.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-287852CD-6398-E211-AFB1-003048FFCC2C.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-322931B8-7A98-E211-B6B9-0018F3D09630.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-3A181C8B-4D98-E211-9389-003048FFD732.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-3A850CE0-EB97-E211-A48C-00304867901A.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-3E45F8EB-6698-E211-9D04-00261894392D.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-3ECDD821-1498-E211-BAB2-003048678B94.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-5A135027-F898-E211-9EB8-003048FFD7A2.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-68DC730E-0898-E211-917F-002618943956.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-7AAC11A4-4798-E211-BFE6-00248C55CC97.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-964E2674-4098-E211-808B-00261894391B.root",
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-9667B6CA-F998-E211-9BF3-0025905938D4.root", 
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-9A1D201D-0C98-E211-A802-003048678B86.root", 
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-9AC11D94-2598-E211-B1B7-00304867BF18.root", 
                      "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-9CFCCF4E-4E98-E211-A56C-003048FFCBFC.root", 
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-9E4ECC6A-0F98-E211-986B-003048678BE8.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-B4B890D6-2C98-E211-AA2B-003048FFD71E.root", 
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-BEC26106-5998-E211-8ABD-00261894397D.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-BEDE641A-0898-E211-9A15-002618943896.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-C233E89D-3998-E211-B04A-0025905822B6.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-CE14903D-2898-E211-A6E0-002590596468.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-CE1ECA47-F397-E211-86F2-002354EF3BDD.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-D69FD5D4-EA97-E211-85C2-003048678C26.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-DEDC8769-0998-E211-8BF5-002590596486.root", 
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-E0AEF6C8-5C98-E211-A131-002618943925.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-EEDE625E-4598-E211-B87E-0026189438FD.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-F4F4E3CF-E098-E211-B188-0025905964BA.root", 
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-F6AF9835-EC97-E211-9E37-002354EF3BE3.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-FA2576A2-2298-E211-959B-0026189438A5.root", 
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-FACE05A2-6298-E211-A94E-003048678E24.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-FC72D211-1298-E211-BA92-00261894390B.root",
                    "/hdfs/store/user/zmao/tt_7-SUB-TT/SUB-TT-patTuple_cfg-FE60B8DD-1598-E211-AB86-002618943970.root",
                    "/hdfs/store/user/zmao/ZZ_7-SUB-TT/SUB-TT-patTuple_cfg-36C44C65-15D8-E111-91CE-00215E221794.root",
                    "/hdfs/store/user/zmao/ZZ_7-SUB-TT/SUB-TT-patTuple_cfg-46DC8639-75D8-E111-BA85-E41F131817F8.root",
                    "/hdfs/store/user/zmao/ZZ_7-SUB-TT/SUB-TT-patTuple_cfg-64FD3891-6DD8-E111-A6A0-E41F13181590.root",
                    "/hdfs/store/user/zmao/ZZ_7-SUB-TT/SUB-TT-patTuple_cfg-6C916E94-39D8-E111-A134-001A645C1DEC.root",
                    "/hdfs/store/user/zmao/ZZ_7-SUB-TT/SUB-TT-patTuple_cfg-B42335F9-78D9-E111-9D78-00215E221680.root"]
