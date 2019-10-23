import re, os, sys
from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions, doTestN, configureSplittingFromTime, cropToLumi
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
def byCompName(components, regexps):
    return [ c for c in components if any(re.match(r, c.name) for r in regexps) ]


from CMGTools.RootTools.samples.samples_13TeV_BParkingData_NanoAOD import samples as allData

from CMGTools.RootTools.samples.triggers_13TeV_BParking import all_triggers as triggers
  

DatasetsAndTriggers = []

# data
for dataset in ["RunA2018_part2_","RunB2018_part2_","RunC2018_part2_","RunD2018_part2_"]:
 for trg in ["mu9ipX"]:
  for num in ["0","1"]:
    DatasetsAndTriggers.append( (dataset+num, triggers[trg] ) )

#create components
dataSamples = []; vetoTriggers = []
for pd, trigs in DatasetsAndTriggers:
    print byCompName(allData, [pd])
    for comp in byCompName(allData, [pd]):
      comp.triggers = trigs[:]
      dataSamples.append(comp)
    

selectedComponents = dataSamples

# load codes
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from CMGTools.RKAnalysis.tools.nanoAOD.BParking_modules import *


modules = BParking_sequence


branchsel_in = os.environ['CMSSW_BASE']+"/src/CMGTools/RKAnalysis/cfg/branchRk_in.txt"

branchsel_out = os.environ['CMSSW_BASE']+"/src/CMGTools/RKAnalysis/cfg/branchRk_out.txt"

compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"


POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut = BParking_skim_cut, prefetch = True, longTermCache = True,
        branchsel = branchsel_in, outputbranchsel = branchsel_out, compression = compression)


