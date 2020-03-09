#include "TH1.h"


int GetPtThr(){
  float thr=0.95;
  TFile * fin= new TFile("experimental/Bpt_0/histos.root");
  TH1F * hin = (TH1F*) fin->Get("Bpt_7");
  float total= static_cast<float> (hin->GetEntries());
  float calcValue=0;
  float pt=0;
  for (int ibin=0; ibin<hin->GetNbinsX(); ibin++){
    calcValue+=(hin->GetBinContent(ibin))/total;
    if (calcValue<1.0-thr) continue;
    pt=ibin;
    break;
  }
  cout<<"pt threshold for "<<thr<<" is "<<pt*(-hin->GetBinCenter(1)+hin->GetBinCenter(hin->GetNbinsX()))/hin->GetNbinsX()<<endl;
cout<<hin->GetBinCenter(1)<<"  "<<hin->GetBinCenter(hin->GetNbinsX())<<endl;

return 0;
}
