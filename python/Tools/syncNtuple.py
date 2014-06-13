#!/usr/bin/env python

import ROOT as r
import tool
from array import array
from operator import itemgetter


varList = [('run', 'RUN', 'I'),
           ('lumi', 'LUMI', 'I'),
           ('evt', 'EVENT', 'I'),
           ('npv', 'vertices', 'I'),

           ('rho', 'Rho', 'F'),

           ('mvis', 'mTauTau', 'F'),
           ('m_sv', 'svMass', 'F'),
           ('pt_sv', 'svPt', 'F'),
           ('eta_sv', 'svEta', 'F'),
           ('phi_sv', 'svPhi', 'F'),

           ('pt_1', 'pt1', 'F'),
           ('phi_1', 'phi1', 'F'),
           ('eta_1', 'eta1', 'F'),
           ('m_1', 'm1', 'F'),
           ('q_1', 'charge1', 'I'),
           ('mva_1', 0, 'I'),
           ('byCombinedIsolationDeltaBetaCorrRaw3Hits_1', 'iso1', 'F'),
           ('d0_1', 'd0_1', 'F'),
           ('dZ_1', 'l1dz', 'F'),
           ('mt_1', 'mt1', 'F'),

           ('pt_2', 'pt2', 'F'),
           ('phi_2', 'phi2', 'F'),
           ('eta_2', 'eta2', 'F'),
           ('m_2', 'm2', 'F'),
           ('q_2', 'charge2', 'I'),
           ('mva_2', 0, 'I'),
           ('byCombinedIsolationDeltaBetaCorrRaw3Hits_2', 'iso2', 'F'),
           ('d0_2', 'd0_2', 'I'),
           ('dZ_2', 'l2dz', 'F'),
           ('mt_2', 'mt2', 'F'),

           ('againstMuonLoose2_1', 'againstMuonLoose1', 'F'),
           ('againstMuonLoose2_2', 'againstMuonLoose2', 'F'),
           ('againstMuonMedium2_1', 'againstMuonMedium1', 'F'),
           ('againstMuonMedium2_2', 'againstMuonMedium2', 'F'),
           ('againstMuonTight2_1', 'againstMuonTight1', 'F'),
           ('againstMuonTight2_2', 'againstMuonTight2', 'F'),

           ('met', 'metUnc', 'F'),
           ('mvamet', 'met', 'F'),
           ('mvametphi', 'metphi', 'F'),


           ('jpt_1', 'J1Pt', 'F'),
           ('jeta_1', 'J1Eta', 'F'),
           ('jphi_1', 'J1Phi', 'F'),
           ('jptraw_1', 'J1PtUncorr', 'F'),
           ('jptunc_1', 'J1JECUnc', 'F'),
           ('jctm_1', 'J1Ntot', 'I'),

           ('jpt_2', 'J2Pt', 'F'),
           ('jeta_2', 'J2Eta', 'F'),
           ('jphi_2', 'J2Phi', 'F'),
           ('jptraw_2', 'J2PtUncorr', 'F'),
           ('jptunc_2', 'J2JECUnc', 'F'),
           ('jctm_2', 'J2Ntot', 'I'),
          ]

