
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
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionEmbeder import collectionEmbeder
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.branchCreator import branchCreator
    BSkim = collectionSkimmer(input = "BToKMuMu",
                            output = "SkimBToKMuMu",
#                            importedVariables = ["Muon_pt","Muon_pt","ProbeTracks_pt",""],
#                            importIds = ["l1Idx","l2Idx","kIdx"],
#                            varnames = ["l1pt","l2pt","kpt"],                  
                            selector = cuts,
                            branches = ["fit_pt","fit_mass","mass","l_xy",
                                        "l_xy_unc","fit_cos2D","svprob",
                                        "l1Idx","l2Idx","kIdx","fit_eta",
                                        "mll_fullfit"],
                            exclTriggerMuonId = "TriggerMuon_trgMuonIndex",
                            #selTriggerMuonId = "TriggerMuon_trgMuonIndex",
                            flat = False
    )   
    process.append(BSkim)
    Mu1 = collectionEmbeder( inputColl = "Muon",
                             embededColl = "SkimBToKMuMu",
                             inputBranches = ["pt","eta","phi","softId","vz","pfRelIso03_all"],
                             embededBranches = ["mu1Pt","mu1Eta","mu1Phi","mu1SoftId","mu1Vz","mu1iso"], 
                             embededCollIdx = "l1Idx"
    )
    process.append(Mu1)
    Mu2 = collectionEmbeder( inputColl = "Muon",
                             embededColl = "SkimBToKMuMu",
                             inputBranches = ["pt","eta","phi","softId","vz","pfRelIso03_all"],
                             embededBranches = ["mu2Pt","mu2Eta","mu2Phi","mu2SoftId","mu2Vz","mu2iso"], 
                             embededCollIdx = "l2Idx"
    )
    process.append(Mu2)
    K = collectionEmbeder( inputColl = "ProbeTracks",
                             embededColl = "SkimBToKMuMu",
                             inputBranches = ["pt","eta","phi","vz"],
                             embededBranches = ["kPt","kEta","kPhi","kVz"],  
                             embededCollIdx = "kIdx"
    )
    process.append(K)
    CreateVars = branchCreator(
      collection="SkimBToKMuMu",
        inputBranches=[["l_xy","l_xy_unc"],["mu1Vz","mu2Vz"],["kVz","mu1Vz","mu2Vz"],["mu1Eta","mu1Phi","mu2Eta","mu2Phi"],["kEta","kPhi","mu1Eta","mu1Phi","mu2Eta","mu2Phi"]],
        operation=["{0}/{1}","abs({0}-{1})","min(abs({0}-{1}),abs({0}-{2}))","deltaR({0},{1},{2},{3})","min( deltaR({0},{1},{2},{3}),deltaR({0},{1},{3},{4}))"],
        createdBranches=["l_xy_sig","mu1mu2Dz","muKDz","mu1mu2Dr","muKDr"]
    )
    process.append(CreateVars)
    return process

def KEEData ( process, cuts,usePF,useLowPtE):
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionSkimmer import collectionSkimmer
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionEmbeder import collectionEmbeder
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.branchCreator import branchCreator
    cuts2 =cuts
    if usePF and not useLowPtE:
      cuts2= cuts and (lambda l: l.e1isPF == 1 and l.e2isPF == 1)
    elif not usePF and useLowPtE:
      cuts2 =cuts and (lambda l: l.e1isPF == 0 and l.e2isPF == 0)
    BSkim = collectionSkimmer(input = "BToKEE",
                            output = "SkimBToKEE",
                            importedVariables = ["Electron_isPF","Electron_isPF"],
                            importIds = ["l1Idx","l2Idx"],
                            varnames = ["e1isPF","e2isPF"],                   
                            selector = cuts2,
                            branches = ["fit_pt","fit_mass","mass","l_xy",
                                        "l_xy_unc","fit_cos2D","svprob",
                                        "l1Idx","l2Idx","kIdx","fit_eta",
                                        "mll_fullfit"],
                            flat = False
    )
    process.append(BSkim)
    El1 = collectionEmbeder( inputColl = "Electron",
                             embededColl = "SkimBToKEE",
                             inputBranches = ["mvaId","isPF","pt","eta","phi","fBrem","hoe","vz"],
                             embededBranches = ["e1mvaId","e1isPF","e1Pt","e1Eta","e1Phi","e1fBrem","e1hoe","e1Vz"], 
                             embededCollIdx = "l1Idx"
    )
    process.append(El1)
    El2 = collectionEmbeder( inputColl = "Electron",
                             embededColl = "SkimBToKEE",
                             inputBranches = ["mvaId","isPF","pt","eta","phi","fBrem","hoe","vz"],
                             embededBranches = ["e2mvaId","e2isPF","e2Pt","e2Eta","e2Phi","e2fBrem","e2hoe","e2Vz"],
                             embededCollIdx = "l2Idx"
    )
    process.append(El2)
    K = collectionEmbeder( inputColl = "ProbeTracks",
                           embededColl = "SkimBToKEE",
                           inputBranches = ["pt","eta","phi","vz"],
                           embededBranches = ["kPt","kEta","kPhi","kVz"],
                           embededCollIdx = "kIdx"
    )
    process.append(K)
    CreateVars = branchCreator(
        collection="SkimBToKEE",
        inputBranches=[["l_xy","l_xy_unc"],["e1Vz","e2Vz"],["kVz","e1Vz","e2Vz"],["e1Eta","e1Phi","e2Eta","e2Phi"],["kEta","kPhi","e1Eta","e1Phi","e2Eta","e2Phi"]],
        operation=["{0}/{1}","abs({0}-{1})","min(abs({0}-{1}),abs({0}-{2}))","deltaR({0},{1},{2},{3})","min( deltaR({0},{1},{2},{3}),deltaR({0},{1},{3},{4}))"],
        createdBranches=["l_xy_sig","e1e2Dz","eKDz","e1e2Dr","eKDr"]
    )
    process.append(CreateVars)
    return process


