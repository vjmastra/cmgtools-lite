import os, subprocess, sys
import re
from os import listdir
from os.path import isfile, join
from optparse import OptionParser
import numpy as np
import tarfile

if __name__ == "__main__":  
  parser = OptionParser()
  parser.add_option("-p", dest="mypath", default='output', type="str", help=" folder of grid results ")
  parser.add_option("--dirFilter", dest="dirFilter", default=None, type="str", help=" use only one folder to get results ")
  parser.add_option("--kwdIdentifier", dest="kwdIdentifier", default='Number of Events:', type="str", help=" word(s) which idecating the total sum of evts in log file. Default'Number of Events:' ")
  
  
  (options, args) = parser.parse_args()
  total=0
  for dirname, dirnames, filenames in os.walk(options.mypath):
    if "log" not in dirname: 
      continue;
    if "failed" in dirname:
      continue;
    if (options.dirFilter != None) and (options.dirFilter not in dirname):
      continue;
    print dirname
    dirtotal=0;
    for filename in filenames:
      tar = tarfile.open(dirname+"/"+filename, "r:gz")
      for name in tar.getnames():
        if "stdout" not in name: 
          continue
        member = tar.getmember(name)
        f = tar.extractfile(member)
        if f is not None:
         content = (f.read()).split()
         kwdId= options.kwdIdentifier.split()
         kwdCands= [i for i,c in enumerate(content) if c==kwdId[0] ]
         idx=-1;
         for kwdCand in kwdCands:
           i=0;
           while i<len(kwdId) and kwdId[i]==content[kwdCand+i]:
             i+=1;             
           if len(kwdId)==i:
             idx=kwdCand+i
             break
         if  idx>-1: 
            total+=float(content[idx])
            dirtotal+=float(content[idx])
         else: 
            print "kwdIdentifier not found in "+name+" Is it correct?"
    print "in this dir",dirtotal,"so far",total 
         
  print "Total ran on ",total,"evts"        
