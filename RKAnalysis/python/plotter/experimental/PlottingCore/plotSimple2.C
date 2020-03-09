#include <sstream>
#include <string>
#include <algorithm>
#include <iterator>
#include <boost/algorithm/string.hpp>
#include <fstream>
#include "plot_tool.h"
#include "TLatex.h"
#include <TMacro.h>




int plotSimple2( TString path, TString name, std::string mca, std::string plots, TString tree){
  

  TChain * ccdata=new TChain(tree);
  std::ifstream inmca(path+"/"+mca);
    
  std::string ntuple;
  if (inmca.is_open()){
    while (std::getline(inmca, ntuple)){  
      if (ntuple=="") continue;
      ccdata->Add(TString(ntuple));  
    }
   }
   cout<<"Running on "<<ccdata->GetEntries()<<" evts "<<endl;  
  

  gStyle->SetOptStat(0); 
  std::string line;

  TFile * fout=new TFile(path+"/"+name+".root","RECREATE");
  ofstream tout;
  tout.open(path+"/_"+name+".txt");
  

  std::ifstream infile(plots);
 
  //create histo
  while (std::getline(infile, line)){

    vector<string> tokens;   
    boost::split(tokens,line,boost::is_any_of(":"));

    //pass plots commented
    if (tokens.size()==1) continue;
    if (tokens[0]=="#") continue;

    // protection
    if (tokens.size()<8) {
       cout<<"ERROR requested plot: "<<tokens[0]<<" less options that mandatory- SKIPPING "<<endl;
       continue;  
    }

    //initialize
    if (tokens[2]=="None") tokens[2]="1>0";
    cout<<"plotting... "<<tokens[0]<<" histo "<<endl;
   
    // create plots
    TH1F * temp_data = gethisto(ccdata,tokens[1],tokens[2],tokens[0],std::stoi(tokens[4]),std::stof(tokens[5]),std::stof(tokens[6]));

    TString titleX(tokens[3]); 
    temp_data->GetXaxis()->SetTitle(titleX);

    std::string options=tokens[0]+":"+tokens[7]+":"; 
    // save optional arguments
    for(unsigned int itoken=8; itoken<tokens.size(); ++itoken){
      if (options=="")
        options=tokens[itoken];
      else 
        options+=";"+tokens[itoken];
     }
    options+="\n";
    temp_data->Write();
    tout<<options<<"\n";  
          
  }
 
  fout->Close();
  tout.close();
 
 
 return 0;

}