def KMuMuMC (process,Jpsi=[]):
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genDecayConstructorPython import genDecayConstructorPython
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genRecoMatcher import genRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.compositeRecoMatcher import compositeRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.branchCreatorMC import branchCreatorMC
   GenDecay = genDecayConstructorPython( momPdgId = 521,
                                   daughtersPdgId = [13, -13, 321],
                                   outputMomColl = "genB",
                                   intermediateDecay = Jpsi,
                                   trgMuonPtEtaThresholds = [7,1.5], #was 7,1.6
                                   selectTrgMuon = False,
                                   excludeTrgMuon = True,
                                   outputDaughterColls = ["genMu1","genMu2","genK"] 
    )                             
   process.append(GenDecay)   
   RecoMu1 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu1",
                             output = "recoMu1",
                             branches = ["pt","eta","phi","softId","vz","pfRelIso03_all"],
                             skipNotMatched=False
   )                             
   process.append(RecoMu1)
   RecoMu2 = genRecoMatcher( recoInput="Muon",
                             genInput = "genMu2",
                             output = "recoMu2",
                             branches = ["pt","eta","phi","softId","vz","pfRelIso03_all"],
                             skipNotMatched=False
   )                             
   process.append(RecoMu2)
   RecoK = genRecoMatcher( recoInput="ProbeTracks",
                             genInput = "genK",
                             output = "recoK",
                             branches = ["pt","eta","phi","vz"],
                             skipNotMatched=False
   )                             
   process.append(RecoK)
   RecoB = compositeRecoMatcher(   compositeColl = "BToKMuMu",
                             lepCompositeIdxs = ["l1Idx","l2Idx"],
                             hadronCompositeIdxs = ["kIdx"],
                             lepMatchedRecoIdxs = ["recoMu1_Idx","recoMu2_Idx"],
                             hadronMatchedRecoIdxs = ["recoK_Idx"],
                             outputColl = "recoB",
                             branches = ["fit_pt","fit_eta","fit_phi","fit_mass","mll_fullfit","l_xy","l_xy_unc","fit_cos2D","svprob","l1Idx","l2Idx","kIdx"]
   )                                  
   process.append(RecoB)
   CreateVars = branchCreatorMC(
      inputBranches=[["recoB_l_xy","recoB_l_xy_unc"], ["recoMu1_vz","recoMu2_vz"], ["recoK_vz","recoMu1_vz","recoMu2_vz"], ["recoMu1_eta","recoMu1_phi","recoMu2_eta","recoMu2_phi"], ["recoK_eta","recoK_phi","recoMu1_eta","recoMu1_phi","recoMu2_eta","recoMu2_phi"] ],
      operation=["{0}/{1}","abs({0}-{1})","min(abs({0}-{1}),abs({0}-{2}))","deltaR({0},{1},{2},{3})","min(deltaR({0},{1},{2},{3}),deltaR({0},{1},{4},{5}))"],
      createdBranches=["recoB_l_xy_sig","recoB_mu1mu2Dz","recoB_muKDz","recoB_mu1mu2Dr","recoB_muKDr"]
    )
   process.append(CreateVars)
   return process  


