#include "TH1.h"
#include "TMath.h"
#include "TF1.h"
#include "TLegend.h"
#include "TCanvas.h"


TLatex cms(){
  TLatex cms_label = TLatex();
  cms_label.SetTextSize(0.04);
  cms_label.DrawLatexNDC(0.16, 0.92, "#bf{ #font[22]{CMS} #font[72]{Preliminary}}");
  return cms_label;
}

TLatex head(){
  TLatex header = TLatex();
  header.SetTextSize(0.03);
  header.DrawLatexNDC(0.63, 0.92, "#sqrt{s} = 13 TeV, 2018 p-p ");
  return header;
    }



 Double_t kTH = -0.5;

Double_t Background(Double_t *x, Double_t *par)
// The background function
{
  

   //   Double_t val = par[0]*TMath::Exp(kTH*arg*arg)*x[0]*x[0];
  Double_t val=TMath::Exp(par[0]+par[1]*x[0]);
   return val;
}

Double_t Signal(Double_t *x, Double_t *par)
// The signal function: a gaussian
{
  // Double_t arg = 0;
   //  if (par[2]) arg = (x[0] - par[1])/par[2];

  Double_t sig = par[0]*TMath::Exp(-0.5*(x[0]-par[1]/par[2])*(x[0]-par[1]/par[2]));
   return sig;
}

Bool_t reject;
Double_t fline(Double_t *x, Double_t *par)
{
  if (reject && x[0] > 5.1 && x[0] < 5.3) {
      TF1::RejectPoint();
      return 0;
   }

    return exp(par[0]+par[1]*x[0]);
       
}

Double_t Total(Double_t *x, Double_t *par)
// Combined background + signal
{
   Double_t tot = Background(x,par) + Signal(x,&par[2]);
   return tot;
}

int backSgnfit7_only_gauss_expo() {
   // the control function
   //fit function
   
  TFile * fmm=new TFile("../25_11/plotsKMuMu2B_2/histos.root","READ");
 

  TString title="M(#mu#muK)";
 
  TH1F * hjp=(TH1F*) fmm->Get("MB");
 
  TH1F * hjp2=(TH1F *) hjp->Clone();
  gStyle->SetOptFit(0);

  TF1 * gfit=new TF1("gfit","gaus",5.18,5.38);
  ROOT::Math::MinimizerOptions::SetDefaultStrategy(1); 

  hjp->Fit("gfit","LR+");
  
  cout<<"gfit "<<gfit->GetChisquare()<<" "<<gfit->GetNDF()<<endl;

  reject=true;
  TF1 * efit=new TF1("efit",fline,4.5,6,2);
  efit->SetParameter(0,20);
  efit->SetParameter(1,-0.2);
  efit->SetLineColor(3);
  hjp->Fit("efit","LR+");
  cout<<"efit "<<efit->GetChisquare()<<" "<<efit->GetNDF()<<endl;

  ROOT::Math::MinimizerOptions::SetDefaultMaxFunctionCalls(100000000);
  TF1 *totfit = new TF1("totfit","gaus(0)+expo(3)",4.7,5.7);
  double par[5]={0};
  gfit->GetParameters(&par[0]);
  efit->GetParameters(&par[3]);
  totfit->SetParameters(par);
  //  totfit->SetParLimits(2,0.03,0.1);
  totfit->FixParameter(1,5.27534);
  totfit->FixParameter(2,0.0399498);
  
  TFitResultPtr r_tot = hjp->Fit("totfit","RLS");
  hjp->Fit("totfit","RL");

  TF1 *bkgfit = new TF1("bkgfit","expo(0)",4.7,5.7);
  double par2[8]={0};
  totfit->GetParameters(&par2[0]);
  bkgfit->FixParameter(0,par2[3]);
  bkgfit->FixParameter(1,par2[4]);


//TFitResultPtr r_tot = hjp->Fit("totfit","SLR");
  TF1 * sfit=new TF1("sfit","gaus",5.0,5.5);
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
  //sd=0.0578105;
  cout<<mean-2*sd<<"  "<<mean+2*sd<<" "<<2*sd<<endl;
  cout<<totfit->GetChisquare()<<" "<<totfit->GetNDF()<<endl;
  cout<<"S= "<<totfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)-bkgfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<" B= "<<bkgfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<endl;

  cout<<"S= "<<sfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<" error Sig "<<sfit->IntegralError(mean-2*sd,mean+2*sd, &parSig[0],subcor.GetMatrixArray())/hjp->GetBinWidth(1)<<endl;
//cout<<"S= "<<totfit->Integral(5.19274,5.35227)/hjp->GetBinWidth(1)- bkgfit->Integral(5.19274,5.35227)/hjp->GetBinWidth(1)<<" B= "<<bkgfit->Integral(5.19274,5.35227)/hjp->GetBinWidth(1)<<endl;
 gStyle->SetOptStat(0);
TCanvas * c1=new TCanvas("c1","c1",700,700);
 hjp->Draw("P E");
 hjp->SetMinimum(0);
   hjp->SetMarkerStyle(kFullDotLarge);
  hjp->SetMarkerColor(kBlack);
 hjp->SetLineColor(1);
 cms().Draw("sames");
 head().Draw("sames");
hjp->SetTitle(" ");
c1->SetGridx(); c1->SetGridy();
 hjp->GetXaxis()->SetTitle(title);
 bkgfit->SetLineStyle(2);
 bkgfit->Draw("sames");
 
  return 0;
}
