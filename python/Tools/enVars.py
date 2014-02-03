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

signalLocation = "/hdfs/store/user/zmao/H2hh260-SUB-TT"
signalLocation = "/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_7/src/UWAnalysis/CRAB/LTau"
ttLocation = "/hdfs/store/user/zmao/tt_3-SUB-TT"
ZZLocation = "/hdfs/store/user/zmao/ZZ_3-SUB-TT"

signal1Location = "/hdfs/store/user/zmao/H2hh260_3-SUB-TT"
signal2Location = "/hdfs/store/user/zmao/H2hh300_3-SUB-TT"
signal3Location = "/hdfs/store/user/zmao/H2hh350_3-SUB-TT"

sampleLocations = [("H2hh260",  "/hdfs/store/user/zmao/H2hh260_3-SUB-TT"),
                   ("H2hh300",  "/hdfs/store/user/zmao/H2hh300_3-SUB-TT"),
                   ("H2hh350",  "/hdfs/store/user/zmao/H2hh350_3-SUB-TT"),
                   ("tt", "/hdfs/store/user/zmao/tt_3-SUB-TT"),
                   ("ZZ", "/hdfs/store/user/zmao/ZZ_3-SUB-TT")]