def KEEMC (process,Jpsi=[]):
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genDecayConstructorPython import genDecayConstructorPython
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.genRecoMatcher import genRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.compositeRecoMatcher import compositeRecoMatcher
   from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.branchCreatorMC import branchCreatorMC
   GenDecay = genDecayConstructorPython( momPdgId = 521,
                                   daughtersPdgId = [11, -11, 321],
                                   outputMomColl = "genB",
                                   intermediateDecay = Jpsi,
                                   trgMuonPtEtaThresholds = [], #was 7,1.6
                                   selectTrgMuon = False,
                                   excludeTrgMuon = False,
                                   outputDaughterColls = ["genE1","genE2","genK"] 
    )                             
   process.append(GenDecay)   
   RecoE1 = genRecoMatcher( recoInput="Electron",
                             genInput = "genE1",
                             output = "recoE1",
                             branches = ["pt","eta","phi","fBrem","vz","hoe"],
                             skipNotMatched=False
   )                             
   process.append(RecoE1)
   RecoE2 = genRecoMatcher( recoInput="Electron",
                             genInput = "genE2",
                             output = "recoE2",
                             branches = ["pt","eta","phi","fBrem","vz","hoe"],
                             skipNotMatched=False
   )                             
   process.append(RecoE2)
   RecoK = genRecoMatcher( recoInput="ProbeTracks",
                             genInput = "genK",
                             output = "recoK",
                             branches = ["pt","eta","phi","vz"],
                             skipNotMatched=False
   )                             
   process.append(RecoK)
   RecoB = compositeRecoMatcher(   compositeColl = "BToKEE",
                             lepCompositeIdxs = ["l1Idx","l2Idx"],
                             hadronCompositeIdxs = ["kIdx"],
                             lepMatchedRecoIdxs = ["recoE1_Idx","recoE2_Idx"],
                             hadronMatchedRecoIdxs = ["recoK_Idx"],
                             outputColl = "recoB",
                             branches = ["fit_pt","fit_eta","fit_phi","fit_mass","mll_fullfit","l_xy","l_xy_unc","fit_cos2D","svprob","l1Idx","l2Idx","kIdx"]
   )                                  
   process.append(RecoB)
   CreateVars = branchCreatorMC(
      inputBranches=[["recoB_l_xy","recoB_l_xy_unc"], ["recoE1_vz","recoE2_vz"], ["recoK_vz","recoE1_vz","recoE2_vz"], ["recoE1_eta","recoE1_phi","recoE2_eta","recoE2_phi"], ["recoK_eta","recoK_phi","recoE1_eta","recoE1_phi","recoE2_eta","recoE2_phi"] ],
      operation=["{0}/{1}","abs({0}-{1})","min(abs({0}-{1}),abs({0}-{2}))","deltaR({0},{1},{2},{3})","min(deltaR({0},{1},{2},{3}),deltaR({0},{1},{4},{5}))"],
      createdBranches=["recoB_l_xy_sig","recoB_e1e2Dz","recoB_eKDz","recoB_e1e2Dr","recoB_eKDr"]
    )
   process.append(CreateVars)
   return process  




########################################### B->K*ll #########################

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



################################### Kshort LL #################################
def KshortMuMuData ( process, cuts):
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionSkimmer import collectionSkimmer
    from PhysicsTools.NanoAODTools.postprocessing.modules.bpark.collectionEmbeder import collectionEmbeder
    BSkim = collectionSkimmer(input = "BToKshortMuMu",
                            output = "SkimBToKshortMuMu",
                            importedVariables = ["Kshort_svprob"],
                            importIds = ["kshort_idx"],
                            varnames = ["kshort_prob"],
                            selector = cuts,
                            branches = [ #B vars
                                        "fit_pt","fit_mass","fit_eta","fit_phi",
                                        "l_xy","l_xy_unc","fit_cos2D","svprob",
                                         # lep 
                                        "mll_fullfit","lep1pt_fullfit", 
                                        "lep1eta_fullfit","lep2pt_fullfit", 
                                        "lep2eta_fullfit","l1_idx", "l2_idx",
                                        # kshort
                                        "ptkshort_fullfit", "etakshort_fullfit",
                                        "mkshort_fullfit", "kshort_idx",
                                        "kshort_prob"
                                       ],
                   #         triggerMuonId = "TriggerMuon_trgMuonIndex",
                            flat = False
    )   
    process.append(BSkim)
    Mu1 = collectionEmbeder( inputColl = "Muon",
                             embededColl = "SkimBToKshortMuMu",
                             inputBranches = ["softMvaId","softId","triggerIdLoose"],
                             embededBranches = ["lep1softMvaId","lep1softId","lep1trigger"], 
                             embededCollIdx = "l1_idx"
    )
    Mu2 = collectionEmbeder( inputColl = "Muon",
                             embededColl = "SkimBToKshortMuMu",
                             inputBranches = ["softMvaId","softId","triggerIdLoose"],
                             embededBranches = ["lep2softMvaId","lep2softId","lep2trigger"], 
                             embededCollIdx = "l2_idx"
    )
    Kshort = collectionEmbeder( inputColl = "Kshort",
                             embededColl = "SkimBToKshortMuMu",
                             inputBranches = ["trk1_pt","trk2_pt"],
                             embededBranches = ["trk1pt","trk2pt"], 
                             embededCollIdx = "kshort_idx"
    )
    process.append(Mu1)
    process.append(Mu2)    
    process.append(Kshort)
    return process
