#!/usr/bin/env python

import ROOT as r
import os

ChainHistList = [('a', '1'),
                 ('b', '2'),
                 ('c', '3')]

print "size: %d" %(len(ChainHistList))

for i in range(3):
    print ChainHistList[0][0]