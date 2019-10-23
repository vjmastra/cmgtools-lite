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

#get datasets
from CMGTools.RootTools.samples.samples_13TeV_BParkingData_NanoAOD import samples as allData

#get triggers
from CMGTools.RootTools.samples.triggers_13TeV_BParking import all_triggers as triggers
  
test = getHeppyOption("test",None)


#create components
selectedComponents=[]
if not test:
  for comp in allData:
     #comp.triggers = trigs[:]
     # jobs per dataset
     comp.splitFactor = 10
     selectedComponents.append(comp)

if test:
   for comp in allData:
     if comp.name != test:
        continue
     comp.splitFactor = 5
     comp.files=comp.files[:10]
     selectedComponents.append(comp)

          

printSummary(selectedComponents)


# load codes
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# B parking modules
from CMGTools.RKAnalysis.tools.nanoAOD.BParking_modules import *


modules = BParking_sequence


# only read the branches in this file - for speed deactivate unescairy stuff
branchsel_in = os.environ['CMSSW_BASE']+"/src/CMGTools/RKAnalysis/cfg/branchRk_in.txt"

# only write the branches in this file in ADDITION of what is produce by module
branchsel_out = os.environ['CMSSW_BASE']+"/src/CMGTools/RKAnalysis/cfg/branchRk_out.txt"


compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"

# run the freaking thing
POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut = BParking_skim_cut, prefetch = True, longTermCache = True,
        branchsel = branchsel_in, outputbranchsel = branchsel_out, compression = compression)


