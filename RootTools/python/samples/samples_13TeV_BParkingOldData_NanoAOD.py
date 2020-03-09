# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# ----------------------------- 2018 pp run  ----------------------------------------

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'

# ----------------------------- Run2018A 17Sep2018 ----------------------------------------
RunA_part2_0 = kreator.makeDataComponentFromEOS("RunA2018_part2_0", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2//crab_data_Run2018A_part2/190912_154729/0000/", ".*root")
RunA_part2_1 = kreator.makeDataComponentFromEOS("RunA2018_part2_1", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2//crab_data_Run2018A_part2/190912_154729/0001/", ".*root")
RunB_part2_0 = kreator.makeDataComponentFromEOS("RunB2018_part2_0", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018B_part2/190912_183627/0000/", ".*root")
RunB_part2_1 = kreator.makeDataComponentFromEOS("RunB2018_part2_1", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018B_part2/190912_183627/0001/", ".*root")
RunC_part2_0 = kreator.makeDataComponentFromEOS("RunC2018_part2_0", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018C_part2/190912_155245/0000/", ".*root")
RunC_part2_1 = kreator.makeDataComponentFromEOS("RunC2018_part2_1", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018C_part2/190912_155245/0001/", ".*root")
RunD_part2_0 = kreator.makeDataComponentFromEOS("RunD2018_part2_0", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018D_part2/190912_155004/0000/", ".*root")
RunD_part2_1 = kreator.makeDataComponentFromEOS("RunD2018_part2_1", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018D_part2/190912_155004/0001/", ".*root")
RunD_part2_2 = kreator.makeDataComponentFromEOS("RunD2018_part2_2", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018D_part2/190912_155004/0002/", ".*root")
RunD_part2_3 = kreator.makeDataComponentFromEOS("RunD2018_part2_3", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018D_part2/190912_155004/0003/", ".*root")
RunD_part2_4 = kreator.makeDataComponentFromEOS("RunD2018_part2_4", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018D_part2/190912_155004/0004/", ".*root")
RunD_part2_5 = kreator.makeDataComponentFromEOS("RunD2018_part2_5", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018D_part2/190912_155004/0005/", ".*root")
RunD_part2_6 = kreator.makeDataComponentFromEOS("RunD2018_part2_6", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018D_part2/190912_155004/0006/", ".*root")
RunD_part2_7 = kreator.makeDataComponentFromEOS("RunD2018_part2_7", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH2/crab_data_Run2018D_part2/190912_155004/0007/", ".*root")
RunA_part3_0 = kreator.makeDataComponentFromEOS("RunA2018_part3_0", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH3/crab_data_Run2018A_part3/190912_154846/0000/", ".*root")
RunA_part3_1 = kreator.makeDataComponentFromEOS("RunA2018_part3_1", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH3/crab_data_Run2018A_part3/190912_154846/0001/", ".*root")
RunB_part3_0 = kreator.makeDataComponentFromEOS("RunB2018_part3_0", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH3/crab_data_Run2018B_part3/190912_183750/0000/", ".*root")
RunB_part3_1 = kreator.makeDataComponentFromEOS("RunB2018_part3_1", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH3/crab_data_Run2018B_part3/190912_183750/0001/", ".*root")
RunC_part3_0 = kreator.makeDataComponentFromEOS("RunC2018_part3_0", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH3/crab_data_Run2018C_part3/190912_155407/0000/", ".*root")
RunC_part3_1 = kreator.makeDataComponentFromEOS("RunC2018_part3_0", "/store/cmst3/group/bpark/BParkingNANO_2019Sep12/ParkingBPH3/crab_data_Run2018C_part3/190912_155407/0001/", ".*root")



RunA_part2 = [RunA_part2_0, RunA_part2_1]
RunB_part2 = [RunB_part2_0, RunB_part2_1]
RunC_part2 = [RunC_part2_0, RunC_part2_1]
RunD_part2 = [RunD_part2_0, RunD_part2_1, RunD_part2_2, RunD_part2_3, RunD_part2_4, RunD_part2_5, RunD_part2_6, RunD_part2_7]
RunA_part3 = [RunA_part3_0, RunA_part3_1]
RunB_part3 = [RunB_part3_0, RunB_part3_1]
RunC_part3 = [RunC_part3_0, RunC_part3_1]

dataSamples = RunA_part2 + RunB_part2 + RunC_part2 + RunD_part2 + RunA_part3 + RunB_part3 + RunC_part3 #+ Kshort_RunA
                

samples = dataSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
