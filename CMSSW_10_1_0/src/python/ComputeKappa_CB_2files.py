from ROOT import *
from utils import *
from namelib import *
import sys
from random import shuffle
#gROOT.SetBatch(1)

gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendTextSize(0.026)
try:fname =sys.argv[1]
except:
    fname = 'TagnProbe_DYJetsToLL.root'
    print 'Histogram file not specified, will run default file:',fname

try:foname =sys.argv[2]
except:
    foname = 'Kappa.root'
    print 'Output file not specified, will create output as: Kappa.root'
file  = TFile(fname)
file.ls()

print 'contents of file'
pause()

#isdata = False #just for setting different parameters for Landau fits different parmeters for DATA and MC
splitFit = False   # To split the Fit in different Pt ranges for Barrel and EC.   Better not to use True option

if 'Run' in fname : isdata = True
else: isdata = False

funcs = {}

keys = file.GetListOfKeys()
#gROOT.ProcessLine("TVirtualFitter *fitter = TVirtualFitter::GetFitter()")
c1 = mkcanvas('c1')
#c2 = mkcanvas('c2')
fnew = TFile(foname,'recreate')
fnew.cd()

for key in keys:
    name = key.GetName()
    if not 'ProbePtDT_eta' in name: continue
    
    print 'histo name', name
    pause()

    hnum   = file.Get(name)
    if 'Gen' in name and 'Run' in fname: continue
    if 'Gen' in name: 
        if 'DY' in fname: hnum.SetLineColor(kAzure)
        if 'WJ' in fname: hnum.SetLineColor(28)
    else:
        if 'DY' in fname: hnum.SetLineColor(kViolet)
        if 'WJ' in fname: hnum.SetLineColor(28)
    if 'Run' in fname: 
    	hnum.SetLineColor(kBlack)
    	hnum.SetMarkerStyle(20)
    	hnum.SetMarkerSize(.85*hnum.GetMarkerSize())
    hden    = file.Get(name.replace('_num','_den').replace('DT','RECO'))
    ratname = name.replace('_num','').replace('DT','Kappa')
    print 'ratname', ratname
    hratio = hnum.Clone(ratname)
    fake = hnum.Clone(ratname)
    hratio.Divide(hden)
    hratio2 = hnum.Clone('hratio2')
#    if 'eta1.4442to1.566' in ratname: continue
    if 'Mu' in ratname : continue
#    if 'El' in ratname : continue
    if 'El' in ratname and 'eta0' in ratname: hratio.Scale(0.67)
    if 'El' in ratname and 'eta1' in ratname: hratio.Scale(0.85) #0.79)
    if 'Mu' in ratname and 'eta0' in ratname: hratio.Scale(0.8)
    if 'Mu' in ratname and 'eta1' in ratname: hratio.Scale(0.95)
    
    hratio.SetTitle('')
    hratio.GetXaxis().SetTitle('p_{T}[GeV]')
    hratio.GetYaxis().SetTitle('#kappa = n(DT)/n(reco-lep)')    
    hratio.GetYaxis().SetLabelSize(0.05)
    hratio.GetXaxis().SetLabelSize(0.05)    
    hratio.GetYaxis().SetTitleOffset(1.25)
#    hratio.Draw()
    #if 'El' in name: funcs['f1'+ratname] = TF1('f1'+ratname,'[0]+[1]/pow(x,.5)+[2]*exp(-[3]*pow(x-[4],2))',20,2000)
    #if 'Mu' in name: funcs['f1'+ratname] = TF1('f1'+ratname,'[0]+([1]/pow(x,2)+[2]/x)*exp(-[3]*pow(x-[4],2))',20,2000)
	#funcs['f1'+ratname] = TF1('f1'+ratname,'[0]+([1]/pow(x,1)+[2]/pow(x,2))+[3]*exp(-[4]*pow(x-350,2))',20,2000)
    #funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0]+([1]/pow(x,1)+[2]/pow(x,2)+[5]/pow(x,3))+0.0002*exp(-[3]*pow(x-325,2))',20,2000)
    #funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0] + [1]/pow(x,1) + [2]/pow(x,2)+[5]/pow(x,0.5) + 0.0002*exp(-[3]*pow(x-325,2))',20,2000)
    #funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0] + [1]/pow(x,1) + [2]*x +[3]*exp(-[4]*(x-325)) ',20,2000)
    #funcs['f1'+ratname] = TF1('f1'+ratname,'0.01*[0] + 0.01*[1]/x + 0.01*[2]/x/x + [3]*exp(-[4]*x)',20,2500)

