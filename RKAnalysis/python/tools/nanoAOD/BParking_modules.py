################################## B selection ################################
#from CMGTools/RKAnalysis/cfg/run_RK_fromNanoAOD_cfg import Bcuts,Bdecay
#Bdecay="BToKMuMu" # name of collection we skimming eg BToKMuMu BToKEE

#Bcuts=dict ( Pt= 3.0, MinMass=4.7, MaxMass=5.7, LxySign=1.0, Cos2D=0.9, Prob=0.005, L1Pt= 2.0, L2Pt= 1.0, KPt= 1.0 )

#Bdecay="0"
#Bcuts=dict(py=0)

def setCollection( coll ):
    
    Bdecay = coll

def setBcuts( cuts ):
    Bcuts = custs

###############################  configuration for R_K #######################
DataKMuMu = True
DataKEE = False
MCKMuMu = False
##############################################################################
def SkimCuts(Bdecay,Bcuts):
    BParking_skim_cut = ("Sum$( "+Bdecay+"_fit_pt>{ptmin} && "+Bdecay+
            "_fit_mass>{mmin} && "+Bdecay+"_fit_mass<{mmax} && "+Bdecay+"_l_xy_unc>0 && "+Bdecay+
            "_l_xy/"+Bdecay+"_l_xy_unc>{slxy} && "+Bdecay+
            "_fit_cos2D>{cos} && "+Bdecay+"_svprob>{prob} )>0"
            ).format(
    ptmin=Bcuts["Pt"], mmin=Bcuts["MinMass"], mmax=Bcuts["MaxMass"],
    slxy=Bcuts["LxySign"], cos=Bcuts["Cos2D"], prob=Bcuts["Prob"]   )
    return BParking_skim_cut

#BParking_sequence = []

def KMuMuData ( process, cuts):
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionSkimmer import collectionSkimmer
    BSkim = collectionSkimmer(input = "BToKMuMu",
                            output = "SkimBToKMuMu",
                            importedVariables = ["Muon_pt","Muon_pt","ProbeTracks_pt"],
                            importIds = ["l1Idx","l2Idx","kIdx"],
                            varnames = ["l1pt","l2pt","kpt"],                   
                            selector = cuts,
                            branches = ["fit_pt","fit_mass","mass","l_xy",
                                        "l_xy_unc","fit_cos2D","svprob",
                                        "l1Idx","l2Idx","kIdx","fit_eta",
                                        "mll_fullfit","mll_raw","l1pt","l2pt",
                                        "kpt"],
                            triggerMuonId = "TriggerMuon_trgMuonIndex",
                            flat = False
    )   
    process.append(BSkim)
    return process

def KEEData ( process, cuts):
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionSkimmer import collectionSkimmer
    BSkim = collectionSkimmer(input = "BToKEE",
                            output = "SkimBToKEE",
                            importedVariables = ["Electron_pt","Electron_pt","ProbeTracks_pt"],
                            importIds = ["l1Idx","l2Idx","kIdx"],
                            varnames = ["l1pt","l2pt","kpt"],                   
                            selector = cuts,
                            branches = ["fit_pt","fit_mass","mass","l_xy",
                                        "l_xy_unc","fit_cos2D","svprob",
                                        "l1Idx","l2Idx","kIdx","fit_eta",
                                        "mll_fullfit","mll_raw","l1pt","l2pt",
                                        "kpt"],
                            flat = False
    )
    El1 = collectionEmbeder( inputColl = "Electron",
                             embededColl = "SkimBToKEE",
                             inputBranches = ["mvaId","isPF","isPFoverlap","isLowPt","unBiased","ptBiased"],
                             embededBranches = ["e1mvaId","e1isPF","e1isPFoverlap","e1isLowPt","e1unBiased","e1ptBiased"], 
                             embededCollIdx = "l1Idx"
    )
    El2 = collectionEmbeder( inputColl = "Electron",
                             embededColl = "SkimBToKEE",
                             inputBranches = ["mvaId","isPF","isPFoverlap","isLowPt","unBiased","ptBiased"],
                             embededBranches = ["e2mvaId","e2isPF","e2isPFoverlap","e2isLowPt","e2unBiased","e2ptBiased"],
                             embededCollIdx = "l2Idx"
    )
    process.append(BSkim)
    process.append(El1)
    process.append(El2)
    return process


def KMuMuMC (process):
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genDecayConstructor import genDecayConstructor
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genRecoMatcher import genRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.compositeRecoMatcher import compositeRecoMatcher
   GenDecay = genDecayConstructor( momPdgId = 521,
                                   daughtersPdgId = [13, -13, 321],
                                   outputMomColl = "genB",
                                   outputDaughterColls = ["genMu1","genMu2","genK"] 
    )                             
   process.append(GenDecay)   
   RecoMu1 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu1",
                             output = "recoMu1",
                             branches = ["pt","eta","phi"]
   )                             
   process.append(RecoMu1)
   RecoMu2 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu2",
                             output = "recoMu2",
                             branches = ["pt","eta","phi"]
   )                             
   process.append(RecoMu2)
   RecoK = genRecoMatcher( recoInput="ProbeTracks",
                             genInput = "genK",
                             output = "recoK",
                             branches = ["pt","eta","phi"]
   )                             
   process.append(RecoK)
   RecoB = compositeRecoMatcher(   compositeColl = "BToKMuMu",
                             compositeIdxs = ["l1Idx","l2Idx","kIdx"],
                             matchedIdxs = ["recoMu1_Idx","recoMu2_Idx","recoK_Idx"],
                             outputColl = "recoB",
                             branches = ["pt","eta","phi"]
   )                                  
   process.append(RecoB)
   return process  

