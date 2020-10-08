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
    fname = 'FakeHists_DYJetsToLL.root'
    print 'Histogram file not specified, will run default file:',fname

try:foname =sys.argv[2]
except:
    foname = 'Alpha.root'
    print 'Output file not specified, will create output as: Kappa.root'
file  = TFile(fname)
file.ls()

print 'contents of file'
pause()

#if 'Run' in fname : isdata = True
#else: isdata = False
isdata =True
splitFit = False

funcs = {}

keys = file.GetListOfKeys()

c1 = mkcanvas('c1')
fnew = TFile(foname,'recreate')
fnew.cd()

for key in keys:
    name = key.GetName()
    if not (('MBSRnum' in name or 'SBSRnum' in name) and ('_0' in name or '_all' in name) and 'inclusive' in name and ('_nDtrks_' in name or '_nVtx_' in name)): continue
    print 'histo name', name
    pause()

    hnum   = file.Get(name)
    hnum.SetLineColor(kViolet)
    if 'Run' in fname: 
    	hnum.SetLineColor(kBlack)
    	hnum.SetMarkerStyle(20)
    	hnum.SetMarkerSize(.85*hnum.GetMarkerSize())
    hden    = file.Get(name.replace('BSRnum','BCRden'))
    ratname = name.replace('SBSRnum','Alpha').replace('MBSRnum','Alpha')
    print 'ratname', ratname
    hratio = hnum.Clone(ratname)
    hratio.Divide(hden)
    

    
    hratio.SetTitle('')
    hratio.GetXaxis().SetTitle(name.replace('SBSRnum',''))  #  Set it to nVtx or NameWizard 
    hratio.GetYaxis().SetTitle('#kappa = n(SBSR)/n(SBCR)')    
    hratio.GetYaxis().SetLabelSize(0.05)
    hratio.GetXaxis().SetLabelSize(0.05)    
    hratio.GetYaxis().SetTitleOffset(1)

    if isdata: funcs['f1'+ratname] =  TF1('f1'+ratname,'[0]*TMath::Landau(x,[1],[2])',1,55) #TF1('f1'+ratname,'[0]*TMath::Landau(x,[1],[2])',1,80)
    if not isdata: funcs['f1'+ratname] = TF1('f1'+ratname,'[0]*TMath::Landau(x,[1],[2])',1,55)

    funcs['f1'+ratname].SetParameter(0,3)
    funcs['f1'+ratname].SetParameter(1,65)
    funcs['f1'+ratname].SetParameter(2,26)


    funcs['f1'+ratname].SetLineColor(hratio.GetLineColor())
    
    hratio.Fit('f1'+ratname,'','SN',1,55) # replace 1000 by 2500 for PtBinEdges
    hratio.SetLineColor(hratio.GetLineColor())
    hratio.Draw()
    pause()
    


    if isdata:
        variation_up = 'f1'+ratname+'_up'
        variation_down ='f1'+ratname+'_down'
        variation_up1 = 'f1'+ratname+'_up1'
        variation_down1 ='f1'+ratname+'_down1'
        variation_up1 = TF1(variation_up1,'1.8*[0]*TMath::Landau(x,[1],[2])',40,55)
        variation_down1 = TF1(variation_down1,'0.4*[0]*TMath::Landau(x,[1],[2])',40,55)

        variation_up = TF1(variation_up,'[0]*TMath::Landau(x,[1],[2])',1,40)
        variation_down = TF1(variation_down,'[0]*TMath::Landau(x,[1],[2])',1,40)

        variation_up1.SetParameters(funcs['f1'+ratname].GetParameter(0) + 0*funcs['f1'+ratname].GetParError(0), funcs['f1'+ratname].GetParameter(1) + 0*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) + 0*funcs['f1'+ratname].GetParError(2))
        variation_down1.SetParameters(funcs['f1'+ratname].GetParameter(0) - 0*funcs['f1'+ratname].GetParError(0), funcs['f1'+ratname].GetParameter(1) - 0*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) - 0*funcs['f1'+ratname].GetParError(2))


        variation_up.SetParameters(funcs['f1'+ratname].GetParameter(0) + 1*funcs['f1'+ratname].GetParError(0), funcs['f1'+ratname].GetParameter(1) + 0*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) + 0*funcs['f1'+ratname].GetParError(2))
        variation_down.SetParameters(funcs['f1'+ratname].GetParameter(0) - 1*funcs['f1'+ratname].GetParError(0), funcs['f1'+ratname].GetParameter(1) - 0*funcs['f1'+ratname].GetParError(1), funcs['f1'+ratname].GetParameter(2) - 0*funcs['f1'+ratname].GetParError(2))

        variation_up.Draw('same')
        variation_down.Draw('same')
        hratio.GetListOfFunctions().Add(variation_up)
        hratio.GetListOfFunctions().Add(variation_down)
        variation_up1.Draw('same')
        variation_down1.Draw('same')
        hratio.GetListOfFunctions().Add(variation_up1)
        hratio.GetListOfFunctions().Add(variation_down1)


    leg = mklegend(x1=.22, y1=.66, x2=.79, y2=.82)
    legname = ratname.split('_')[-1].replace('eta','eta ')
#    if 'Gen' in name: legname+=' (DY MC, 2016 geom)'
    leg.AddEntry(hratio,legname)
    leg.Draw()
    c1.Update()
    pause()
    fnew.cd()
    hratio.Write(hratio.GetName())
    c1.Write('c_'+hratio.GetName())
    hratio.Write()
    funcs['f1'+ratname].Write()
    if isdata:
        variation_up.Write()
        variation_down.Write()
        variation_up1.Write()
        variation_down1.Write()
print 'just made', fnew.GetName()
fnew.Close()
exit(0)
