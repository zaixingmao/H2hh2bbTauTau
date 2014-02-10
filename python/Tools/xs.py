pb = 1.0
fb = 1.0e3*pb

def signal(title="gg --> H --> hh --> tauttaubb", tanB=None, mA=None):
    assert mA is not None
    assert tanB is not None
    title += "  (mA=%3d, tanB=%3.1f)" % (mA, tanB)
    print title
    print "-"*len(title)
    # xs(gg --> H_300) * BR(H--> hh) * BR(h-->bb) * BR(h-->tt) * 2

    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt8TeV#gluon_gluon_Fusion_Process


    if mA == 300.0:
        xs_gg = 3.594 * pb
    elif mA == 260.0:
        xs_gg = 4.461 * pb
    elif mA == 350.0:
        xs_gg = 3.401 * pb
    else:
        xs_gg = 0.

    if (mA == 300.0) and (tanB == 3.0):
        br_hh =  0.387919
        br_bb = 0.760173
        br_bb_sm = 0.691853
        br_tautau = 8.488134E-02
        br_tautau_sm = 7.768646E-02

    elif (mA == 260.0) and (tanB == 3.0):
        br_hh =  0.584283
        br_bb = 0.785130
        br_bb_sm = 0.702055
        br_tautau = 8.757456E-02
        br_tautau_sm = 7.870959E-02

    elif (mA == 350.0) and (tanB == 3.0):
        br_hh =  0.236728
        br_bb = 0.736941
        br_bb_sm = 0.683177
        br_tautau = 8.236178E-02
        br_tautau_sm = 7.679761E-02


    elif (mA == 300.0) and (tanB == 5.0):
        br_hh = 0.233635
        br_bb = 0.686272
        br_bb_sm = 0.587200 
        br_tautau = 7.787560E-02
        br_tautau_sm = 6.672744E-02

    elif (mA == 260.0) and (tanB == 5.0):
        br_hh = 0.309927
        br_bb = 0.719826
        br_bb_sm = 0.593764 
        br_tautau = 8.176575E-02
        br_tautau_sm = 6.742464E-02

    elif (mA == 350.0) and (tanB == 5.0):
        br_hh = 0.135464
        br_bb = 0.656414
        br_bb_sm = 0.581146 
        br_tautau = 7.443343E-02
        br_tautau_sm = 6.607262E-02


    elif (mA == 300.0) and (tanB == 10.0):
        br_hh = 4.737830E-02
        br_bb = 0.636044
        br_bb_sm = 0.521541
        br_tautau = 7.340051E-02
        br_tautau_sm = 5.962125E-02

    elif (mA == 260.0) and (tanB == 10.0):
        br_hh = 3.151184E-02
        br_bb = 0.672953
        br_bb_sm = 0.523072
        br_tautau = 7.802198E-02
        br_tautau_sm = 5.978365E-02

    elif (mA == 350.0) and (tanB == 10.0):
        br_hh = 3.003028E-02
        br_bb = 0.604155
        br_bb_sm = 0.518957
        br_tautau = 6.946494E-02
        br_tautau_sm = 5.933430E-02

    else:
        assert False

    br_mssm = br_hh * br_bb * br_tautau * 2
    print "BR_H_hh = %8.2e" %  br_hh
    print "BR_h_bb = %8.2e" %  br_bb
    print "BR_h_tt = %8.2e" %  br_tautau
    #print "mssm_bbtt / sm_bbtt = %5.2f" %  (br_bb * br_tautau / (br_bb_sm * br_tautau_sm))
    print "BR_mssm = %8.2e" %  br_mssm
    print "xs_mssm (fb) = %6.2f" % (xs_gg * br_mssm * fb)
    print


def ttbar(title="pp --> tt --> bb tautau nunu"):
    print title
    print "-"*len(title)

    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
    xs_inc = 245.8 * pb
    br_W_taunu = 0.1125
    print "BR_W_taunu = ", br_W_taunu
    br_WW_tauttaununu = br_W_taunu**2
    print "BR_WW_tautaununu = ", br_WW_tauttaununu
    print "xs_tautaubb (fb) = ", xs_inc * br_WW_tauttaununu * fb
    print


def zz(title="pp --> ZZ --> bb tautau"):
    print title
    print "-"*len(title)

    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013
    xs_inc = 2.502 * pb
    br_Z_qq = 0.6991
    br_Z_bb = 0.1512
    br_Z_tautau_over_ll = 1/3.
    br = br_Z_tautau_over_ll * br_Z_bb / br_Z_qq
    print "BR_ZllZqq_ZtautauZbb = ", br
    print "xs_tautaubb (fb) = ", xs_inc * br * fb
    print


signal(mA=260.0, tanB=3.0)
signal(mA=300.0, tanB=3.0)
signal(mA=350.0, tanB=3.0)

signal(mA=260.0, tanB=5.0)
signal(mA=300.0, tanB=5.0)
signal(mA=350.0, tanB=5.0)

signal(mA=260.0, tanB=10.0)
signal(mA=300.0, tanB=10.0)
signal(mA=350.0, tanB=10.0)
ttbar()
zz()
