import os, subprocess, sys
import re
from os import listdir
from os.path import isfile, join
import argparse


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-p", dest="mypath", default='output', type=str, help="Main folder in eos that contains other folders ")
  parser.add_argument("-f","--eraFilter", dest="eraFilter", default=[],nargs='+', type=str, help="If only some folders needed, put them here ")
  parser.add_argument("-o","--outputName", dest="outputName", default='test', type=str, help="output name ")


  options = parser.parse_args()
  sampleNames=[]
  text="# COMPONENT CREATOR\nfrom CMGTools.RootTools.samples.ComponentCreator import ComponentCreator\nkreator = ComponentCreator()\n\n\n\n"
  for dirname, dirnames, filenames in os.walk(options.mypath):
    if '0000' not in dirnames: 
      continue
    words = dirname.split("/")
    filterCut=False
    if len(options.eraFilter)>0:
      filterCut=True
      for i in words:
        for kwd in options.eraFilter:
          if kwd in i:
            filterCut=False
    if filterCut:
       continue
    for word in words:
      if 'crab' not in word:
        continue;
      print words
      pth=""
      for i in range(3,len(words)):
        pth+="/"+words[i]
      for j in dirnames:
        pth2=pth+"/"+j+"/"
        text+="{name} = kreator.makeDataComponentFromEOS('{name}','{path}','.*root')\n".format(name=word+"_"+j,path=pth2)
        sampleNames.append(word+"_"+j)
 #   print text
#    print 
  text+="\n\nsamples = ["
  for sample in  sampleNames:
    if sample != sampleNames[-1]:
      text+=sample+","
    else:
      text+=sample+"] \n\n\n\n"

  text+='if __name__ == "__main__":\n\tfrom CMGTools.RootTools.samples.tools import runMain\n\trunMain(samples, localobjs=locals())'
  with open(options.outputName+".py",'w') as out:
     out.write(text)

