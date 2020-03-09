#include "TH1.h"
#include "TMath.h"
#include "TF1.h"
#include "TLegend.h"
#include "TCanvas.h"
#include "TLatex.h"
   
    
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
  if (reject && x[0] > 4.8 && x[0] < 5.4) {
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

int backSgnfit7() {
  // the control function
  //fit function
  TFile * fmm=new TFile("../25_11/plotsKMuMu2B_2/histos.root","READ");
     
  TH1F * hjp=(TH1F*) fmm->Get("MllB");
  TH1F * hjp2=(TH1F *) hjp->Clone();
  gStyle->SetOptFit(0);

  TF1 * gfit=new TF1("gfit","gaus",5.25,5.32);
  ROOT::Math::MinimizerOptions::SetDefaultStrategy(1); 

  hjp->Fit("gfit","LR+");
  cout<<gfit->GetChisquare()<<" "<<gfit->GetNDF()<<endl;
  TF1 * gfit2=new TF1("gfit2","gaus",5.2,5.35);

  hjp->Fit("gfit2","LR+");
  double gpar[6]={0};
  gfit->GetParameters(&gpar[0]);
  gfit2->GetParameters(&gpar[3]);

  TF1 * gfitT=new TF1("gfitT","gaus(0)+gaus(3)",5.2,5.35);
  gfitT->SetParameters(gpar);
  gfitT->SetParLimits(2,0,0.1);
  gfitT->FixParameter(1,gpar[1]);
  gfitT->FixParameter(4,gpar[4]);
  

  hjp->Fit("gfitT","LR+");

  reject=true;
  TF1 * efit=new TF1("efit",fline,4.73,5.7,2);
  efit->SetParameter(0,20);
  efit->SetParameter(1,-0.2);
  efit->SetLineColor(3);
  hjp->Fit("efit","LR+");
  cout<<efit->GetChisquare()<<" "<<efit->GetNDF()<<endl;

  ROOT::Math::MinimizerOptions::SetDefaultMaxFunctionCalls(1000000000);


  TF1 *pfit = new TF1("pfit","gaus",4.85,5.16);
  hjp->Fit("pfit","LR+");

  cout<<pfit->GetChisquare()<<" "<<pfit->GetNDF()<<endl;
  TF1 *totfit = new TF1("totfit","gaus(0)+gaus(3)+expo(6)+gaus(8)",4.73,5.7);
  double par[11]={0};
  gfitT->GetParameters(&par[0]);
  efit->GetParameters(&par[6]);
  pfit->GetParameters(&par[8]);
  //totfit->SetParLimits(2,0,0.1);
  //totfit->SetParLimits(8,10,10000);
  //totfit->SetParLimits(10,0,10);
  //  totfit->FixParameter(9,par[9]);
  //totfit->FixParameter(1,5.279);
  // totfit->FixParameter(4,5.279);

  totfit->SetParameters(par);
  hjp->Fit("totfit","RL");

  TF1 *bkgfit = new TF1("bkgfit","expo(0)+gaus(2)",4.8,5.7);
  double par2[11]={0};
  totfit->GetParameters(&par2[0]);
  bkgfit->SetParameter(0,par2[6]);
  bkgfit->SetParameter(1,par2[7]);
  bkgfit->SetParameter(2,par2[8]);
  bkgfit->SetParameter(3,par2[9]);
  bkgfit->SetParameter(4,par2[10]);

  TFitResultPtr r_tot = hjp2->Fit("totfit","SLR+");
  TF1 * sfit=new TF1("sfit","gaus(0)+gaus(3)",4.8,5.7);
  sfit->SetParameter(0,totfit->GetParameter(0));
  sfit->SetParameter(1,totfit->GetParameter(1));
  sfit->SetParameter(2,totfit->GetParameter(2));
  sfit->SetParameter(3,totfit->GetParameter(3));
  sfit->SetParameter(4,totfit->GetParameter(4));
  sfit->SetParameter(5,totfit->GetParameter(5));
  sfit->SetParError(0,totfit->GetParError(0));
  sfit->SetParError(1,totfit->GetParError(1));
  sfit->SetParError(2,totfit->GetParError(2));
  sfit->SetParError(3,totfit->GetParError(3));
  sfit->SetParError(4,totfit->GetParError(4));
  sfit->SetParError(5,totfit->GetParError(5));


  double parSig[3]={0};
  sfit->GetParameters(&parSig[0]);

  TMatrixD cor = r_tot->GetCovarianceMatrix();
  TMatrixD subcor; 
  cor.GetSub(0,2,0,2,subcor);

  double mean=par2[1],sd=par2[5]; 

  cout<<"start "<<mean-2*sd<<" end "<<mean+2*sd<<endl;

  cout<<totfit->GetChisquare()<<" "<<totfit->GetNDF()<<endl;

  cout<<"S= "<<totfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)-bkgfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<" B= "<<bkgfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<endl;
 
  //  cout<<"S= "<<sfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<endl;//<<" error Sig "<<sfit->IntegralError(mean-2*sd,mean+2*sd, &parSig[0],subcor.GetMatrixArray())/hjp->GetBinWidth(1)<<endl;


  TCanvas * c1=new TCanvas("c1","c1",700,700);
  hjp->SetMarkerStyle(kFullDotLarge);
  hjp->Draw("P E");
  hjp->SetLineColor(1);

  gStyle->SetOptStat(0);
  
  hjp->SetTitle(" ");
  c1->SetGridx(); c1->SetGridy();
  hjp->GetXaxis()->SetTitle("M(#mu#muK)");
  hjp->SetMinimum(0);
  bkgfit->SetLineStyle(2);
  bkgfit->Draw("sames");
  head().Draw("sames");
  cms().Draw("sames");
  return 0;
}
