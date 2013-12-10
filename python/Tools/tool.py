#!/usr/bin/env python
import sys
import ROOT as r
import time
from operator import itemgetter

lvClass = r.Math.LorentzVector(r.Math.PtEtaPhiM4D('double'))
b1 = lvClass()
b2 = lvClass()
j1 = lvClass()
j2 = lvClass()
v_tmp = lvClass()



def matchBJet(tree):
    genBPt1 = tree.bPt.at(0)
    genBPt2 = tree.bPt.at(1)
    genBEta1 = tree.bEta.at(0)
    genBEta2 = tree.bEta.at(1)
    genBPhi1 = tree.bPhi.at(0)
    genBPhi2 = tree.bPhi.at(1)
    genBMass1 = tree.bMass.at(0)
    genBMass2 = tree.bMass.at(1)

    b1.SetCoordinates(genBPt1, genBEta1, genBPhi1, genBMass1)
    b2.SetCoordinates(genBPt2, genBEta2, genBPhi2, genBMass2)
    
    dr1 = 1000
    dr2 = 1000

    #Loop to find best matching gen jet
    for j in range(1, 5):
        v_tmp.SetCoordinates(tree.GetLeaf("J%sPt" %(j)).GetValue(0),
                             tree.GetLeaf("J%sEta" %(j)).GetValue(0),
                             tree.GetLeaf("J%sPhi" %(j)).GetValue(0),
                             4.8)
        if dr1 > r.Math.VectorUtil.DeltaR(b1, v_tmp):
            dr1 = r.Math.VectorUtil.DeltaR(b1, v_tmp)
            j1pt = tree.GetLeaf("J%sPt" %(j)).GetValue(0)
            j1eta = tree.GetLeaf("J%sEta" %(j)).GetValue(0)
            j1phi = tree.GetLeaf("J%sPhi" %(j)).GetValue(0)
        if dr2 > r.Math.VectorUtil.DeltaR(b2, v_tmp):
            dr2 = r.Math.VectorUtil.DeltaR(b2, v_tmp)
            j2pt = tree.GetLeaf("J%sPt" %(j)).GetValue(0)
            j2eta = tree.GetLeaf("J%sEta" %(j)).GetValue(0)
            j2phi = tree.GetLeaf("J%sPhi" %(j)).GetValue(0)


    if dr1 < 0.5 and dr2 < 0.5:
        j1.SetCoordinates(j1pt, j1eta, j1phi, 4.8)
        j2.SetCoordinates(j2pt, j2eta, j2phi, 4.8)
    
    return j1, j2

def printProcessStatus(iCurrent, total, processName = 'Foo process'):
    iCurrent+=0.
    total+=0.
    AddedPercent = iCurrent/total
    sys.stdout.write("\r%s completed: %0.f" %(processName, round(AddedPercent,2)*100) + "%")
    sys.stdout.flush()


def addFiles(ch, dirName, knownEventNumber):
    added = 0.
    dir = r.TSystemDirectory(dirName, dirName)
    files = dir.GetListOfFiles()
    totalAmount = files.GetSize() - 2.
    for iFile in files:
        fName = dirName + '/' + iFile.GetName()
        if (not iFile.IsDirectory()) and fName.endswith(".root"):
            ch.Add(fName, knownEventNumber)
            added+=1
            printProcessStatus(iCurrent=added, total=totalAmount, processName = 'Adding files from [%s]' %dirName)
    print ""
    return added

def unitNormHists(HistNameList):
    for iHist in HistNameList:
        integral = iHist.Integral()
        if integral > 0:
            iHist.Scale(1/integral)

def xsNormHists(HistNameList, xsList):
    i=0
    for iHist in HistNameList:
        integral = iHist.Integral()
        if integral > 0:
            iHist.Scale(xsList[i]/integral*20)
            print  xsList[i]/integral*20
            print xsList[i]
        i+=1

def setDrawHists(sigHist, ttHist, ZZHist, DrawOpt = ""):

    sigHist.SetLineWidth(2)
    sigHist.SetFillStyle(3001)
    sigHist.SetFillColor(4)
    sigHist.SetLineColor(4)

    ttHist.SetLineWidth(2)
    ttHist.SetFillStyle(3001)
    ttHist.SetFillColor(2)
    ttHist.SetLineColor(2)
    ttMax = ttHist.GetMaximum() 

    ZZHist.SetLineWidth(2)
    ZZHist.SetLineStyle(2)
    ZZHist.SetLineColor(1)
    ZZMax = ZZHist.GetMaximum()

    HistMaxList = [(sigHist.GetMaximum(), sigHist),
                   (ttHist.GetMaximum(), ttHist),
                   (ZZHist.GetMaximum(), ZZHist)]
    HistMaxList = sorted(HistMaxList, key=itemgetter(0), reverse=True)
    #draw from the highest histogram

    HistMaxList[0][1].Draw(DrawOpt)
    DrawOpt = "same" + DrawOpt
    HistMaxList[1][1].Draw(DrawOpt)
    HistMaxList[2][1].Draw(DrawOpt)

def setMyLegend(lPosition, lHistList):
    l = r.TLegend(lPosition[0], lPosition[1], lPosition[2], lPosition[3])
    l.SetFillStyle(0)
    l.SetBorderSize(0)
    for i in range(len(lHistList)):
        l.AddEntry(lHistList[i][0], lHistList[i][1])
    return l

def addHistFirstBinFromFiles(dirName, nBins=15, xMin=0, xMax=14):
    added = 0.
    firstBinSum = 0
    dir = r.TSystemDirectory(dirName, dirName)
    files = dir.GetListOfFiles()
    totalAmount = files.GetSize() - 2.
    for iFile in files:
        fName = dirName + '/' + iFile.GetName()
        if (not iFile.IsDirectory()) and fName.endswith(".root"):
            tmpHist = r.TH1F("tmpHist", " ", nBins, xMin, xMax)
            ifile = r.TFile(fName)
            tmpHist = ifile.Get("TT/results")
            firstBinSum+=tmpHist.GetBinContent(1)
            added+=1
            printProcessStatus(iCurrent=added, total=totalAmount, processName = 'Adding files from [%s]' %dirName)
    print ""
    return firstBinSum
