
def SkimCuts(Bdecay,Bcuts):
    BParking_skim_cut = ("Sum$( "+Bdecay+"_fit_pt>{ptmin} && "+Bdecay+
            "_fit_mass>{mmin} && "+Bdecay+"_fit_mass<{mmax} && "+Bdecay+"_l_xy_unc>0 && "+Bdecay+
            "_l_xy/"+Bdecay+"_l_xy_unc>{slxy} && "+Bdecay+
            "_fit_cos2D>{cos} && "+Bdecay+"_svprob>{prob} )>0"
            ).format(
    ptmin=Bcuts["Pt"], mmin=Bcuts["MinMass"], mmax=Bcuts["MaxMass"],
    slxy=Bcuts["LxySign"], cos=Bcuts["Cos2D"], prob=Bcuts["Prob"]   )
    return BParking_skim_cut


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
                            #triggerMuonId = "TriggerMuon_trgMuonIndex",
                            flat = False
    )   
    process.append(BSkim)
    return process

def KEEData ( process, cuts):
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionSkimmer import collectionSkimmer
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionEmbeder import collectionEmbeder
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
                             inputBranches = ["mvaId","isPF","isPFoverlap","isLowPt"],
                             embededBranches = ["e1mvaId","e1isPF","e1isPFoverlap","e1isLowPt"], 
                             embededCollIdx = "l1Idx"
    )
    El2 = collectionEmbeder( inputColl = "Electron",
                             embededColl = "SkimBToKEE",
                             inputBranches = ["mvaId","isPF","isPFoverlap","isLowPt"],
                             embededBranches = ["e2mvaId","e2isPF","e2isPFoverlap","e2isLowPt"],
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
                             lepCompositeIdxs = ["l1Idx","l2Idx"],
                             hadronCompositeIdxs = ["kIdx"],
                             lepMatchedRecoIdxs = ["recoMu1_Idx","recoMu2_Idx"],
                             hadronMatchedRecoIdxs = ["recoK_Idx"],
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
                                   daughtersPdgId = [13, -13, 321,-211],
                                   outputMomColl = "genB",
                                   interDecay = ["313->321,-211"],
                                   outputDaughterColls = ["genMu1","genMu2","genK","genPi"] 
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
   RecoPi = genRecoMatcher( recoInput="ProbeTracks",
                             genInput = "genPi",
                             output = "recoPi",
                             branches = ["pt","eta","phi"]
   )
   process.append(RecoPi)
   RecoB = compositeRecoMatcher(   compositeColl = "BToKsMuMu",
                             lepCompositeIdxs = ["l1_idx","l2_idx"],
                             hadronCompositeIdxs = ["trk1_idx","trk2_idx"],
                             lepMatchedRecoIdxs = ["recoMu1_Idx","recoMu2_Idx"],
                             hadronMatchedRecoIdxs = ["recoK_Idx","recoPi_Idx"],
                             outputColl = "recoB",
                             branches = ["pt","eta","phi"]
   )                                  
   process.append(RecoB)
   return process  

