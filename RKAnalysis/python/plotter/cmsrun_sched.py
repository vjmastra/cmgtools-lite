import os
import os.path
import multiprocessing as mp



def f(x):
  #args=x.split("_")
  print "1"
  #os.system("cmsRun step3_PAT.py sample="+lfile+" name=pat_"+out


if __name__ == "__main__":
  listfiles=[]

  for dirpath, dirnames, filenames in os.walk("/eos/cms//store/group/cmst3/user/gkaratha/FastSim_BToMuMuX_2/BToMuMuX/CRAB3_fastsim/191104_235955/0000/"):
    for filename in [f for f in filenames if f.endswith(".root")]:
      listfiles.append(os.path.join(dirpath, filename))

  for dirpath, dirnames, filenames in os.walk("/eos/cms/store/group/cmst3/user/gkaratha/FastSim_BToMuMuX/BToMuMuX/CRAB3_fastsim/191104_145633/0000/"):
    for filename in [f for f in filenames if f.endswith(".root")]:
       listfiles.append(os.path.join(dirpath, filename))


  ifile=0
  while ifile <len(listfiles)-mp.cpu_count():
    jobs=[]
    print ifile
    for i in range(0,mp.cpu_count()):
       print "  ",ifile
       temp=listfiles[ifile]+";"+str(ifile)
       jobs.append(temp)
       ifile+=1
    p = mp.Pool(1)
    print type(jobs)
    jobs=['/eos/cms//store/group/cmst3/user/gkaratha/FastSim_BToMuMuX_2/BToMuMuX/CRAB3_fastsim/191104_235955/0000/BToMuMuX_1.root;0']
    p.map(f,['/eos/cms//store/group/cmst3/user/gkaratha/FastSim_BToMuMuX_2/BToMuMuX/CRAB3_fastsim/191104_235955/0000/BToMuMuX_1.root;0','/eos/cms//store/group/cmst3/user/gkaratha/FastSim_BToMuMuX_2/BToMuMuX/CRAB3_fastsim/191104_235955/0000/BToMuMuX_1.root;0'])