#    funcs['f1'+ratname] = TF1('f1'+ratname,'0.1*[0] + 0.1*[1]/x + 0.1*[2]/pow(x,2) + [3]*exp(-[4]*x)',20,1000) # replace 1000 by 2500 for PtBinEdges upto 2500

    if not splitFit: funcs['f1'+ratname] = TF1('f1'+ratname,'[0]*TMath::Landau(x,[1],[2])',20,710)
    else:
        if '2.4' in name:    funcs['f1'+ratname] = TF1('f1'+ratname,'[0]*TMath::Landau(x,[1],[2])',20,300)
        else: funcs['f1'+ratname] = TF1('f1'+ratname,'[0]*TMath::Landau(x,[1],[2])',20,600)

    if isdata:
        print 'name of hist: ', name
        if 'MuProbePtDT_eta1.566to2.4' in name:
            funcs['f1'+ratname].SetParameter(0,.00001)
            funcs['f1'+ratname].SetParameter(1,10)
            funcs['f1'+ratname].SetParameter(2,2)
        else:
            funcs['f1'+ratname].SetParameter(0,.05)
            funcs['f1'+ratname].SetParameter(1,200)
            funcs['f1'+ratname].SetParameter(2,70)

    if not isdata:
        funcs['f1'+ratname].SetParameter(0,.00001)
        funcs['f1'+ratname].SetParameter(1,10)
        funcs['f1'+ratname].SetParameter(2,2)
#    funcs['f1'+ratname].SetParLimits(0,0, .9)
#    funcs['f1'+ratname].SetParLimits(0,0, 0.9)
    #funcs['f1'+ratname].SetParLimits(1,0, 9999)
    #funcs['f1'+ratname].SetParLimits(2,0, 9999)
    #funcs['f1'+ratname].SetParLimits(3,0, 0.999)
    #funcs['f1'+ratname].SetParLimits(4,200, 400)
    funcs['f1'+ratname].SetLineColor(hratio.GetLineColor())
 #   hratio.Fit('f1'+ratname,'','SN',20,1000) 
    
    if not splitFit: hratio.Fit('f1'+ratname,'B','SN',20,710) # replace 1000 by 2500 for PtBinEdges
    else:
        if '2.4' in name:   hratio.Fit('f1'+ratname,'','SN',20,300) # replace 1000 by 2500 for PtBinEdges
        else: hratio.Fit('f1'+ratname,'','SN',20,600)
#    funcs['f1'+ratname].SetLineColor(hratio.GetLineColor())
    hratio.SetLineColor(hratio.GetLineColor())
