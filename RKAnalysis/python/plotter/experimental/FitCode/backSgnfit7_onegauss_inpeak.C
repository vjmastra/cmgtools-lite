#include "TH1.h"
#include "TMath.h"
#include "TF1.h"
#include "TLegend.h"
#include "TCanvas.h"





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
  if (reject && x[0] > 4.9 && x[0] < 5.4) {
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

int backSgnfit7_onegauss_inpeak() {
   // the control function
   //fit function
   TFile *fmm;
    // fmm=new TFile("histo_470m_fixedtag.root","READ");
   // fmm=new TFile("histo_270m_fixedxsec_Bptetares.root","READ");
   fmm=new TFile("/afs/cern.ch/work/g/gkaratha/private/SUSYCMG/HLT/efficiency/Analizer/uboost/CMSSW_10_1_4/src/hep_ml/AnalyzeBDTresults/histoFit_xgb_step2opt.root","READ");
     
TH1F *hjp;
    hjp=(TH1F*) fmm->Get("bmll_xgb");
    TH1F * hjp2=(TH1F *) hjp->Clone();
    gStyle->SetOptFit(0);

 TF1 * gfit=new TF1("gfit","gaus",5.18,5.38);
 ROOT::Math::MinimizerOptions::SetDefaultStrategy(1); 
 hjp->Fit("gfit","LR+");


 reject=true;
 TF1 * efit=new TF1("efit",fline,4.8,5.7,2);
 efit->SetParameter(0,20);
 efit->SetParameter(1,-0.2);
 efit->SetLineColor(3);
 hjp->Fit("efit","LR+");
 cout<<efit->GetChisquare()<<" "<<efit->GetNDF()<<endl;

 ROOT::Math::MinimizerOptions::SetDefaultMaxFunctionCalls(1000000000);


 TF1 *pfit = new TF1("pfit","gaus",5.0,5.16);
 hjp->Fit("pfit","LR+");
 cout<<pfit->GetChisquare()<<" "<<pfit->GetNDF()<<endl;
 TF1 *totfit = new TF1("totfit","gaus(0)+expo(3)+gaus(5)",4.8,5.7);
 double par[8]={0};
 gfit->GetParameters(&par[0]);
 efit->GetParameters(&par[3]);
 pfit->GetParameters(&par[5]);
 totfit->SetParLimits(2,0,0.1);
 totfit->SetParLimits(8,10,10000);
 totfit->SetParLimits(10,0,10);
 totfit->FixParameter(2,5.279);

 totfit->SetParameters(par);

 hjp->Fit("totfit","RL");

 TF1 *bkgfit = new TF1("bkgfit","expo(0)+gaus(2)",4.8,5.7);
 double par2[11]={0};
totfit->GetParameters(&par2[0]);
bkgfit->SetParameter(0,par2[3]);
bkgfit->SetParameter(1,par2[4]);
bkgfit->SetParameter(2,par2[5]);
bkgfit->SetParameter(3,par2[6]);
bkgfit->SetParameter(4,par2[7]);

TFitResultPtr r_tot = hjp2->Fit("totfit","SLR+");
 TF1 * sfit=new TF1("sfit","gaus",4.8,5.7);
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

//bkgfit->SetParameter(0, 5.31206e+05);
//bkgfit->SetParameter(1,-1.87847e+05);
//bkgfit->SetParameter(2,1.66102e+04);
//bkgfit->SetParameter(5,par2[11]);

for (int i=0; i<11; i++){
 cout<<" par "<<i<<" v "<<par2[i]<<endl;
}

double mean=par2[1],sd=par2[2]; 



 cout<<"start "<<mean-2*sd<<" end "<<mean+2*sd<<endl;
cout<<totfit->GetChisquare()<<" "<<totfit->GetNDF()<<endl;
 cout<<"S= "<<totfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)-bkgfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<" B= "<<bkgfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<endl;
cout<<"S= "<<sfit->Integral(mean-2*sd,mean+2*sd)/hjp->GetBinWidth(1)<<" error Sig "<<sfit->IntegralError(mean-2*sd,mean+2*sd, &parSig[0],subcor.GetMatrixArray())/hjp->GetBinWidth(1)<<endl;
/*TF1 *bfit = new TF1("bfit","expo(0)+gaus(2)",4.7,5.7);
double fpar[11]={0};
totfit->GetParameters(&fpar[0]);
bfit->SetParameter(0,fpar[6]);
bfit->SetParameter(1,fpar[7]);
bfit->SetParameter(2,fpar[8]);
bfit->SetParameter(3,fpar[9]);
bfit->SetParameter(4,fpar[10]);
bfit->SetLineStyle(2);*/


 gStyle->SetOptStat(0);
TCanvas * c1=new TCanvas("c1","c1",700,700);
 hjp->Draw("P E");
 hjp->SetMinimum(0);
   hjp->SetMarkerStyle(kFullDotLarge);
  hjp->SetMarkerColor(kBlack);
 hjp->SetLineColor(1);
TPaveText *t = new TPaveText(0.07, 0.9, 0.7, 0.98, "NDC"); // left-up brNDC
t->AddText("#font[22]{CMS} #font[72]{Preliminary}, 2018 p-p (13TeV)");
t->SetBorderSize(0);
t->SetFillColor(0);
t->Draw("sames");
hjp->SetTitle(" ");
c1->SetGridx(); c1->SetGridy();
 hjp->GetXaxis()->SetTitle("M(#mu#muK)");
 bkgfit->SetLineStyle(2);
 bkgfit->Draw("sames");

  return 0;
}
