# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()



crab_BuToKJpsi_ToEE_0000 = kreator.makeDataComponentFromEOS('crab_BuToKJpsi_ToEE_0000','/store/cmst3/group/bpark/gkaratha/BToKEE_BToKJPsi_ToEE_MuFilter_18_12_2019/BuToKJpsi_Toee_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/crab_BuToKJpsi_ToEE/191216_203442/0000/','.*root')
crab_BuToKJpsi_ToEE_part2_0000 = kreator.makeDataComponentFromEOS('crab_BuToKJpsi_ToEE_part2_0000','/store/cmst3/group/bpark/gkaratha/BToKEE_BToKJPsi_ToEE_MuFilter_18_12_2019/BuToKJpsi_Toee_Mufilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/crab_BuToKJpsi_ToEE_part2/191217_222643/0000/','.*root')
crab_BuToKEE_0000 = kreator.makeDataComponentFromEOS('crab_BuToKEE_0000','/store/cmst3/group/bpark/gkaratha/BToKEE_BToKJPsi_ToEE_MuFilter_18_12_2019/BuToK_Toee_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/crab_BuToKEE/191216_203559/0000/','.*root')
crab_BuToKEE_part2_0000 = kreator.makeDataComponentFromEOS('crab_BuToKEE_part2_0000','/store/cmst3/group/bpark/gkaratha/BToKEE_BToKJPsi_ToEE_MuFilter_18_12_2019/BuToKee_Mufilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/crab_BuToKEE_part2/191217_222816/0000/','.*root')


samples = [crab_BuToKJpsi_ToEE_0000,crab_BuToKJpsi_ToEE_part2_0000,crab_BuToKEE_0000,crab_BuToKEE_part2_0000] 



if __name__ == "__main__":
	from CMGTools.RootTools.samples.tools import runMain
	runMain(samples, localobjs=locals())
