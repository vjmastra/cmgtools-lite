# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()



crab_BuToKJpsi_ToMuMu_0000 = kreator.makeDataComponentFromEOS('crab_BuToKJpsi_ToMuMu_0000','/store/cmst3/group/bpark/gkaratha/BToKMuMu_BToKJPsi_ToMuMu_MuFilter_18_12_2019/BParkingNANO_2019Dec16/BuToKJpsi_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/crab_BuToKJpsi_ToMuMu/191216_120056/0000/','.*root')
crab_BuToKMuMu_0000 = kreator.makeDataComponentFromEOS('crab_BuToKMuMu_0000','/store/cmst3/group/bpark/gkaratha/BToKMuMu_BToKJPsi_ToMuMu_MuFilter_18_12_2019/BParkingNANO_2019Dec16/BuToK_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/crab_BuToKMuMu/191216_120214/0000/','.*root')


samples = [crab_BuToKJpsi_ToMuMu_0000,crab_BuToKMuMu_0000] 



if __name__ == "__main__":
	from CMGTools.RootTools.samples.tools import runMain
	runMain(samples, localobjs=locals())