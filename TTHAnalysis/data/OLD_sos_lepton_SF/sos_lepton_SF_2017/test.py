import ROOT

f = ROOT.TFile.Open("mu_tracking_highpt.root","read")
g = f.Get("ratio_eff_eta3_dr030e030_corr")

#f = ROOT.TFile.Open("mu_tracking_lowpt.root","read")
#g = f.Get("ratio_eff_eta3_tk0_dr030e030_corr")

for i in range(g.GetN()):
	print (i, g.GetX()[i]-g.GetErrorXlow(i), g.GetX()[i], g.GetX()[i]+g.GetErrorXhigh(i), g.GetY()[i])

f.Close()