def makeSyncNtuples(iLocation):

    iTree = r.TChain("TauCheck/eventTree")
    print iLocation
    nEntries = tool.addFiles(ch=iTree, dirName=iLocation, knownEventNumber=0, maxFileNumber=-1, printTotalEvents = True)
    print nEntries
    iTree.SetBranchStatus("*",1)

    oFile = r.TFile("HTT_2.root" ,"recreate")
    oTree = r.TTree('TauCheck', 'TauCheck')

    run  = array('i', [0])
    lumi = array('i', [0])
    evt = array('i', [0])

    npv = array('i', [0])
    npu = array('i', [0])
    rho = array('f', [0.])

    mvis = array('f', [0.])
    m_sv = array('f', [0.])
    pt_sv = array('f', [0.])
    eta_sv = array('f', [0.])
    phi_sv = array('f', [0.])
    
    pt_1 = array('f', [0.])
    phi_1 = array('f', [0.])
    eta_1 = array('f', [0.])
    m_1 = array('f', [0.])
    q_1 = array('i', [0])
    iso_1 = array('f', [0.])
    mva_1 = array('f', [0.])
    byCombinedIsolationDeltaBetaCorrRaw3Hits_1 = array('f', [0.])
    d0_1 = array('f', [0.])
    dZ_1 = array('f', [0.])
    mt_1 = array('f', [0.])

    pt_2 = array('f', [0.])
    phi_2 = array('f', [0.])
    eta_2 = array('f', [0.])
    m_2 = array('f', [0.])
    q_2 = array('i', [0])
    iso_2 = array('f', [0.])
    mva_2 = array('f', [0.])
    byCombinedIsolationDeltaBetaCorrRaw3Hits_2 = array('f', [0.])
    d0_2 = array('f', [0.])
    dZ_2 = array('f', [0.])
    mt_2 = array('f', [0.])

    againstElectronMVA3raw_1 = array('f', [0.])
    againstElectronMVA3raw_2 = array('f', [0.])
    againstMuonLoose2_1 = array('f', [0.])
    againstMuonLoose2_2 = array('f', [0.])
    againstMuonMedium2_1 = array('f', [0.])
    againstMuonMedium2_2 = array('f', [0.])
    againstMuonTight2_1 = array('f', [0.])
    againstMuonTight2_2 = array('f', [0.])

    met = array('f', [0.])
    mvamet = array('f', [0.])
    mvametphi = array('f', [0.])
    mvacov00 = array('f', [0.])
    mvacov01 = array('f', [0.])
    mvacov10 = array('f', [0.])
    mvacov11 = array('f', [0.])

    pzetavis = array('f', [0.])
    pzetamiss = array('f', [0.])

    pt_tt = array('f', [0.])
    njets = array('f', [0.])
    njetspt20 = array('f', [0.])

    jpt_1 = array('f', [0.])
    jeta_1 = array('f', [0.])
    jphi_1 = array('f', [0.])
    jptraw_1 = array('f', [0.])
    jptunc_1 = array('f', [0.])
    jmva_1 = array('f', [0.])
    jlrm_1 = array('f', [0.])
    jctm_1 = array('f', [0.])
    jpass_1 = array('b', [0])

    jpt_2 = array('f', [0.])
    jeta_2 = array('f', [0.])
    jphi_2 = array('f', [0.])
    jptraw_2 = array('f', [0.])
    jptunc_2 = array('f', [0.])
    jmva_2 = array('f', [0.])
    jlrm_2 = array('f', [0.])
    jctm_2 = array('f', [0.])
    jpass_2 = array('b', [0])

    bpt_1 = array('f', [0.])
    beta_1 = array('f', [0.])
    bphi_1 = array('f', [0.])
    bcsv_1 = array('f', [0.])

    bpt_2 = array('f', [0.])
    beta_2 = array('f', [0.])
    bphi_2 = array('f', [0.])
    bcsv_2 = array('f', [0.])

    bpt_3 = array('f', [0.])
    beta_3 = array('f', [0.])
    bphi_3 = array('f', [0.])
    bcsv_3 = array('f', [0.])

    m_bb = array('f', [0.])
    m_ttbb = array('f', [0.])
    nbtag = array('f', [0.])

    oTree.Branch("run", run, "run/I")
    oTree.Branch("lumi", lumi, "lumi/I")
    oTree.Branch("evt", evt, "evt/I")

    oTree.Branch("npv", npv, "npv/I")
    oTree.Branch("npu", npu, "npu/I")
    oTree.Branch("rho", rho, "rho/F")

    oTree.Branch("mvis", mvis, "mvis/F")
    oTree.Branch("m_sv", m_sv, "m_sv/F")
    oTree.Branch("pt_sv", pt_sv, "pt_sv/F")
    oTree.Branch("eta_sv", eta_sv, "eta_sv/F")
    oTree.Branch("phi_sv", phi_sv, "phi_sv/F")

    oTree.Branch("pt_1", pt_1, "pt_1/F")
    oTree.Branch("phi_1", phi_1, "phi_1/F")
    oTree.Branch("eta_1", eta_1, "eta_1/F")
    oTree.Branch("m_1", m_1, "m_1/F")
    oTree.Branch("q_1", q_1, "q_1/I")
    oTree.Branch("iso_1", iso_1, "iso_1/F")
    oTree.Branch("mva_1", mva_1, "mva_1/F")
    oTree.Branch("byCombinedIsolationDeltaBetaCorrRaw3Hits_1", byCombinedIsolationDeltaBetaCorrRaw3Hits_1, "byCombinedIsolationDeltaBetaCorrRaw3Hits_1/F")
    oTree.Branch("d0_1", d0_1, "d0_1/F")
    oTree.Branch("dZ_1", dZ_1, "dZ_1/F")
    oTree.Branch("mt_1", mt_1, "mt_1/F")

    oTree.Branch("pt_2", pt_2, "pt_2/F")
    oTree.Branch("phi_2", phi_2, "phi_2/F")
    oTree.Branch("eta_2", eta_2, "eta_2/F")
    oTree.Branch("m_2", m_2, "m_2/F")
    oTree.Branch("q_2", q_2, "q_2/I")
    oTree.Branch("iso_2", iso_2, "iso_2/F")
    oTree.Branch("mva_2", mva_2, "mva_2/F")
    oTree.Branch("byCombinedIsolationDeltaBetaCorrRaw3Hits_2", byCombinedIsolationDeltaBetaCorrRaw3Hits_2, "byCombinedIsolationDeltaBetaCorrRaw3Hits_2/F")
    oTree.Branch("d0_2", d0_2, "d0_2/F")
    oTree.Branch("dZ_2", dZ_2, "dZ_2/F")
    oTree.Branch("mt_2", mt_2, "mt_2/F")

    oTree.Branch("againstElectronMVA3raw_1", againstElectronMVA3raw_1, "againstElectronMVA3raw_1/F")
    oTree.Branch("againstElectronMVA3raw_2", againstElectronMVA3raw_2, "againstElectronMVA3raw_2/F")
    oTree.Branch("againstMuonLoose2_1", againstMuonLoose2_1, "againstMuonLoose2_1/F")
    oTree.Branch("againstMuonLoose2_2", againstMuonLoose2_2, "againstMuonLoose2_2/F")
    oTree.Branch("againstMuonMedium2_1", againstMuonMedium2_1, "againstMuonMedium2_1/F")
    oTree.Branch("againstMuonMedium2_2", againstMuonMedium2_2, "againstMuonMedium2_2/F")
    oTree.Branch("againstMuonTight2_1", againstMuonTight2_1, "againstMuonTight2_1/F")
    oTree.Branch("againstMuonTight2_2", againstMuonTight2_2, "againstMuonTight2_2/F")

    oTree.Branch("met", met, "met/F")
    oTree.Branch("mvamet", mvamet, "mvamet/F")
    oTree.Branch("mvametphi", mvametphi, "mvametphi/F")
    oTree.Branch("mvacov00", mvacov00, "mvacov00/F")
    oTree.Branch("mvacov01", mvacov01, "mvacov01/F")
    oTree.Branch("mvacov10", mvacov10, "mvacov10/F")
    oTree.Branch("mvacov11", mvacov11, "mvacov11/F")

    oTree.Branch("pzetavis", pzetavis, "pzetavis/F")
    oTree.Branch("pzetamiss", pzetamiss, "pzetamiss/F")

    oTree.Branch("pt_tt", pt_tt, "pt_tt/F")
    oTree.Branch("njets", njets, "njets/F")
    oTree.Branch("njetspt20", njetspt20, "njetspt20/F")

    oTree.Branch("jpt_1", jpt_1, "jpt_1/F")
    oTree.Branch("jeta_1", jeta_1, "jeta_1/F")
    oTree.Branch("jphi_1", jphi_1, "jphi_1/F")
    oTree.Branch("jptraw_1", jptraw_1, "jptraw_1/F")
    oTree.Branch("jptunc_1", jptunc_1, "jptunc_1/F")
    oTree.Branch("jmva_1", jmva_1, "jmva_1/F")
    oTree.Branch("jctm_1", jctm_1, "jctm_1/F")
    oTree.Branch("jpass_1", jpass_1, "jpass_1/B")    

    oTree.Branch("jpt_2", jpt_2, "jpt_2/F")
    oTree.Branch("jeta_2", jeta_2, "jeta_2/F")
    oTree.Branch("jphi_2", jphi_2, "jphi_2/F")
    oTree.Branch("jptraw_2", jptraw_2, "jptraw_2/F")
    oTree.Branch("jptunc_2", jptunc_2, "jptunc_2/F")
    oTree.Branch("jmva_2", jmva_2, "jmva_2/F")
    oTree.Branch("jctm_2", jctm_2, "jctm_2/F")
    oTree.Branch("jpass_2", jpass_2, "jpass_2/B")    

    oTree.Branch("bpt_1", bpt_1, "bpt_1/F")
    oTree.Branch("beta_1", beta_1, "beta_1/F")
    oTree.Branch("bphi_1", bphi_1, "bphi_1/F")
    oTree.Branch("bcsv_1", bcsv_1, "bcsv_1/F")
    oTree.Branch("bpt_2", bpt_2, "bpt_2/F")
    oTree.Branch("beta_2", beta_2, "beta_2/F")
    oTree.Branch("bphi_2", bphi_2, "bphi_2/F")
    oTree.Branch("bcsv_2", bcsv_2, "bcsv_2/F")
    oTree.Branch("bpt_3", bpt_3, "bpt_3/F")
    oTree.Branch("beta_3", beta_3, "beta_3/F")
    oTree.Branch("bphi_3", bphi_3, "bphi_3/F")
    oTree.Branch("bcsv_3", bcsv_3, "bcsv_3/F")

    oTree.Branch("m_bb", m_bb, "m_bb/F")    
    oTree.Branch("m_ttbb", m_ttbb, "m_ttbb/F")    

    counter = 0
    lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
    b1 = lvClass()
    b2 = lvClass()
    tau1 = lvClass()
    tau2 = lvClass()
    for iEntry in range(nEntries):
        iTree.GetEntry(iEntry)

        jetsList = [(iTree.J1CSVbtag, iTree.J1Pt, iTree.J1Eta, iTree.J1Phi, iTree.J1Mass),
                    (iTree.J2CSVbtag, iTree.J2Pt, iTree.J2Eta, iTree.J2Phi, iTree.J2Mass),
                    (iTree.J3CSVbtag, iTree.J3Pt, iTree.J3Eta, iTree.J3Phi, iTree.J3Mass),
                    (iTree.J4CSVbtag, iTree.J4Pt, iTree.J4Eta, iTree.J4Phi, iTree.J4Mass)]
        jetsList = sorted(jetsList, key=itemgetter(0), reverse=True)

        tau1.SetCoordinates(iTree.pt1.at(0), iTree.eta1.at(0), iTree.phi1.at(0), iTree.m1.at(0))
        tau2.SetCoordinates(iTree.pt2.at(0), iTree.eta2.at(0), iTree.phi2.at(0), iTree.m2.at(0))

        b1.SetCoordinates(jetsList[0][1], jetsList[0][2], jetsList[0][3], jetsList[0][4])
        b2.SetCoordinates(jetsList[1][1], jetsList[1][2], jetsList[1][3], jetsList[1][4])

        if jetsList[0][1] < 20 or jetsList[1][1] < 20:
            continue
        if abs(jetsList[0][2]) > 2.4 or abs(jetsList[1][2]) > 2.4:
            continue

        run[0] = iTree.RUN
        evt[0] = iTree.EVENT
        npv[0] = iTree.LUMI
        npu[0] = int(iTree.puBX0)
        lumi[0] = iTree.vertices
        rho[0] = iTree.Rho
        mvis[0] = (tau1+tau2).mass()
        m_sv[0] = iTree.svMass.at(0)
        pt_sv[0] = iTree.svPt.at(0)
        eta_sv[0] = iTree.svEta.at(0)
        phi_sv[0] = iTree.svPhi.at(0)

        pt_1[0] = iTree.pt1.at(0)
        eta_1[0] = iTree.eta1.at(0)
        phi_1[0] = iTree.phi1.at(0)
        m_1[0] = iTree.m1.at(0)
        q_1[0] = int(iTree.charge1.at(0))
        iso_1[0] = iTree.tau1MVAIso
        mva_1[0] = 0
        byCombinedIsolationDeltaBetaCorrRaw3Hits_1[0] = iTree.iso1.at(0)
        d0_1[0] = iTree.d0_1
        dZ_1[0] = iTree.l1dz
        mt_1[0] = iTree.mt1

        pt_2[0] = iTree.pt2.at(0)
        eta_2[0] = iTree.eta2.at(0)
        phi_2[0] = iTree.phi2.at(0)
        m_2[0] = iTree.m2.at(0)
        q_2[0] = int(iTree.charge2.at(0))
        iso_2[0] = iTree.tau2MVAIso
        mva_2[0] = 0
        byCombinedIsolationDeltaBetaCorrRaw3Hits_2[0] = iTree.iso2.at(0)
        d0_2[0] = iTree.d0_2
        dZ_2[0] = iTree.l2dz
        mt_2[0] = iTree.mt2

        againstElectronMVA3raw_1[0] = iTree.againstElectronMVA3raw_1
        againstElectronMVA3raw_2[0] = iTree.againstElectronMVA3raw_2
        againstMuonLoose2_1[0] = iTree.againstMuonLoose1.at(0)
        againstMuonLoose2_2[0] = iTree.againstMuonLoose2.at(0)
        againstMuonMedium2_1[0] = iTree.againstMuonMedium2_1
        againstMuonMedium2_2[0] = iTree.againstMuonMedium2_2
        againstMuonTight2_1[0] = iTree.againstMuonTight2_1
        againstMuonTight2_2[0] = iTree.againstMuonTight2_2

        met[0] = iTree.metUnc
        mvamet[0] = iTree.met.at(0)
        mvametphi[0] = iTree.metphi.at(0)
        mvacov00[0] = iTree.mvacov00
        mvacov01[0] = iTree.mvacov01
        mvacov10[0] = iTree.mvacov10
        mvacov11[0] = iTree.mvacov11
    
        pzetavis[0] = iTree.pZV
        pzetamiss[0] = iTree.pZetaMiss

        pt_tt[0] = iTree.fullPt

        njets[0] = iTree.njets
        njetspt20[0] = iTree.njetspt20

        bcsv_1[0] = jetsList[0][0]
        bpt_1[0] = jetsList[0][1]
        beta_1[0] = jetsList[0][2]
        bphi_1[0] = jetsList[0][3]
        bcsv_2[0] = jetsList[1][0]
        bpt_2[0] = jetsList[1][1]
        beta_2[0] = jetsList[1][2]
        bphi_2[0] = jetsList[1][3]
        bcsv_3[0] = jetsList[2][0]
        bpt_3[0] = jetsList[2][1]
        beta_3[0] = jetsList[2][2]
        bphi_3[0] = jetsList[2][3]

        jpt_1[0] = iTree.J2Pt
        jeta_1[0] = iTree.J2Eta
        jphi_1[0] = iTree.J2Phi
        jptraw_1[0] = iTree.J2PtUncorr
        jptunc_1[0] = iTree.J2JECUnc
        jmva_1[0] = iTree.jmva_1
        jctm_1[0] = iTree.J2Ntot
        jpass_1[0] = bool(iTree.jpass_1) 

        jpt_2[0] = iTree.J2Pt
        jeta_2[0] = iTree.J2Eta
        jphi_2[0] = iTree.J2Phi
        jptraw_2[0] = iTree.J2PtUncorr
        jptunc_2[0] = iTree.J2JECUnc
        jmva_2[0] = iTree.jmva_2
        jctm_2[0] = iTree.J2Ntot
        jpass_2[0] = bool(iTree.jpass_2)

        m_bb[0] = iTree.mJJ
        m_ttbb[0] = iTree.HMass

        oTree.Fill()
        counter += 1
        tool.printProcessStatus(iEntry, nEntries, 'Saving to file ')
    
    print ''
    oFile.cd()
    oTree.Write()
    oFile.Close()

makeSyncNtuples('/hdfs/store/user/zmao/H2hh300_sync2-SUB-TT')