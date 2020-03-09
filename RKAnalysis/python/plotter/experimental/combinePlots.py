import os, subprocess 
from argparse import ArgumentParser
import multiprocessing as mp
from ROOT import *
import time;



def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(kBlack)
    h3.SetMarkerStyle(21)
    h3.SetTitle("")
    h3.SetMinimum(0)
    h3.SetMaximum(4)
    # Set up plot for markers and errors
    h3.Divide(h2)
 
    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("ratio")
    y.SetNdivisions(505)
    y.SetTitleSize(30)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.0)
    y.SetLabelFont(43)
    y.SetLabelSize(20)
 
    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitleSize(30)
    x.SetTitleFont(43)
    x.SetTitleOffset(3.0)
    x.SetLabelFont(43)
    x.SetLabelSize(25)
    return h3
 
 
def createCanvasPads():
    c = TCanvas("c", "canvas", 800, 800)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetGridx()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.3)
    pad2.SetRightMargin(0.03)
    pad1.SetRightMargin(0.03)   
    pad2.SetLeftMargin(0.08)
    pad1.SetLeftMargin(0.08)   
    pad2.SetGridx()
    pad2.Draw()
    return c, pad1, pad2
  
 

def transform( heff, kwds):
      
   for kwd in kwds:          
     value = kwd.split("=")
     if len(value)==1: 
        if value[0]=="Norm":
          heff.Scale(1.0/heff.Integral())
        continue
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
     if value[0]=="XTitle":
        heff.GetXaxis().SetTitle(value[1]);
     if value[0]=="YSetMin":
        heff.GetXaxis().SetTitle(value[1]);
     
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




if __name__ == "__main__":

    # availiable plotting options
    parser = ArgumentParser()

    parser.add_argument("-i","--inputPaths",dest="inputPaths", nargs='+',type=str,   default=["plots.root"], help="input directories to find histos.root")

    parser.add_argument("-p","--plots", nargs='+', dest="plotNames", default=["SimplePlots"],type=str, help="plot names to be superimposed. same order as dir. If only ONE name is provided it will search for that in all files ")
    parser.add_argument("-c","--cfgPlots" ,dest="cfg",nargs='+',default=["None"],type=str, help="")
    parser.add_argument("--colors" ,dest="colors",nargs="+",  default=None,type=int, help="")
    parser.add_argument("-l","--legends" ,nargs='+',dest="legends",  default=["None"],type=str, help="legend per plot")
    parser.add_argument("--two-plot-ratio",dest="ratio",  default=False, action="store_true", help="")
    parser.add_argument("-o","--output",dest="outputName",  default="PlotsComp", type=str, help="folder name to save plots. Default=Plots_Date")
    
   
    args = parser.parse_args()
    
     #  create output folder to save plots
    num=0
    while ( os.path.exists(args.outputName+".png") and num==0) or os.path.exists(args.outputName+"_%d.png" % num ):
      num+=1
      
    args.outputName+="_"+str(num)
    #os.system(  "mkdir -p "+args.outputDir )
    #print "plots will be saved at "+args.outputDir
    
    if len(args.plotNames)==0 :
       print " histo name is not provided"
       exit()

    if len(args.legends) != len(args.inputPaths):
       print "legends for all plots not defined"
       exit()    

    if len(args.plotNames) == 1 and len(args.inputPaths)>1:
       while len(args.plotNames)<len(args.inputPaths):
         args.plotNames.append(args.plotNames[0])          
    
    gROOT.SetBatch(True)
    
    leg = TLegend(0.7,0.7,0.9,0.9)
    #gROOT.Macro(".rootlogon.C")
    c2 = TCanvas( "cnv2","cnv2", 700,700);
    hstack= THStack("hs","histos")
#    options = (args.cfg).split(";")
    options = args.cfg
        
    files = { "file_"+str(i) : TFile(path+"/histos.root") for i,path in enumerate(args.inputPaths)}

    plots = { 'plot_'+str(i)  : files['file_'+str(i)].Get(plot) for i,plot in enumerate(args.plotNames)}
   

    for i,plot in enumerate(plots.keys()):             
       if args.colors != None and len(args.colors) == len(args.inputPaths):
          plots[plot].SetLineColor(args.colors[num])
          plots[plot].SetMarkerColor(args.colors[num])
       else:
          plots[plot].SetLineColor(i+1)
          plots[plot].SetMarkerColor(i+1)
       plots[plot].SetLineWidth(3)
       plots[plot]=transform(plots[plot], options)
       leg.AddEntry(plots[plot],args.legends[i])
       hstack.Add(plots[plot])    
    
    if "marker" in options:   
      hstack.Draw("nostack,e1p")
    else:
      hstack.Draw("nostack,hist")
    leg.Draw("sames")

    cms().Draw("sames")
    head().Draw("sames")
   
    if args.ratio and len(plots)==2:
       c, pad1, pad2 = createCanvasPads()
       hstack= THStack("hs","histos")
       hstack.Add(plots['plot_0'])
       hstack.Add(plots['plot_1'])
       # draw everything
       pad1.cd()
       if "LogY" in options:
        pad1.SetLogy()  
       if "marker" in options:
         hstack.Draw("nostack,e1p")
       else:
         hstack.Draw("nostack,hist")         
           
       leg.Draw("sames")
       hratio = createRatio( plots['plot_0'], plots['plot_1'])
       # to avoid clipping the bottom zero, redraw a small axis
       cms().Draw("sames")
       head().Draw("sames")
       pad2.cd()
       hratio.Draw("p")
       c2=c

    elif args.ratio and len(plots)!=2:
       print "ratio possible only for two histos"
     
      
    c2.SaveAs(args.outputName+".png");
    c2.SaveAs(args.outputName+".pdf"); 
     
           
         
        
        
    
        
    print "finished !"
  
