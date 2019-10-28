# condor usage: nanopy_batch.py -o <localOutput> -r /store/group/cmst3/group/bpark/gkaratha/<remoteOutput> -b 'run_condor_simple.sh -t 1200' run_RK_fromNanoAOD_cfg.py --option xxx=yyy
# local run: nanopy.py <folder>  run_RK_fromNanoAOD_cfg.py -N <evts per dataset> -o xxx=yyy


import re, os, sys
from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions, doTestN, configureSplittingFromTime, cropToLumi
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from CMGTools.RootTools.samples.configTools import *
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
import time


kreator = ComponentCreator()
def byCompName(components, regexps):
    return [ c for c in components if any(re.match(r, c.name) for r in regexps) ]


# parse options
filterSample = str(getHeppyOption("filterSample",""))
mc = getHeppyOption("mc",False)
data = getHeppyOption("data",False)
njobs = getHeppyOption("njobs",10)
kmumu = getHeppyOption("kmumu",False)
kstarmumu = getHeppyOption("kstarmumu",False)
kee = getHeppyOption("kee",False)
test = getHeppyOption("test")
start_time = time.time()


if (not data) and (not mc):
   data=True


#get triggers
from CMGTools.RootTools.samples.triggers_13TeV_BParking import all_triggers as triggers


# get datasets  
Ncomps=[]
if data:
  from CMGTools.RootTools.samples.samples_13TeV_BParkingData_NanoAOD import samples as allData
  Ncomps = allData
if mc:
  from CMGTools.RootTools.samples.samples_13TeV_BParkingMC_NanoAOD import samples as allMC
  Ncomps = Ncomps + allMC    



#create components
selectedComponents=[]
if not test:
  for comp in Ncomps:
     #comp.triggers = trigs[:]
     # jobs per dataset
     if filterSample!="":
        if filterSample not in comp.name:
           continue
     comp.splitFactor = njobs
     selectedComponents.append(comp)
else:
   for comp in Ncomps:
     comp.splitFactor = 1
     comp.files=comp.files[:3]
#     if filterSample != "":
#        print filterSample
     #if "KstarMuMu" not in comp.name:
      #     continue
     selectedComponents.append(comp)


# status
printSummary(selectedComponents)


# load main cmg code
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


# B parking code
from CMGTools.RKAnalysis.tools.nanoAOD.BParking_modules import *


BparkSkim = ""

modules = []

br_in = ""

# code loaded here just like in cmssw cfg
if kmumu and not mc:
  br_in = "branchRkmumu_in.txt"
  Bdecay="BToKMuMu"
  Bcuts=dict ( Pt= 5.0, MinMass=4.5, MaxMass=7.0, LxySign=2.0, Cos2D=0.9, Prob=0.1, L1Pt= -2.0, L2Pt= -1.0, KPt= -1.0 )
  BKLLSelection = lambda l : l.fit_pt > Bcuts["Pt" ] and l.fit_cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and l.l_xy/l.l_xy_unc > Bcuts["LxySign"] and l.fit_mass>Bcuts["MinMass"] and l.fit_mass<Bcuts["MaxMass"] and l.l1pt>Bcuts["L1Pt"]  and l.l2pt>Bcuts["L2Pt"]  and l.kpt>Bcuts["KPt"]
  BparkSkim= SkimCuts(Bdecay,Bcuts)
  modules = KMuMuData(modules,BKLLSelection)

if kee and not mc:
  br_in = "branchRkee_in.txt"
  Bdecay="BToKEE"
  Bcuts=dict ( Pt= 3.0, MinMass=4.7, MaxMass=6.0, LxySign=2.0, Cos2D=0.9, Prob=0.005, L1Pt= 2.0, L2Pt= 1.0, KPt= 1.0 )
  BKLLSelection = lambda l : l.fit_pt > Bcuts["Pt" ] and l.fit_cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and l.l_xy/l.l_xy_unc > Bcuts["LxySign"] and l.fit_mass>Bcuts["MinMass"] and l.fit_mass<Bcuts["MaxMass"] and l.l1pt>Bcuts["L1Pt"]  and l.l2pt>Bcuts["L2Pt"]  and l.kpt>Bcuts["KPt"]
  BparkSkim= SkimCuts(Bdecay,Bcuts)
  modules = KEEData(modules,BKLLSelection)  

if kmumu and mc:
  br_in = "branchRkmumu_in.txt"
  modules = KMuMuMC(modules)

if kstarmumu and mc:
  modules = KstarMuMuMC(modules)




#modules = 

# only read the branches in this file - for speed deactivate unescairy stuff
branchsel_in = os.environ['CMSSW_BASE']+"/src/CMGTools/RKAnalysis/cfg/"+br_in

# only write the branches in this file in ADDITION of what is produce by module
branchsel_out = os.environ['CMSSW_BASE']+"/src/CMGTools/RKAnalysis/cfg/branchRk_out.txt"


compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"

# run the freaking thing
POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut =  BparkSkim, prefetch = True, longTermCache = True,
        branchsel = branchsel_in, outputbranchsel = branchsel_out, compression = compression)
print("--- %s seconds ---" % (time.time() - start_time))

