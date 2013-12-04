pb = 1.0
fb = 1.0e3*pb

def signal(title="gg --> H --> hh --> tauttaubb"):
    print title
    print "-"*len(title)
    # xs(gg --> H_300) * BR(H--> hh) * BR(h-->bb) * BR(h-->tt) * 2

    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt8TeV#gluon_gluon_Fusion_Process

    xs_gg = 3.594 * pb

    br_mssm = 4.737830E-02 * 0.636044 * 7.340051E-02 * 2
    br_xxsm = 4.737830E-02 * 0.521541 * 5.962125E-02 * 2
    print "BR_mssm = ", br_mssm
    print "BR_xxsm = ", br_xxsm
    
    print "xs_mssm (fb) = ", xs_gg * br_mssm * fb
    print "xs_xxsm (fb) = ", xs_gg * br_xxsm * fb
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

signal()
ttbar()
