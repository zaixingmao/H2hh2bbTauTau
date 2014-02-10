#!/usr/bin/env python

import ROOT as r
import os
import enVars
import tool

signalLocation = enVars.signalLocation
signalEntries = 0


print tool.addHistFirstBinFromFiles(dirName=signalLocation)
