# condor usage: nanopy_batch.py -o <localOutput> -r /store/group/cmst3/user/gkaratha/<remoteOutput> -b 'run_condor_simple.sh -t 1200' run_RK_fromNanoAOD_cfg.py --option xxx=yyy
# /store/group/cmst3/user/gkaratha
# /store/group/cmst3/group/bpark/gkaratha/
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
nfiles = getHeppyOption("nfiles",1)
kmumu = getHeppyOption("kmumu",False)
kstarmumu = getHeppyOption("kstarmumu",False)
kshortmumu = getHeppyOption("kshortmumu",False)
kee = getHeppyOption("kee",False)
onlyPFe = getHeppyOption("onlyPFe",False)
jpsi = getHeppyOption("jpsi",False)
psi2s = getHeppyOption("psi2s",False)
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
  if kee:
    from CMGTools.RootTools.samples.samples_13TeV_BParkingDataPFe_NanoAOD import samples as allData
    Ncomps = allData
if mc:
  from CMGTools.RootTools.samples.samples_13TeV_BParkingMC_NanoAOD import samples as allMC
  Ncomps = allMC    
  if kee:
    from CMGTools.RootTools.samples.samples_13TeV_BParkingMCPFe_NanoAOD import samples as allData
    Ncomps = allData


print Ncomps[0].files
#create components
selectedComponents=[]
if not test:
  for comp in Ncomps:
     if filterSample!="":
        if filterSample not in comp.name:
           continue
     comp.splitFactor = int(njobs)
     selectedComponents.append(comp)

else:
   for comp in Ncomps:
     if filterSample!="":
        if filterSample not in comp.name:
           continue
     comp.splitFactor = 1
     comp.files=comp.files[:int(nfiles)]
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
  # tag cuts
 # Bcuts=dict ( Pt= 10.5, MinMass=4.7, MaxMass=6.0, LxySign=1.0, Cos2D=0.99, Prob=0.001, L1Pt= 7.2, L2Pt= 1.0, KPt= 1.0 )
  # probe cuts 
  Bcuts=dict ( Pt= 3.0, MinMass=4.7, MaxMass=6.0, LxySign=1.0, Cos2D=0.99, Prob=0.001, L1Pt= 1.0, L2Pt= 1.0, KPt= 1.0 )
  BKLLSelection = lambda l : l.fit_pt > Bcuts["Pt" ] and l.fit_cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and (l.l_xy)/l.l_xy_unc > Bcuts["LxySign"] and l.fit_mass>Bcuts["MinMass"] and l.fit_mass<Bcuts["MaxMass"] 
  modules = KMuMuData(modules,BKLLSelection)

if kee and not mc:
  br_in = "branchRkee_in.txt"
  Bdecay="BToKEE"
  EnableLowPtE=True
  EnablePFE=True
  if onlyPFe: EnableLowPtE=False
  Bcuts=dict ( Pt= 3.0, MinMass=4.7, MaxMass=6.0, LxySign=0.0, Cos2D=0, Prob=0, L1Pt= 1.0, L2Pt= 1.0, KPt= 0.0 )
  BKLLSelection = lambda l : l.fit_pt > Bcuts["Pt" ] and l.fit_cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and (l.l_xy)/l.l_xy_unc > Bcuts["LxySign"] and l.fit_mass>Bcuts["MinMass"] and l.fit_mass<Bcuts["MaxMass"]
  if not EnableLowPtE and not EnablePFE: print "Neither PF e nor low pt e enabled. Results may be invalid"
  modules = KEEData(modules,BKLLSelection,EnablePFE,EnableLowPtE) 


#################################### KsLL ###################################
if kshortmumu and not mc:
  br_in = "branchRkshortMuMu_in.txt"
  
  Bcuts=dict ( Pt= 3.0, MinMass=4.7, MaxMass=5.7, LxySign=1.0, Cos2D=0.9, Prob=0.005, L1Pt= 1.5, L2Pt=1.0, KsPt=1.0, KsProb=0.0005 )
  

  BKLLSelection = lambda l : l.fit_pt > Bcuts["Pt" ] and l.fit_cos2D > Bcuts["Cos2D"] and l.svprob > Bcuts["Prob"] and l.l_xy_unc >0 and l.l_xy/l.l_xy_unc > Bcuts["LxySign"] and l.fit_mass>Bcuts["MinMass"] and l.fit_mass<Bcuts["MaxMass"] and l.lep1pt_fullfit>Bcuts["L1Pt"]  and l.lep2pt_fullfit>Bcuts["L2Pt"]  and l.ptkshort_fullfit>Bcuts["KsPt"] and l.kshort_prob>Bcuts["KsProb"]

  BparkSkim = ("Sum$( BToKshortMuMu_fit_pt>{ptmin} && "+
                    "BToKshortMuMu_fit_mass>{mmin} && "+
                    "BToKshortMuMu_fit_mass<{mmax} && "+
                    "BToKshortMuMu_l_xy_unc>0 && "+
                    "BToKshortMuMu_l_xy/BToKshortMuMu_l_xy_unc>{slxy} && "+
                    "BToKshortMuMu_fit_cos2D>{cos} && "+
                    "BToKshortMuMu_svprob>{prob} && "+
                    "BToKshortMuMu_lep1pt_fullfit>{l1pt} && "+
                    "BToKshortMuMu_lep2pt_fullfit>{l2pt} && "+
                    "BToKshortMuMu_ptkshort_fullfit>{kspt} "+
                   ")>0"
               ).format( ptmin=Bcuts["Pt"], mmin=Bcuts["MinMass"], 
                         mmax=Bcuts["MaxMass"], slxy=Bcuts["LxySign"], 
                         cos=Bcuts["Cos2D"], prob=Bcuts["Prob"], 
                         l1pt=Bcuts["L1Pt"], l2pt=Bcuts["L2Pt"], 
                         kspt=Bcuts["KsPt"]
                        )
            
  modules = KshortMuMuData(modules,BKLLSelection)  

if kmumu and mc:
  br_in = "branchRkmumu_in.txt"
  if not jpsi and not psi2s:
     modules = KMuMuMC(modules)
  elif jpsi and not psi2s:
     modules = KMuMuMC(modules,["443->13,-13"])
  elif not jpsi and psi2s:
     modules = KMuMuMC(modules,["100443->13,-13"])
  BparkSkim=""

if kee and mc:
  br_in = "branchRkee_in.txt"
  if not jpsi and not psi2s:
     modules = KEEMC(modules)
  elif jpsi and not psi2s:
     modules = KEEMC(modules,["443->11,-11"])
  elif not jpsi and psi2s:
     modules = KEEMC(modules,["100443->11,-11"])
  BparkSkim=""

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