def KstarMuMuMC (process):
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genDecayConstructor import genDecayConstructor
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genRecoMatcher import genRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.compositeRecoMatcher import compositeRecoMatcher
   GenDecay = genDecayConstructor( momPdgId = 511,
                                   daughtersPdgId = [13, -13, 321, -211],
                                   outputMomColl = "genB",
                                   outputDaughterColls = ["genMu1","genMu2","genK"] 
    )                             
   process.append(GenDecay)   
   RecoMu1 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu1",
                             output = "recoMu1",
                             branches = ["pt","eta","phi"]
   )                             
   process.append(RecoMu1)
   RecoMu2 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu2",
                             output = "recoMu2",
                             branches = ["pt","eta","phi"]
   )                             
   process.append(RecoMu2)
   RecoK = genRecoMatcher( recoInput="ProbeTracks",
                             genInput = "genK",
                             output = "recoK",
                             branches = ["pt","eta","phi"]
   )                             
   process.append(RecoK)
   RecoB = compositeRecoMatcher(   compositeColl = "BToKMuMu",
                             compositeIdxs = ["l1Idx","l2Idx","kIdx"],
                             matchedIdxs = ["recoMu1_Idx","recoMu2_Idx","recoK_Idx"],
                             outputColl = "recoB",
                             branches = ["pt","eta","phi"]
   )                                  
   process.append(RecoB)
   return process  







'''BKLLSelection = lambda l : l.pt > Bcuts["Pt" ] and l.cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and l.l_xy/l.l_xy_unc > Bcuts["LxySign"] and l.mass>Bcuts["MinMass"] and l.mass<Bcuts["MaxMass"] and l.l1pt>Bcuts["L1Pt"]  and l.l2pt>Bcuts["L2Pt"]  and l.kpt>Bcuts["KPt"]




BParking_sequence = []

if KMuMu:
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionSkimmer import collectionSkimmer
   BSkim = collectionSkimmer(input = "BToKMuMu",
                            output = "SkimBToKMuMu",
                            importedVariables = ["Muon_pt","Muon_pt","ProbeTracks_pt"],
                            importIds = ["l1Idx","l2Idx","kIdx"],
                            varnames = ["l1pt","l2pt","kpt"],                   
                            selector = BKLLSelection,
                            branches = ["fit_pt","fit_mass","mass","l_xy",
                                        "l_xy_unc","fit_cos2D","svprob",
                                        "l1Idx","l2Idx","kIdx","fit_eta",
                                        "mll_fullfit","mll_raw","l1pt","l2pt",
                                        "kpt"],
                            triggerMuonId = "TriggerMuon_trgMuonIndex",
                            flat = False
   )
   BParking_sequence.append(BSkim)


if KEE:
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionSkimmer import collectionSkimmer
   BSkim = collectionSkimmer(input = "BToKEE",
                            output = "SkimBToKEE",
                            selector = BKLLSelection,
                            branches = ["pt","mass","l_xy","l_xy_unc","cos2D",
                                        "svprob","l1Idx","l2Idx","kIdx","eta"],
   )

   BParking_sequence.append(BSkim)
   
   
if MCKMuMu:
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genDecayConstructor import genDecayConstructor
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genRecoMatcher import genRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.compositeRecoMatcher import compositeRecoMatcher
   GenDecay = genDecayConstructor( momPdgId = 521,
                                   daughtersPdgId = [13, -13, 321],
                                   outputMomColl = "genB",
                                   outputDaughterColls = ["genMu1","genMu2","genK"] 
    )                             
   BParking_sequence.append(GenDecay)   
   RecoMu1 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu1",
                             output = "recoMu1",
                             branches = ["pt","eta","phi"]
   )                             
   BParking_sequence.append(RecoMu1)
   RecoMu2 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu2",
                             output = "recoMu2",
                             branches = ["pt","eta","phi"]
   )                             
   BParking_sequence.append(RecoMu2)
   RecoK = genRecoMatcher( recoInput="ProbeTracks",
                             genInput = "genK",
                             output = "recoK",
                             branches = ["pt","eta","phi"]
   )                             
   BParking_sequence.append(RecoK)
   RecoB = compositeRecoMatcher(   compositeColl = "BToKMuMu",
                             compositeIdxs = ["l1Idx","l2Idx","kIdx"],
                             matchedIdxs = ["recoMu1_Idx","recoMu2_Idx","recoK_Idx"],
                             outputColl = "recoB",
                             branches = ["pt","eta","phi"]
   )                                  
   BParking_sequence.append(RecoB)
'''
