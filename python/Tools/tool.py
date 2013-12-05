#!/usr/bin/env python

import ROOT as r
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

    
def addFiles(ch, dirName, ext = ".root"):
    added = 0.
    printTick = 0.2
    dir = r.TSystemDirectory(dirName, dirName)
    files = dir.GetListOfFiles()
    totalAmount = files.GetSize() - 2.
    for iFile in files:
        fName = dirName + '/' + iFile.GetName()
        if (not iFile.IsDirectory()) and fName.endswith(ext):
            ch.Add(fName)
            added+=1
            AddedPercent = added/totalAmount
            if not AddedPercent < printTick:
                print "Added: %0.f" %(round(AddedPercent,2)*100) + "%"
                printTick += 0.2
    return added

    