#    gROOT.ProcessLine("TVirtualFitter *fitter = TVirtualFitter::GetFitter()")
#    gROOT.ProcessLine("(TVirtualFitter::GetFitter())->GetConfidenceIntervals(hratio, .95)")
#    pause()
#    fitter.GetConfidenceIntervals(hratio, .5)
#    hratio.SetFillColor(2)
    #hratio.Draw()
    print funcs['f1'+ratname].GetParameter(0)
    print funcs['f1'+ratname].GetParError(0)
    if isdata:
        base = 'f1'+ratname+'base'
        variation_up = 'f1'+ratname+'_up'
        variation_down ='f1'+ratname+'_down'
        base = TF1(base,'[0]*TMath::Landau(x,[1],[2])',20,710)
        variation_up = TF1(variation_up,'[0]*TMath::Landau(x,[1],[2])',20,710)
        variation_down = TF1(variation_down,'[0]*TMath::Landau(x,[1],[2])',20,710)
        if 'El' in ratname and 'eta0' in ratname:
            base.SetParameters(funcs['f1'+ratname].GetParameter(0), funcs['f1'+ratname].GetParameter(1), funcs['f1'+ratname].GetParameter(2))
            variation_up.SetParameters(funcs['f1'+ratname].GetParameter(0) + 1.65*funcs['f1'+ratname].GetParError(0), funcs['f1'+ratname].GetParameter(1) + 1*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) + 1*funcs['f1'+ratname].GetParError(2))
            variation_down.SetParameters(funcs['f1'+ratname].GetParameter(0) - 1.65*funcs['f1'+ratname].GetParError(0), funcs['f1'+ratname].GetParameter(1) - 1*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) - 1*funcs['f1'+ratname].GetParError(2))
        if 'Mu' in ratname and 'eta0' in ratname:
            base.SetParameters(funcs['f1'+ratname].GetParameter(0),0.95*funcs['f1'+ratname].GetParameter(1), 1.02*funcs['f1'+ratname].GetParameter(2))
            variation_up.SetParameters(funcs['f1'+ratname].GetParameter(0) + 1.7*funcs['f1'+ratname].GetParError(0), 0.95*funcs['f1'+ratname].GetParameter(1) + 1*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) + 1.35*funcs['f1'+ratname].GetParError(2))
            variation_down.SetParameters(funcs['f1'+ratname].GetParameter(0) - 1.3*funcs['f1'+ratname].GetParError(0), 0.95*funcs['f1'+ratname].GetParameter(1) - 1*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) - 1.1*funcs['f1'+ratname].GetParError(2))

        if 'El' in ratname and 'eta1' in ratname:
            base.SetParameters(funcs['f1'+ratname].GetParameter(0), funcs['f1'+ratname].GetParameter(1), funcs['f1'+ratname].GetParameter(2))
            variation_up.SetParameters(funcs['f1'+ratname].GetParameter(0) + 1.2*funcs['f1'+ratname].GetParError(0), funcs['f1'+ratname].GetParameter(1) + 1*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) + 1*funcs['f1'+ratname].GetParError(2))
            variation_down.SetParameters(funcs['f1'+ratname].GetParameter(0) - 1.2*funcs['f1'+ratname].GetParError(0), funcs['f1'+ratname].GetParameter(1) - 1*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) - 1*funcs['f1'+ratname].GetParError(2))
        if 'Mu' in ratname and 'eta1' in ratname:
            base.SetParameters(1.15*6.76402e-04,-4.16692e+04,3.51187e+05)
#            base.SetParameters(funcs['f1'+ratname].GetParameter(0), funcs['f1'+ratname].GetParameter(1), 0*funcs['f1'+ratname].GetParameter(2))
            variation_up.SetParameters(funcs['f1'+ratname].GetParameter(0) + 0.7*funcs['f1'+ratname].GetParError(0), funcs['f1'+ratname].GetParameter(1) + 1*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) + 1*funcs['f1'+ratname].GetParError(2))
            variation_down.SetParameters(funcs['f1'+ratname].GetParameter(0) - 1.2*funcs['f1'+ratname].GetParError(0), funcs['f1'+ratname].GetParameter(1) - 1*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) - 1*funcs['f1'+ratname].GetParError(2))
    
        base.SetLineColor(kBlue)
        base.Draw('same')
        variation_up.Draw('same')
        variation_down.Draw('same')
        hratio.GetListOfFunctions().Add(base)
        hratio.GetListOfFunctions().Add(variation_up)
        hratio.GetListOfFunctions().Add(variation_down)
    

    base.SetLineColor(kBlue)
    leg = mklegend(x1=.22, y1=.66, x2=.79, y2=.82)
    legname = ratname.split('_')[-1].replace('eta','eta ')
    if 'Gen' in name: legname+=' (DY MC, 2016 geom)'
    leg.AddEntry(hratio,legname)
    leg.Draw()
    c1.Update()
    fnew.cd()
    hratio.Write(hratio.GetName())
    c1.Write('c_'+hratio.GetName())
    #hratio.Write()
    funcs['f1'+ratname].Write()
    if isdata:
        base.Write()
        variation_up.Write()
        variation_down.Write()

print 'just made', fnew.GetName()
fnew.Close()
exit(0)
