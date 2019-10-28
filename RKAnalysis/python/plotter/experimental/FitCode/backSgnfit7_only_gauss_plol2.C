#include "TH1.h"
#include "TMath.h"
#include "TF1.h"
#include "TLegend.h"
#include "TCanvas.h"

float minW=2.9,maxW=3.2;
TString PolN="pol2";

Bool_t reject;
Double_t fline(Double_t *x, Double_t *par)
{
  if (reject && x[0]>minW && x[0]<maxW) {
      TF1::RejectPoint();
      return 0;
   }
  if(PolN=="pol2")
    return par[0]+par[1]*x[0]+par[2]*x[0]*x[0];
  else 
    return par[0]+par[1]*x[0];
}  


int backSgnfit7_only_gauss_plol2() {
  // the control function
  //fit function
  TFile * fmm=new TFile("../Validations/histo_valmassee.root","READ");
  TString title="M(e,e)";
  TH1F * hjp=(TH1F*) fmm->Get("hbmall_old");
  hjp->Rebin(2);
  PolN="pol1";
  float minX=2.6,maxX=3.4,minG=2.95,maxG=3.15; //e 3.62 3.8
   minW=3.6; maxW=3.8;
  //float minX=2.6,maxX=3.5,minG=3.01,maxG=3.18;
  //minW=3.01; maxW=3.18;
  TH1F * hjp2=(TH1F *) hjp->Clone();
  gStyle->SetOptFit(0);
    
// TF1 * gfit=new TF1("gfit","gaus",2.9,3.2);
  TF1 * gfit=new TF1("gfit","gaus",minG,maxG);
  ROOT::Math::MinimizerOptions::SetDefaultStrategy(1); 
  //ROOT::Math::MinimizerOptions::SetDefaultPrintLevel(0);
  hjp->Fit("gfit","LR+");
  cout<<"gfit "<<gfit->GetChisquare()<<" "<<gfit->GetNDF()<<endl;

  reject=true;
  //TF1 * efit=new TF1("efit",fline,2.6,3.5,2);
  TF1 * efit=new TF1("efit",fline,minX,maxX,2);
  efit->SetParameter(0,5);
  efit->SetParameter(1,0.2);
  efit->SetLineColor(3);
  hjp->Fit("efit","LR+");
  cout<<"efit "<<efit->GetChisquare()<<" "<<efit->GetNDF()<<endl;
  //ROOT::Math::MinimizerOptions::SetDefaultMaxFunctionCalls(100000);
  ROOT::Math::MinimizerOptions::SetDefaultMaxFunctionCalls(100000000);


  //TF1 *totfit = new TF1("totfit","gaus(0)+pol2(3)",2.6,3.5);
  TF1 *totfit;
  //  if (PolN=="Pol2")
    totfit= new TF1("totfit","gaus(0)+"+PolN+"(3)",minX,maxX);
  double par[6]={0};
  gfit->GetParameters(&par[0]);
  efit->GetParameters(&par[3]);
  totfit->SetParameters(par);
  totfit->SetParLimits(2,0,1);

  TFitResultPtr r_tot = hjp->Fit("totfit","RLS");
  //hjp->Fit("totfit","RL");
  //TF1 *bkgfit = new TF1("bkgfit","pol2(0)",2.6,3.5);
  TF1 *bkgfit = new TF1("bkgfit",PolN+"(0)",minX,maxX);
  double par2[8]={0};
  totfit->GetParameters(&par2[0]);
  bkgfit->FixParameter(0,par2[3]);
  bkgfit->FixParameter(1,par2[4]);
  if (PolN=="pol2")
    bkgfit->FixParameter(2,par2[5]);


//TFitResultPtr r_tot = hjp->Fit("totfit","SLR");
 //TF1 * sfit=new TF1("sfit","gaus",2.6,3.5);
  TF1 * sfit=new TF1("sfit","gaus",minX,maxX);
  sfit->SetParameter(0,totfit->GetParameter(0));
  sfit->SetParameter(1,totfit->GetParameter(1));
  sfit->SetParameter(2,totfit->GetParameter(2));
  sfit->SetParError(0,totfit->GetParError(0));
  sfit->SetParError(1,totfit->GetParError(1));
  sfit->SetParError(2,totfit->GetParError(2));
  double parSig[3]={0};
  sfit->GetParameters(&parSig[0]);
  TMatrixD cor = r_tot->GetCovarianceMatrix();
  TMatrixD subcor; cor.GetSub(0,2,0,2,subcor);

  double mean=par2[1],sd=par2[2];  
  cout<<mean-2*sd<<"  "<<mean+2*sd<<" "<<2*sd<<endl;
  cout<<totfit->GetChisquare()<<" "<<totfit->GetNDF()<<endl;
  cout<<"S= "<<totfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)-bkgfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<" B= "<<bkgfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<endl;
  cout<<"S= "<<sfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<" error Sig "<<sfit->IntegralError(mean-2*sd,mean+2*sd, &parSig[0],subcor.GetMatrixArray())/hjp->GetBinWidth(1)<<endl;
//cout<<"S= "<<totfit->Integral(5.19274,5.35227)/hjp->GetBinWidth(1)- bkgfit->Integral(5.19274,5.35227)/hjp->GetBinWidth(1)<<" B= "<<bkgfit->Integral(5.19274,5.35227)/hjp->GetBinWidth(1)<<endl;
  gStyle->SetOptStat(0);
  TCanvas * c1=new TCanvas("c1","c1",700,700);
  hjp->Draw("P E"); hjp->SetMinimum(0);
  hjp->SetMarkerStyle(kFullDotLarge); hjp->SetMarkerColor(kBlack);
  hjp->SetLineColor(1);
  TPaveText *t = new TPaveText(0.07, 0.9, 0.7, 0.98, "NDC"); // left-up brNDC
  t->AddText("#font[22]{CMS} #font[72]{Preliminary}, 2018 p-p (13TeV)");
  t->SetBorderSize(0); t->SetFillColor(0);
  t->Draw("sames"); hjp->SetTitle(" ");
  c1->SetGridx(); c1->SetGridy();
  hjp->GetXaxis()->SetTitle(title);
  bkgfit->SetLineStyle(2);
  bkgfit->Draw("sames");
  //bfit->Draw("sames");
  return 0;
}
