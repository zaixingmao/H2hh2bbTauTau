To install TMVA

1) cd CMSSW_X_X_X/src

2) cmsenv

3) wget http://sourceforge.net/projects/tmva/files/TMVA-v*.tgz	#whatever new version

4) tar xfz TMVA-v*.tgz

5) cd TMVA-v*

6) make

7) cp TMVAClassification_new.py test/

8) cp tool.py test/

9) source setup.sh

10) python TMVAClassification_new.py --methods BDT
