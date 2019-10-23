# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# ----------------------------- 2018 pp run  ----------------------------------------

# ----------------------------- Run2018A 17Sep2018 ----------------------------------------
MCBToKMuMu = kreator.makeDataComponentFromEOS("MCBToKMuMu", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/BuToKMuMu_probefilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/crab_BuToKMuMu/190912_160256/0000/", ".*root")

MCBToKstarMuMu = kreator.makeDataComponentFromEOS("MCBToKstarMuMu", "/store/cmst3/group/bpark/BParkingNANO_2019Oct18/BdToKstarMuMu_probefilter_SoftQCDnonD_TuneCP5_13Tev-pythia8-evtgen/crab_BuToKstarMuMu/191017_221742/0000/", ".*root")

MCBToKstarEE = kreator.makeDataComponentFromEOS("MCBToKstarEE", "/store/cmst3/group/bpark/BParkingNANO_2019Oct18/BdToKstaree_Mufilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/crab_BuToKstarEE/191017_221900/0000/", ".*root")


#RunA_part2 = [RunA_part2_0, RunA_part2_1]
#RunB_part2 = [RunB_part2_0, RunB_part2_1]
#RunC_part2 = [RunC_part2_0, RunC_part2_1]
#RunD_part2 = [RunD_part2_0, RunD_part2_1]

#dataSamples = RunA_part2 + RunB_part2 + RunC_part2 + RunD_part2
                

samples = [MCBToKMuMu]


# ---------------------------------------------------------------------


if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
