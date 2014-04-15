#!/usr/bin/env python
import ROOT as r
import optparse
import tool
import random

r.gROOT.SetBatch(True)  # to suppress canvas pop-outs

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--f1", dest="file1", default="", help="REQUIRED: .root file 1 over which to run")
    parser.add_option("--f2", dest="file2", default="", help="REQUIRED: .root file 2 over which to run")
    parser.add_option("--n", dest="nEvents", default=2, help="Number of Events to be Compared")
    options, args = parser.parse_args()

    if not all([options.file1, options.file2]):
        parser.print_help()
        exit()
    return options

options = opts()

def checkVars(var1, var2):
    if var1 == var2:
        if var1 < 0:
            return "", var1, "", var2, "-"
        else:
            return " ", var1, " ", var2, "-"
    else:
        if var1 < 0:
            return "", var1, "", var2, "Different!!!"
        else:
            return " ", var1, " ", var2, "Different!!!"

f1 = r.TFile(options.file1)
f2 = r.TFile(options.file2)
tree1 = f1.Get("eventTree")
tree2 = f2.Get("ttTreeBeforeChargeCut/eventTree")

listBranch = tree1.GetListOfBranches()


nBranches = listBranch.GetEntries()

for iEventsTried in range(0, options.nEvents):
    iRan = random.randint(0, tree1.GetEntries())
    tree1.GetEntry(iRan)
    eventNumber = tree1.EVENT
    foundEvent = 0
    
    for j in range(0, tree2.GetEntries()):
        tree2.GetEntry(j)
        if tree2.EVENT == eventNumber:
            print '--------------------- Event %s ------------' %(eventNumber)
            print '--------------  f1  --------------  f2  ------'
            print 'pt1 :       %s%.3e    |    %s%.3e    %s' %(checkVars(tree1.pt1.at(0), tree2.pt1.at(0)))
            print 'pt2 :       %s%.3e    |    %s%.3e    %s' %(checkVars(tree1.pt2.at(0), tree2.pt2.at(0)))
            print 'eta1:       %s%.3e    |    %s%.3e    %s' %(checkVars(tree1.eta1.at(0), tree2.eta1.at(0)))
            print 'eta2:       %s%.3e    |    %s%.3e    %s' %(checkVars(tree1.eta2.at(0), tree2.eta2.at(0)))
            print 'phi1:       %s%.3e    |    %s%.3e    %s' %(checkVars(tree1.phi1.at(0), tree2.phi1.at(0)))
            print 'phi2:       %s%.3e    |    %s%.3e    %s' %(checkVars(tree1.phi2.at(0), tree2.phi2.at(0)))
#             print 'm1:         %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.m1.at(0), tree2.m1.at(0))
#             print 'm2:         %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.m2.at(0), tree2.m2.at(0))
#             print 'iso1:       %s%.3e    |    %s%.3e    %s' %(checkVars(tree1.iso1.at(0), tree2.iso1.at(0)))
#             print 'iso2:       %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.iso2.at(0), tree2.iso2.at(0)))
#             print 'NBTags:         %s%i        |        %s%i        %s' %( checkVars(tree1.NBTags, tree2.NBTags))
#             print 'J1CSVbtag:  %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J1CSVbtag, tree2.J1CSVbtag))
#             print 'J1Eta:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J1Eta, tree2.J1Eta))
#             print 'J1Phi:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J1Phi, tree2.J1Phi))
#             print 'J1Pt:       %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J1Pt, tree2.J1Pt))
#             print 'J1Mass:     %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J1Mass, tree2.J1Mass))
# 
#             print 'J2CSVbtag:  %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J2CSVbtag, tree2.J2CSVbtag))
#             print 'J2Eta:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J2Eta, tree2.J2Eta))
#             print 'J2Phi:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J2Phi, tree2.J2Phi))
#             print 'J2Pt:       %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J2Pt, tree2.J2Pt))
#             print 'J2Mass:     %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J2Mass, tree2.J2Mass))
# 
#             print 'J3CSVbtag:  %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J3CSVbtag, tree2.J3CSVbtag))
#             print 'J3Eta:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J3Eta, tree2.J3Eta))
#             print 'J3Phi:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J3Phi, tree2.J3Phi))
#             print 'J3Pt:       %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J3Pt, tree2.J3Pt))
#             print 'J3Mass:     %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J3Mass, tree2.J3Mass))
# 
#             print 'J4CSVbtag:  %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J4CSVbtag, tree2.J4CSVbtag))
#             print 'J4Eta:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J4Eta, tree2.J4Eta))
#             print 'J4Phi:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J4Phi, tree2.J4Phi))
#             print 'J4Pt:       %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J4Pt, tree2.J4Pt))
#             print 'J4Mass:     %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.J4Mass, tree2.J4Mass))
# 
#             print 'HMass:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.HMass, tree2.HMass))
#             print 'fMass:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.fMass, tree2.fMass))
#             print 'etaJJ:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.etaJJ, tree2.etaJJ))
#             print 'phiJJ:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.phiJJ, tree2.phiJJ))
#             print 'ptJJ:       %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.ptJJ, tree2.ptJJ))
#             print 'mJJ:        %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.mJJ, tree2.mJJ))
#             print 'met:        %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.met.at(0), tree2.met.at(0)))
#             print 'pZ:         %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.pZ, tree2.pZ))
#             print 'pZV:        %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.pZV, tree2.pZV))
#             print 'pZeta:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.pZeta, tree2.pZeta))
#             print 'svEta:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.svEta.at(0), tree2.svEta.at(0)))
#             print 'svMass:     %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.svMass.at(0), tree2.svMass.at(0)))
#             print 'svPhi:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.svPhi.at(0), tree2.svPhi.at(0)))
#             print 'CSVJ1:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.CSVJ1, tree2.CSVJ1))
#             print 'CSVJ2:      %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.CSVJ2, tree2.CSVJ2))
#             print 'dRTauTau:   %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.dRTauTau, tree2.dRTauTau))
#             print 'dRJJ:       %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.dRJJ, tree2.dRJJ))
#             print 'dRhh:       %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.dRhh, tree2.dRhh))
            print 'triggerEff: %s%.3e    |    %s%.3e    %s' %( checkVars(tree1.triggerEff, tree2.diTauHadTriggerWeight))
            print '----------------------------------------------'
            print ' '
            foundEvent = 1
    if not foundEvent:
        print '------------- Could\'nt Find Event %s -----------' %(eventNumber)
