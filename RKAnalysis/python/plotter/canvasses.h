#include "TCanvas.h"
#include "TLegend.h"
#include "TH1.h"
#include "TString.h"


TLatex cms(){

  TLatex cms_label = TLatex();
  cms_label.SetTextSize(0.04);
  cms_label.DrawLatexNDC(0.1, 0.957, "#font[61]{CMS} ");
  return cms_label;
}

TLatex extra(){

  TLatex cms_label = TLatex();
  cms_label.SetTextSize(0.03);
  cms_label.DrawLatexNDC(0.19, 0.957, "#font[52]{Preliminary}");
  return cms_label;
}

TLatex head(){
    TLatex header = TLatex();
    header.SetTextSize(0.03);
    header.DrawLatexNDC(0.6, 0.957, "2018 (p-p 13 TeV) ");
    return header;
 }


TH1F * gethisto(TChain * cc,TString var,TString cuts, TString name, int bins, float start, float end){
 TH1F * htemp=new TH1F(name," ",bins,start,end);
 cc->Draw(var+">>"+name,cuts);
 return htemp;
}

void addregion(TChain * cc,TString var,TString cuts, TString name){
 cc->Draw(var+">>+"+name,cuts);
}

TH2F * get2Dhisto(TChain * cc,TString varX,TString varY ,TString cuts, TString name, int binsX, float startX, float endX,int binsY, float startY, float endY ){
  TH2F * htemp=new TH2F(name," ",binsX,startX,endX,binsY,startY,endY);
 cc->Draw(varY+" : "+varX+">>"+name,cuts);
 return htemp;
}

