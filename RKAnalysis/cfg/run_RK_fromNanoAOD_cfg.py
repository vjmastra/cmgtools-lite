# condor usage: nanopy_batch.py -o <localOutput> -r <remoteOutput> -b 'run_condor_simple.sh -t 1200' run_RK_fromNanoAOD_cfg.py 
# local run: nanopy.py <folder>  run_RK_fromNanoAOD_cfg.py -N <evts per dataset>

import re, os, sys
from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions, doTestN, configureSplittingFromTime, cropToLumi
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from CMGTools.RootTools.samples.configTools import *
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

kreator = ComponentCreator()
def byCompName(components, regexps):
    return [ c for c in components if any(re.match(r, c.name) for r in regexps) ]

# parse options
test = getHeppyOption("test")
filterSample = getHeppyOption("filterSample")
mc = getHeppyOption("mc",False)
njobs = getHeppyOption("njobs",10)
kmumu = getHeppyOption("kmumu",False)
kee = getHeppyOption("kee",False)


#get triggers
from CMGTools.RootTools.samples.triggers_13TeV_BParking import all_triggers as triggers

# get datasets  
Ncomps=[]
if not mc:
  from CMGTools.RootTools.samples.samples_13TeV_BParkingData_NanoAOD import samples as allData
  Ncomps = allData
else:
  from CMGTools.RootTools.samples.samples_13TeV_BParkingMC_NanoAOD import samples as allMC
  Ncomps = allMC    


#create components
selectedComponents=[]
if not test:
  for comp in Ncomps:
     #comp.triggers = trigs[:]
     # jobs per dataset
     if filterSample:
        if filterSample not in comp:
           continue
     comp.splitFactor = njobs
     selectedComponents.append(comp)
else:
   for comp in Ncomps:
     comp.splitFactor = 1
     comp.files=comp.files[:3]
     if filterSample:
        if filterSample not in comp:
           continue
     selectedComponents.append(comp)

          
# status
printSummary(selectedComponents)


# load main cmg code
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# B parking code
from CMGTools.RKAnalysis.tools.nanoAOD.BParking_modules import *

BparkSkim = ""


modules = []

# code loaded here just like in cmssw cfg
if kmumu and not mc:
  Bdecay="BToKMuMu"
  Bcuts=dict ( Pt= 3.0, MinMass=4.7, MaxMass=5.7, LxySign=1.0, Cos2D=0.9, Prob=0.005, L1Pt= 2.0, L2Pt= 1.0, KPt= 1.0 )
  BKLLSelection = lambda l : l.pt > Bcuts["Pt" ] and l.cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and l.l_xy/l.l_xy_unc > Bcuts["LxySign"] and l.mass>Bcuts["MinMass"] and l.mass<Bcuts["MaxMass"] and l.l1pt>Bcuts["L1Pt"]  and l.l2pt>Bcuts["L2Pt"]  and l.kpt>Bcuts["KPt"]
  BparkSkim= SkimCuts(Bdecay,Bcuts)
  modules = KMuMuData(modules,BKLLSelection)

if kee and not mc:
  Bdecay="BToKEE"
  Bcuts=dict ( Pt= 3.0, MinMass=4.7, MaxMass=5.7, LxySign=1.0, Cos2D=0.9, Prob=0.005, L1Pt= 2.0, L2Pt= 1.0, KPt= 1.0 )
  BKLLSelection = lambda l : l.pt > Bcuts["Pt" ] and l.cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and l.l_xy/l.l_xy_unc > Bcuts["LxySign"] and l.mass>Bcuts["MinMass"] and l.mass<Bcuts["MaxMass"] and l.l1pt>Bcuts["L1Pt"]  and l.l2pt>Bcuts["L2Pt"]  and l.kpt>Bcuts["KPt"]
  BparkSkim= SkimCuts(Bdecay,Bcuts)
  modules = KEEData(modules,BKLLSelection)  

if kmumu and mc:
  modules = KMuMuMC(modules)


#modules = 





# only read the branches in this file - for speed deactivate unescairy stuff
branchsel_in = os.environ['CMSSW_BASE']+"/src/CMGTools/RKAnalysis/cfg/branchRk_in.txt"

# only write the branches in this file in ADDITION of what is produce by module
branchsel_out = os.environ['CMSSW_BASE']+"/src/CMGTools/RKAnalysis/cfg/branchRk_out.txt"


compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"

# run the freaking thing
POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut =  BparkSkim, prefetch = True, longTermCache = True,
        branchsel = branchsel_in, outputbranchsel = branchsel_out, compression = compression)


