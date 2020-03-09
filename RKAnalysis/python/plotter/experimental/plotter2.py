import os, subprocess 
from optparse import OptionParser
import multiprocessing as mp
from ROOT import *
import time;



def f(x):
  args = x.split(";")
  print x
  qt= "\",\""
  os.system(  "root -l -b -q 'PlottingCore/plotSimple2.C(\""+args[0]+qt+args[1]+qt+args[2]+qt+args[3]+qt+args[4]+"\")'"   )
  print "core",(args[1].split("_"))[1],"done"


def transform( heff, kwds):
      
   for kwd in kwds:     
     value = kwd.split("=")

     if value[0]=="LineColor":
        heff.SetLineColor(float(value[1]))

     if value[0]=="LineWidth": 
        heff.SetLineWidth(float(value[1]))

     if value[0]=="XLabelSize":
        heff.GetXaxis().SetTitleSize(float(value[1]));     

     if value[0]=="YLabelSize":
        heff.GetYaxis().SetTitleSize(float(value[1]));
     if value[0]=="YTitle":
        heff.GetYaxis().SetTitle(value[1]);
   return heff



def legPos( options):
  default= (0.7,0.7,0.9,0.9)
  newpos=0
  for option in options:
    if not "LegPos" in option :
       continue;
    pos = (option.split("=") )[1]
    if pos =="BL":
      newpos=(0.1,0.1,0.3,0.3)
    elif pos  =="BR":
      newpos=(0.7,0.1,0.9,0.3) 
    elif pos =="TL":
      newpos= (0.1,0.7,0.3,0.9)
    elif pos  =="TR":
      newpos= (0.7,0.7,0.9,0.9) 

  if newpos ==0:
     return default; 
  else:
     return newpos





def legName( options,default):
  name=default
  for option in options:
    if "LegName" in option:
      name = (option.split("="))[1]
  return name
    


def cms():
  cms_label = TLatex()
  cms_label.SetTextSize(0.04)
  cms_label.DrawLatexNDC(0.16, 0.96, "#bf{ #font[22]{CMS} #font[72]{Preliminary}}")
  return cms_label



def head():
  header = TLatex()
  header.SetTextSize(0.03)
  header.DrawLatexNDC(0.63, 0.96, "#sqrt{s} = 13 TeV, 2018 p-p ")
  return header




cppcode="""
  #include "PlottingCore/plot_tool.h"
  class cosmetics{
    public:
     cosmetics(TH1F* h1, std::string kwds){
       cout<<kwds<<endl;
//       transform((&h1),kwds);
     }
  }


"""



