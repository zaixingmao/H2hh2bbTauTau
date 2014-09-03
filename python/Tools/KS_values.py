#!/usr/bin/env python

import ROOT as r


ksTestValues = [0.886, 0.895, 0.305, 0.655,
                0.955, 0.772, 0.329, 0.107,
                0.367, 0.494, 0.067, 0.021,
                0.029, 0.984, 0.376, 0.511,
                0.159, 0.792]

hist = r.TH1F('hist', '', 10, 0, 1)
for iKS in ksTestValues:
    hist.Fill(iKS)

psfile = 'KStests.pdf'
c = r.TCanvas("c","Test", 800, 600)
hist.Draw('E0')
c.Print('%s' %psfile)
c.Close()