TCanvas *canvas_5plot(TH1F * h1, TH1F * h2, TH1F * h3, TH1F * h4, TH1F * h5,TString canvas, bool Logy, bool norm,double miny, double maxy, TString Labelx,TString Labely, TString leg1,TString leg2,TString leg3, TString leg4,TString leg5){

  TCanvas *data_mc_canvas = new TCanvas(canvas,canvas,700,700);
  gStyle->SetPadBorderMode(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(1);

  h1->SetLineColor(kRed);
  h2->SetLineColor(kBlue);
  h3->SetLineColor(kBlack);
  h4->SetLineColor(kMagenta);
  h5->SetLineColor(kGreen);
 
  h1->GetYaxis()->SetTitle(Labely);
  h1->GetXaxis()->SetTitle(Labelx);

  if (norm) {
      h1->Scale(1/h1->Integral());
      h2->Scale(1/h2->Integral());
      h3->Scale(1/h3->Integral());
      h4->Scale(1/h4->Integral());
      h5->Scale(1/h5->Integral());
   }

  h1->Draw("HIST ");
  h2->Draw("HIST sames");
  h3->Draw("HIST sames");
  h4->Draw("HIST sames");
  h5->Draw("HIST sames");

  
  h1->GetYaxis()->SetRangeUser(miny,maxy);
  
   TLegend * leg = new TLegend(0.70,0.70,1,1);
   leg->AddEntry(h1,leg1);
   leg->AddEntry(h2,leg2);
   leg->AddEntry(h3,leg3);
   leg->AddEntry(h4,leg4);
   leg->AddEntry(h5,leg5);
   leg->SetTextFont(42);
   leg->SetFillColor(kWhite);
   leg->SetLineColor(kWhite);
   leg->SetBorderSize(0);
   leg->Draw();
   if (Logy) data_mc_canvas->SetLogy();
   cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
   return data_mc_canvas;
   
   }



TCanvas *canvas_4plot(TH1F * h1, TH1F * h2, TH1F * h3, TH1F * h4, TString canvas, bool Logy, bool norm,double miny, double maxy, TString Labelx,TString Labely, TString leg1,TString leg2,TString leg3, TString leg4, bool dashed=false){

  TCanvas *data_mc_canvas = new TCanvas(canvas,canvas,700,700);
    gStyle->SetPadBorderMode(0);
  gStyle->SetOptStat(0);
    gStyle->SetOptTitle(1);

  h1->SetLineColor(kRed);
  h2->SetLineColor(kBlue);
  h3->SetLineColor(kBlack);
  h4->SetLineColor(kMagenta);
if(dashed){
  h1->SetLineColor(kRed);
  h2->SetLineColor(kBlue);
  h3->SetLineColor(kRed);
  h4->SetLineColor(kBlue);
}
 
  h1->GetYaxis()->SetTitle(Labely);
  h1->GetXaxis()->SetTitle(Labelx);

  if (norm) {
      h1->Scale(1/h1->Integral());
      h2->Scale(1/h2->Integral());
      h3->Scale(1/h3->Integral());
      h4->Scale(1/h4->Integral());
   }

  h1->Draw("HIST ");
  h2->Draw("HIST sames");
  h3->Draw("HIST sames");
  h4->Draw("HIST sames");
 if (miny>-1 && maxy >-1)
  h1->GetYaxis()->SetRangeUser(miny,maxy);
  else if (miny!=-1 && maxy==-1)
    h1->SetMinimum(miny);
  else if (miny==-1 && maxy!=-1)
     h1->SetMaximum(maxy);
   TLegend * leg = new TLegend(0.70,0.70,1,1);
   leg->AddEntry(h1,leg1);
   leg->AddEntry(h2,leg2);
   leg->AddEntry(h3,leg3);
   leg->AddEntry(h4,leg4);
   leg->SetFillColor(kWhite);
   leg->SetLineColor(kWhite);
   leg->SetBorderSize(0);
   leg->Draw();
   cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
   if (Logy) data_mc_canvas->SetLogy();

   return data_mc_canvas;

   }

TCanvas *canvas_1plot(TH1F * h1, TString canvas, bool Logy, TString Labelx,TString Labely, bool marker=false){

  TCanvas *data_mc_canvas = new TCanvas(canvas,canvas,700,700);
  gStyle->SetPadBorderMode(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(1);
  h1->SetLineColor(1);
  h1->SetLineWidth(2);
  h1->GetYaxis()->SetTitle(Labely);
  h1->GetXaxis()->SetTitle(Labelx);
  h1->Draw("P E1");
//  else h1->Draw("HIST");
  if (Logy) data_mc_canvas->SetLogy();
  cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
  return data_mc_canvas;
   }

TCanvas *canvas_1graph(TGraph * gr, TString canvas, TString Labelx,TString Labely){

  TCanvas *data_mc_canvas = new TCanvas(canvas,canvas,700,700);
  gStyle->SetPadBorderMode(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(1);
  gr->SetMarkerSize(2);
  gr->SetLineColor(1);
  gr->SetMarkerStyle(kFullDotLarge);
  gr->SetTitle(" ;"+ Labelx+" ;"+ Labely);
  gr->Draw("A*");
  cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
  return data_mc_canvas;
             }
TCanvas *canvas_3graph(TGraph * gr1, TGraph *gr2 ,TGraph *gr3, TString canvas, TString Labelx,TString Labely,TString leg1,TString leg2,TString leg3){

  TCanvas *data_mc_canvas = new TCanvas(canvas,canvas,700,700);
  gStyle->SetPadBorderMode(0); gStyle->SetOptStat(0); gStyle->SetOptTitle(1);
  gr1->SetMarkerColor(1); gr1->SetLineColor(1);
  gr2->SetMarkerColor(2); gr2->SetLineColor(2);
  gr3->SetMarkerColor(3); gr3->SetLineColor(3);
  TLegend * leg = new TLegend(0.70,0.70,1,1);
  leg->AddEntry(gr1,leg1); leg->AddEntry(gr2,leg2); leg->AddEntry(gr3,leg3);
  auto mgr=new TMultiGraph();
  mgr->Add(gr1); mgr->Add(gr2); mgr->Add(gr3);
  mgr->SetTitle(" ;"+ Labelx+" ;"+ Labely);
   mgr->Draw("AL*"); leg->SetTextFont(42); leg->SetFillColor(kWhite);
  leg->SetLineColor(kWhite); leg->SetBorderSize(0); leg->Draw();
  cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
  return data_mc_canvas;
             }

TCanvas *canvas_5graph(TGraph * gr1, TGraph *gr2 , TGraph * gr3,TGraph * gr4,TGraph * gr5, TString canvas, TString Labelx,TString Labely,TString leg1,TString leg2,TString leg3,TString leg4,TString leg5){

  TCanvas *data_mc_canvas = new TCanvas(canvas,canvas,700,700);
  gStyle->SetPadBorderMode(0); gStyle->SetOptStat(0); gStyle->SetOptTitle(1);
  gr1->SetMarkerColor(1); gr1->SetLineColor(1);
  gr2->SetMarkerColor(2); gr2->SetLineColor(2);
  gr3->SetMarkerColor(3); gr3->SetLineColor(3);
  gr4->SetMarkerColor(4); gr4->SetLineColor(4);
  gr5->SetMarkerColor(kMagenta); gr5->SetLineColor(kMagenta);
  TLegend * leg = new TLegend(0.70,0.70,1,1);
  leg->AddEntry(gr1,leg1); leg->AddEntry(gr2,leg2); leg->AddEntry(gr3,leg3);
  leg->AddEntry(gr4,leg4); leg->AddEntry(gr5,leg5);
  auto mgr=new TMultiGraph();
  mgr->Add(gr1); mgr->Add(gr2); mgr->Add(gr3); mgr->Add(gr4); mgr->Add(gr5);
  mgr->SetTitle(" ;"+ Labelx+" ;"+ Labely);
  mgr->Draw("AL*"); leg->SetTextFont(42); leg->SetFillColor(kWhite);
  leg->SetLineColor(kWhite); leg->SetBorderSize(0); leg->Draw();
  cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
  return data_mc_canvas;
             }
  TCanvas *canvas_2graph(TGraph * gr1, TGraph *gr2 , TString canvas, TString Labelx,TString Labely,TString leg1,TString leg2){

  TCanvas *data_mc_canvas = new TCanvas(canvas,canvas,700,700);
  gStyle->SetPadBorderMode(0); gStyle->SetOptStat(0); gStyle->SetOptTitle(1);
  gr1->SetMarkerColor(4); gr1->SetLineColor(4);
  gr2->SetMarkerColor(2); gr2->SetLineColor(2);
  gr1->SetMarkerStyle(20);
  gr2->SetMarkerStyle(21);
  TLegend * leg = new TLegend(0.80,0.80,0.94,0.94);
  leg->AddEntry(gr1,leg1); leg->AddEntry(gr2,leg2); 
  
  auto mgr=new TMultiGraph();
  mgr->Add(gr1); mgr->Add(gr2); 
  mgr->SetTitle(" ;"+ Labelx+" ;"+ Labely);
   mgr->Draw("AP"); leg->SetTextFont(42); leg->SetFillColor(kWhite);
  leg->SetLineColor(kWhite); leg->SetBorderSize(0); leg->Draw();
  cms().Draw("sames");
  head().Draw("sames");
  extra().Draw("sames");
  return data_mc_canvas;
             }

TCanvas *canvas_2plot(TH1F * h1, TH1F * h2, TString canvas, bool Logy, bool norm,double miny, double maxy, TString Labelx,TString Labely, TString leg1,TString leg2,bool dashed=false){

  TCanvas *data_mc_canvas = new TCanvas(canvas,canvas,700,700);
  gStyle->SetPadBorderMode(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(1);

  h1->SetLineColor(kRed);
  h1->SetMarkerColor(kRed);
  h2->SetLineColor(kBlue);
  h2->SetMarkerColor(kBlue);
  h1->SetLineWidth(3);
  h2->SetLineWidth(3);
 if (dashed){
   h1->SetLineColor(kBlack);
   h2->SetLineColor(kBlack);
  }

  h1->GetYaxis()->SetTitle(Labely);
  h1->GetXaxis()->SetTitle(Labelx);

  if (norm) {
      h1->Scale(1/h1->Integral());
      h2->Scale(1/h2->Integral());
   }

  h1->Draw("HIST ");
  h2->Draw("HIST sames");

  if(miny!=-1 && maxy!=-1)
    h1->GetYaxis()->SetRangeUser(miny,maxy);
  else if (miny!=-1 && maxy==-1)
    h1->SetMinimum(miny);
  else if (miny==-1 && maxy!=-1)
     h1->SetMaximum(maxy);
  
   TLegend * leg = new TLegend(0.70,0.75,0.95,0.95);
   leg->AddEntry(h1,leg1);
   leg->AddEntry(h2,leg2);
   leg->SetFillColor(kWhite);
   leg->SetLineColor(kWhite);
   leg->SetBorderSize(0);
   leg->Draw();

   if (Logy) data_mc_canvas->SetLogy();
   cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
   return data_mc_canvas;

   }



TCanvas *canvas_2plot_ratio(TH1F * h1, TH1F * h2, TString canvas, bool Logy, bool norm,double miny, double maxy, TString Labelx,TString Labely, TString leg1,TString leg2,bool dashed=false){

  TCanvas *data_mc_canvas = new TCanvas(canvas,canvas,700,700);
    gStyle->SetPadBorderMode(0);
    gStyle->SetOptStat(0);
    gStyle->SetOptTitle(1);
  TPad *pad1 = new TPad("pad1","This is pad1",0.,0.30,1.,1.);
  TPad *pad2 = new TPad("pad2","This is pad2",0.,0.,1.,0.30);
  pad1->SetFillColor(kWhite);
  pad2->SetFillColor(kWhite);
  pad1->Draw();
  pad2->Draw();

  pad1->cd();
   gPad->SetBottomMargin(0);
  gPad->SetLeftMargin(0.10); gPad->SetRightMargin(0.03);

  h1->SetLineColor(kRed);
  h2->SetLineColor(kBlue);
  h1->SetMarkerStyle(2);
  h2->SetMarkerStyle(2);

   if (dashed){
   h1->SetLineColor(kBlack);
   h2->SetLineColor(kBlack);
  }
  h1->GetYaxis()->SetTitle(Labely);
  h1->GetXaxis()->SetTitle(Labelx);


  if (norm) {
      h1->Scale(1/h1->Integral());
      h2->Scale(1/h2->Integral());
   }
 // h1->SetMarkerSize(2);
  h1->Draw("HIST ");
  h2->Draw("HIST sames");
 
  
  if(miny!=-1 && maxy!=-1)
    h1->GetYaxis()->SetRangeUser(miny,maxy);
  else if (miny!=-1 && maxy==-1)
    h1->SetMinimum(miny);
  else if (miny==-1 && maxy!=-1)
     h1->SetMaximum(maxy);
  
   TLegend * leg = new TLegend(0.70,0.70,1,1);
   leg->AddEntry(h1,leg1);
   leg->AddEntry(h2,leg2);
   leg->SetFillColor(kWhite);
   leg->SetLineColor(kWhite);
   leg->SetBorderSize(0);
   leg->Draw();
   cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
   if (Logy) data_mc_canvas->SetLogy();
   pad2->cd();                                                                     gPad->SetTopMargin(0);
   gPad->SetBottomMargin(0.2);
   gPad->SetLeftMargin(0.10); gPad->SetRightMargin(0.03);
   
   TH1F* hdif1=(TH1F*)h1->Clone();
    TH1F* hdif2=(TH1F*)h2->Clone();
     hdif1->SetTitle(" ");
    hdif1->GetYaxis()->SetTitle(""+leg1+"/"+leg2+"");
    hdif1->GetYaxis()->SetLabelSize(0.07);
    hdif1->GetYaxis()->SetTitleSize(0.1);
    hdif1->GetYaxis()->SetTitleOffset(0.4);
   hdif1->GetXaxis()->SetLabelSize(0.1);
    hdif1->GetXaxis()->SetTitleSize(0.1);
    hdif1->GetXaxis()->SetTitleOffset(0.7);

    hdif1->Divide(hdif2);
    hdif1->Draw("P");
    hdif1->SetMarkerStyle(kFullCircle);
   hdif1->SetMarkerSize(1);

   return data_mc_canvas;

   }

TCanvas *canvas_2plot_dif(TH1F * h1, TH1F * h2, TString canvas, bool Logy, bool norm,double miny, double maxy, TString Labelx,TString Labely, TString leg1,TString leg2){

  TCanvas *data_mc_canvas = new TCanvas(canvas,canvas,700,700);
    gStyle->SetPadBorderMode(0);
    gStyle->SetOptStat(0);
    gStyle->SetOptTitle(1);
  TPad *pad1 = new TPad("pad1","This is pad1",0.,0.30,1.,1.);
  TPad *pad2 = new TPad("pad2","This is pad2",0.,0.,1.,0.30);
  pad1->SetFillColor(kWhite);
  pad2->SetFillColor(kWhite);
  pad1->Draw();
  pad2->Draw();

  pad1->cd();
   gPad->SetBottomMargin(0);
  gPad->SetLeftMargin(0.10); gPad->SetRightMargin(0.03);

  h1->SetLineColor(kRed);
  h2->SetLineColor(kBlue);
  h1->SetMarkerStyle(2);
   h2->SetMarkerStyle(2);
   h1->SetLineColor(kRed);
  h1->GetYaxis()->SetTitle(Labely);
  h1->GetXaxis()->SetTitle(Labelx);
h2->SetMarkerColor(kBlue);
h1->SetMarkerColor(kRed);

  if (norm) {
      h1->Scale(1/h1->Integral());
      h2->Scale(1/h2->Integral());
   }
  
  h1->Draw("HIST ");
  h2->Draw("HIST sames");
  cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
  if(miny!=-1 && maxy!=-1)
    h1->GetYaxis()->SetRangeUser(miny,maxy);
  else if (miny!=-1 && maxy==-1)
    h1->SetMinimum(miny);
  else if (miny==-1 && maxy!=-1)
     h1->SetMaximum(maxy);
  
   TLegend * leg = new TLegend(0.70,0.70,1,1);
   leg->AddEntry(h1,leg1);
   leg->AddEntry(h2,leg2);
   leg->SetFillColor(kWhite);
   leg->SetLineColor(kWhite);
   leg->SetBorderSize(0);
   leg->Draw();

   if (Logy) data_mc_canvas->SetLogy();
   pad2->cd();                                                                     gPad->SetTopMargin(0);
   gPad->SetBottomMargin(0.2);
   gPad->SetLeftMargin(0.10); gPad->SetRightMargin(0.03);
   
   TH1F* hdif1=(TH1F*)h1->Clone();
    TH1F* hdif2=(TH1F*)h2->Clone();
     hdif1->SetTitle(" ");
    hdif1->GetYaxis()->SetTitle("#Delta ("+leg1+","+leg2+")");
    hdif1->GetYaxis()->SetLabelSize(0.07);
    hdif1->GetYaxis()->SetTitleSize(0.1);
    hdif1->GetYaxis()->SetTitleOffset(0.4);
   hdif1->GetXaxis()->SetLabelSize(0.1);
    hdif1->GetXaxis()->SetTitleSize(0.1);
    hdif1->GetXaxis()->SetTitleOffset(0.7);

    hdif1->Add(hdif2,-1);
    hdif1->Draw("P");
    hdif1->SetMarkerStyle(kFullCircle);
   hdif1->SetMarkerSize(1);
    hdif1->SetMarkerColor(1);

   return data_mc_canvas;

   }


TCanvas *canvas_3plot(TH1F * h1, TH1F * h2, TH1F * h3, TString canvas, bool Logy, bool norm,double miny, double maxy, TString Labelx,TString Labely, TString leg1,TString leg2,TString leg3){

  TCanvas *data_mc_canvas = new TCanvas(canvas,canvas,700,700);
    gStyle->SetPadBorderMode(0);
  gStyle->SetOptStat(0);
    gStyle->SetOptTitle(1);

  h1->SetLineColor(kRed);
  h2->SetLineColor(kBlue);
  h3->SetLineColor(kBlack);

  h1->SetLineWidth(3);
  h2->SetLineWidth(3);
  h3->SetLineWidth(3);
 
  h1->GetYaxis()->SetTitle(Labely);
  h1->GetXaxis()->SetTitle(Labelx);

  if (norm) {
      h1->Scale(1/h1->Integral());
      h2->Scale(1/h2->Integral());
      h3->Scale(1/h3->Integral());
   }

  h1->Draw("HIST ");
  h2->Draw("HIST sames");
  if(leg3!="data")
  h3->Draw("HIST sames");
  else
   h3->Draw("sames");

    if(miny!=-1 && maxy!=-1)
  h1->GetYaxis()->SetRangeUser(miny,maxy);
   else if (miny!=-1 && maxy==-1)
    h1->SetMinimum(miny);
  else if (miny==-1 && maxy!=-1)
     h1->SetMaximum(maxy);
   TLegend * leg = new TLegend(0.70,0.70,1,1);
   leg->AddEntry(h1,leg1);
   leg->AddEntry(h2,leg2);
   leg->AddEntry(h3,leg3);
   leg->SetTextFont(42);
   leg->SetFillColor(kWhite);
   leg->SetLineColor(kWhite);
   leg->SetBorderSize(0);
   leg->Draw();
   cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
   if (Logy) data_mc_canvas->SetLogy();

   return data_mc_canvas;

   }





TCanvas *canvas_2d(TH2F * h2,TString name, TString xaxis, TString yaxis){
TCanvas * ctemp=new TCanvas(name,name,700,700);
gStyle->SetOptStat(0);
h2->Draw("COLZ");
h2->GetXaxis()->SetTitle(xaxis);
h2->GetYaxis()->SetTitle(yaxis);
cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
return ctemp;
}

TCanvas * canvas_prof(TH1F * h1, TH1F * h2, TH1F * h3,double xax[],double xerr[], TString name, TString title){
double yax[3]={h1->GetMean(),h2->GetMean(),h3->GetMean()};
double yerr[3]={h1->GetStdDev(),h2->GetStdDev(),h3->GetStdDev()};
TGraphErrors * gr=new TGraphErrors(3,xax,yax,xerr,yerr);
TCanvas * ct= new TCanvas(name,name,700,700);
gr->SetTitle(title);
gr->Draw("*A");
cms().Draw("sames");
   head().Draw("sames");
   extra().Draw("sames");
return ct;
}

TCanvas * canvas_proj(TH2F * h1,TString name, TString titleX){
TCanvas * ct=new TCanvas("c"+name,"c"+name,700,700);
TH1D *hp1=h1->ProjectionY("h1"+name,0,1);
TH1D *hp2=h1->ProjectionY("h2"+name,1,2);
TH1D *hp3=h1->ProjectionY("h3"+name,2,3);

hp1->Draw("HIST");
hp2->Draw("HIST sames");
hp3->Draw("HIST sames");

hp1->SetLineColor(1);
hp2->SetLineColor(2);

hp1->SetTitle(";"+titleX);

hp1->Scale(1/hp1->Integral());
hp2->Scale(1/hp2->Integral());
hp3->Scale(1/hp3->Integral());

return ct;
}


TCanvas * canvas_prof(TH2F * h1,TString name, TString title){
TCanvas * ct=new TCanvas("c"+name,"c"+name,700,700);
 TH1D *hp1=h1->ProfileX("h1"+name,1,-1,"s");
 hp1->Draw();

hp1->SetLineColor(1);
//hp3->SetLineColor(3);

hp1->SetTitle(title);

return ct;
}

TCanvas * canvas_2prof(TH2F * h1,TH2F * h2,TString name, TString titleX, TString titleY){
TCanvas * ct=new TCanvas("c"+name,"c"+name,700,700);
 TH1D *hp1=h1->ProfileX("h1"+name,1,-1,"s");
 TH1D *hp2=h2->ProfileX("h2"+name,1,-1,"s");
 hp1->Draw();
 hp2->Draw("sames");

hp1->SetLineColor(1);
hp2->SetLineColor(2);

hp1->SetTitle("#font[22]{CMS} #font[12]{Preliminary};"+titleX+";"+titleY);

return ct;
}