if __name__ == "__main__":

    # availiable plotting options
    parser = OptionParser()

    parser.add_option("-p","--plotsTxtFile", dest="plotfile",   default="plots.txt", type="string", help="txt with selected plots and cuts")

    parser.add_option("-t","--type", dest="script", default="SimplePlots", type="choice",choices= ['EfficiencyPlots','SimplePlots'], help="plotter type choices: EfficiencyPlots or SimplePlots")

    parser.add_option("-i","--inputData" ,dest="inputData",  default="mca.txt", type="string", help="txt with root files to run on. By default running on mca.txt")

    parser.add_option("-o","--outputDir",dest="outputDir",  default="Plots_Date", type="string", help="folder name to save plots. Default=Plots_Date")

    parser.add_option("-f","--forceRewrite",dest="rewriteOutDir",  default=False,action='store_true', help="if the outputDir exists, this rewrites it (previous deleted)")

    parser.add_option("-n","--ncore",dest="ncore",type="int",  default=-1, help="number of cores to use. -1 uses all")

    parser.add_option("--tree",dest="tree",  default="Events", type="string", help="tree name. Default Events")

    (options, args) = parser.parse_args()

    if  os.path.exists(options.outputDir) and options.rewriteOutDir:
        os.system("rm -r "+options.outputDir)

     #  create output folder to save plots
    if options.outputDir=="Plots_Date":
      localtime = time.asctime( time.localtime(time.time()) )
      options.outputDir = "Plots_{0}".format(localtime.replace(" ","_"))
      options.outputDir = options.outputDir.replace(":","_")
      os.system(  "mkdir -p "+options.outputDir )
      print "plots will be saved at "+options.outputDir
      
    else:
      print "plots will be saved at "+options.outputDir
      if not os.path.exists(options.outputDir):    
         os.makedirs(options.outputDir)
      else:
         num1=0
         while os.path.exists(options.outputDir+"_{0}".format(str(num1)) ):
           num1+=1
         options.outputDir=options.outputDir+"_{0}".format(str(num1))
         print "directory exist. will save at "+options.outputDir
         


    #create tmp folder inside the user one - needed for job partitioning - will be erased at the end
    num=0
    # make sure that it does not exist
    while os.path.exists(options.outputDir+"/temp_{0}".format(str(num)) ):
        num+=1

    workdir =  options.outputDir+"/temp_{0}".format(str(num))
    os.makedirs(workdir)

    
    nlines=0
    with open(options.inputData,"r") as inf:
      lines=inf.readlines()
      nlines=len(lines)


    ncores=mp.cpu_count()
    if nlines<mp.cpu_count(): ncores=nlines
    if options.ncore!=-1: ncores=options.ncore
    files = [open(workdir+'/mca_%d.txt' % i, 'w') for i in range(ncores)]

    print "job distributed in",ncores,"cores"

    for i,line in enumerate(lines):
      if line.startswith("#"): continue;
      if not line.strip(): continue;
      if line=="\n": continue;
      itxt = i % ncores 
      files[itxt].write(line) 

      
    for fi in files:
      fi.close() 

    rootname="hadd -f "+workdir+"/hsum.root "
    jobs=[]
    for i in range(0,ncores):
       temp=workdir+";"+str('histo_%d' % i)+";"+str('mca_%d.txt' % i)+";"+options.plotfile+";"+options.tree
       rootname+=workdir+str('/histo_%d.root  ' % i)
       jobs.append(temp)


    p = mp.Pool(ncores)
    p.map(f,jobs)

   
    print "merging... "
    os.system(rootname)


    print "applying cosmetics... "
    #gInterpreter.ProcessLine(cppcode)
    gROOT.SetBatch(True)
    froot = TFile(workdir+'/hsum.root')
    with open(workdir+"/_histo_0.txt","r") as res:
      lines=[]
      lines=res.readlines()
      plotted_alrd=[]
      for iline,line in enumerate(lines):
        if line=="\n": continue
        if iline in plotted_alrd:
           continue
        wline=(line.rstrip()).split(":")
        histName=wline[0]
        canvasName=wline[1]
        plot_options=(wline[2]).split(";")
        h1= froot.Get(histName)
        h1.SetLineWidth(3)
        c1 = TCanvas( canvasName,canvasName, 700,700);
        hstack= THStack("hs","histos")
        heff=transform(h1,plot_options)
        if "LogX" in plot_options: c1.SetLogx()
        if "LogY" in plot_options: c1.SetLogy()
        if "Norm" in plot_options and h1.Integral()>0:
           h1.Scale(1.0/h1.Integral())
        hstack.Add(h1)
        x1,y1,x2,y2= legPos(plot_options)
        leg = TLegend(x1,y1,x2,y2)
        leg.AddEntry(h1,legName(plot_options,histName))
        multhisto=False
        for jline in range(iline+1,len(lines)-1):
          line2=lines[jline]
          if line2=="\n": continue;
          wline2=(line2.rstrip()).split(":")
          canvasName2=wline2[1]
          if canvasName != canvasName2:
             break;
          multhisto=True
          plotted_alrd.append(jline);
          histName2=wline2[0]
          plot_options2=wline2[2].split(";")
          h2=froot.Get(histName2)
          
          h2.SetLineWidth(3)
          h2.SetLineColor(jline-iline)
          hstack.Add(h2)
          if "Norm" in plot_options2 and h2.Integral()>0: 
             h2.Scale(1.0/h2.Integral())
          h2=transform(h2,plot_options2)
          leg.AddEntry(h2,legName(plot_options2,histName2))
        if "PlotLine" in plot_options:
            hstack.Draw("nostack,hist")
        else:
            hstack.Draw("nostack,e1p")
        hstack.GetXaxis().SetTitle(h1.GetXaxis().GetTitle())
        hstack.GetYaxis().SetTitle(h1.GetYaxis().GetTitle())
        if multhisto: leg.Draw("sames")
        cms().Draw("sames")
        head().Draw("sames");
        c1.SaveAs(options.outputDir+"/"+canvasName+".png");
        c1.SaveAs(options.outputDir+"/"+canvasName+".pdf");
    os.system( "mv "+workdir+"/hsum.root   "+options.outputDir+"/histos.root" )
    os.system( "rm -r "+workdir )
    print "finished !"
  
