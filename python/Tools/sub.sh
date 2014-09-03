#!/bin/sh
# voms-proxy-init --voms cms --valid 100:00

#
# Usage:
#       farmoutAnalysisJobs <jobName> <CMSSW Version> <config file>
#
# The config file should refer to the following macros, which are automatically
# inserted by this script:
#
# $inputFileNames     ==>  Will be replaced by list of input files
# $outputFileName     ==>  Will be replaced by the $inputFileName-output.root
#
# Job parameters
#

# $1 is the output location?

#farmoutAnalysisJobs  $1   --vsize-limit=8000  --input-dir=/store/user/tapas/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/2013-02-25-8TeV-53X-PatTuple_Master   		DYJets    $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-MCZ.py


# farmoutAnalysisJobs  --input-dir=/store/user/zmao/ZZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/test3 ZZ_noSign_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# 
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/GluGluToHTohhTo2Tau2B_mH-300_mh-125_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM/3 H2hh300_sync2 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py

#farmoutAnalysisJobs  --input-dir=/store/user/zmao/GluGluToHTohhTo2Tau2B_mH-260_mh-125_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM/11 H2hh260_noSign_relaxed9 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/GluGluToHTohhTo2Tau2B_mH-300_mh-125_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM/3 H2hh300_syncNew $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
#farmoutAnalysisJobs   --input-dir=/store/user/zmao/GluGluToHTohhTo2Tau2B_mH-350_mh-125_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM/test3 H2hh350_noSign_relaxed9 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v2/AODSIM/2 tt_pt20 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM/new tt_SemiLep_pt20 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/Tau/Run2012A-22Jan2013-v1/AOD/data2 Tau_Run2012A_relaxed9 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT-data.py 
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/TauParked/Run2012B-22Jan2013-v1/AOD/data2 TauParked_Run2012B_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT-data.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/TauParked/Run2012C-22Jan2013-v1/AOD/data2 TauParked_Run2012C_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT-data.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/TauParked/Run2012D-22Jan2013-v1/AOD/data2 TauParked_Run2012D_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT-data.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM/QCD/ QCD_Pt-80to120_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM/QCD/ QCD_Pt-120to170_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/QCD_Pt-150_bEnriched_TuneZ2star_8TeV-pythia6-evtgen/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/QCD/ QCD_Pt-150_bEnriched_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py

# farmoutAnalysisJobs  --input-dir=/store/user/zmao/QCD_Pt-30To50_bEnriched_TuneZ2star_8TeV-pythia6-evtgen/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/QCD/ QCD_Pt-30To50_bEnriched_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM/QCD/ QCD_Pt-30to50_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py

# farmoutAnalysisJobs  --input-dir=/store/user/zmao/QCD_Pt-50To150_bEnriched_TuneZ2star_8TeV-pythia6-evtgen/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/QCD/ QCD_Pt-50To150_bEnriched_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM/QCD/ QCD_Pt-50to80_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py

# farmoutAnalysisJobs  --input-dir=/store/user/zmao/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/W2JetsToLNu W2JetsToLNu_relaxed9 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/DYJetsToLL/ DYJetsToLL_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/1 W1JetsToLNu_relaxed9 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/1/ W3JetsToLNu_relaxed9 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/DY3JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/1 DY3JetsToLL_relaxed9 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM/1 DY2JetsToLL_relaxed9 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/DY1JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/9 DY1JetsToLL_relaxed9 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/WZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/9 WZJetsTo2L2Q_relaxed8 $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py

# farmoutAnalysisJobs  --input-dir=/store/user/zmao/VBF_HToTauTau_M-125_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/1 VBF_HToTauTau $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
# farmoutAnalysisJobs  --input-dir=/store/user/zmao/TTJets_MSDecays_central_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM/1 TTJets_MSDecays $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
farmoutAnalysisJobs  --input-dir=/store/user/zmao/WH_ZH_TTH_HToTauTau_M-125_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/1 WH_ZH_TTH_HToTauTau $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
farmoutAnalysisJobs  --input-dir=/store/user/zmao/GluGluToHToTauTau_M-125_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/1 GluGluToHToTauTau $CMSSW_BASE $CMSSW_BASE/src/UWAnalysis/CRAB/LTau/SUB-TT.py
