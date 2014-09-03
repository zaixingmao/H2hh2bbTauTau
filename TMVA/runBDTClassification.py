#!/usr/bin/env python
import os as os
import varsList
def reWriteRankFile(inputFile):

    lines = open(inputFile, "r").readlines()
    ofile = "%s_fix.txt" %inputFile[0: inputFile.rfind(".txt")]
    output = open(ofile, "w")
    output.writelines(" massPoint: %s            nVars %s\n" %(massPoint, nVars))
    output.writelines(" --------------------------------------------------\n")
    for i in range(0, len(lines)):
        current_line = lines[i]
        cutPosition = current_line.find(":")
        BDT = current_line.find("--- BDT                      :")
        if BDT == -1:
            output.close()
            print "file saved at: %s" %ofile

            return 1
        current_line = current_line[cutPosition+1:len(current_line)]
        output.writelines(current_line)
    

varList = varsList.varList

nVars = str(len(varList))
# nVars += "_2"

massPoints = ["260", "300", "350"]


for massPoint in massPoints:
    command1 = "python TMVAClassification_both.py -i %s | grep \"Variable Importance\" -A 20 > /scratch/zmao/TMVA/new/varsRank%s_%s.txt" %(massPoint, massPoint, nVars)
    command2 = "mv TMVA.root /scratch/zmao/TMVA/new/TMVA%s_%s.root" %(massPoint, nVars)

    os.system(command1)
    os.system(command2)
    reWriteRankFile("/scratch/zmao/TMVA/new/varsRank%s_%s.txt" %(massPoint, nVars))
    print 

