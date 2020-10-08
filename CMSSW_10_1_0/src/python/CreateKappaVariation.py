from ROOT import *
from utils import *
from namelib import *
import sys
import numpy as np

from random import shuffle

gROOT.SetBatch(1)

gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendTextSize(0.026)
try:fname =sys.argv[1]
except:
    fname = 'Kappa.root'
    print 'Histogram file not specified, will run default file:',fname

try:foname =sys.argv[2]
except:
    foname = 'KappaVariation.root'
    print 'Output file not specified, will create output as: KappaVariation.root'
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
variation = ['BASE',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
c1 = mkcanvas('c1')
fnew = TFile(foname,'recreate')
fnew.cd()
colors = [1,40,43,46,30,38, 28, 9,4,2, 6, 8, 3, 31, 36, 38, 24, 13, 29, 7,35,20, 5]
for key in keys:
    name = key.GetName()
    if 'c_' in name: continue
    if 'f1h' in name: continue
    if 'eta1.4442to1.566' in name: continue
    if not 'Kappa_' in name: continue

    print 'histo name', name
    pause()

    
    kappa_original   = file.Get(name)

    for ivar, var in enumerate(variation):
        if ivar > 15: break
        if ivar == 0: ratname = name+'_'+str(var)
        else: ratname = name+'_variation_'+str(var)
        print ratname
        pause()
    
        kappa = kappa_original.Clone(ratname)
        x_axis = kappa.GetXaxis()
        if ivar > 0:
            for ibin in range(1,x_axis.GetNbins()+1):
                mean = kappa.GetBinContent(ibin)
                sigma = kappa.GetBinError(ibin)
                newcontent=np.random.normal(mean,sigma)
                kappa.SetBinContent(ibin, newcontent)

        kappa.SetLineColor(colors[ivar])
        kappa.SetMarkerStyle(20)
        kappa.SetMarkerSize(.85*kappa.GetMarkerSize())
        kappa.SetTitle('')
        kappa.GetXaxis().SetTitle('p_{T}[GeV]')
        kappa.GetYaxis().SetTitle('#kappa = n(DT)/n(reco-lep)')    
        kappa.GetYaxis().SetLabelSize(0.05)
        kappa.GetXaxis().SetLabelSize(0.05)    
        kappa.GetYaxis().SetTitleOffset(1.25)

        funcs['f1'+ratname] = TF1('f1'+ratname,'[0]*TMath::Landau(x,[1],[2])',20,310)
        if isdata:
            print 'name of hist: ', name
            if 'Mu' in name and 'eta1.566to2.4' in name:
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
        funcs['f1'+ratname].SetLineColor(kappa.GetLineColor())
    
        kappa.Fit('f1'+ratname,'','SN',20,310) # replace 1000 by 2500 for PtBinEdges

        kappa.SetLineColor(kappa.GetLineColor())
        kappa.Draw()
        leg = mklegend(x1=.22, y1=.66, x2=.79, y2=.82)
        legname = ratname.split('_')[-1].replace('eta','eta ')
        if 'Gen' in name: legname+=' (DY MC, 2016 geom)'
        leg.AddEntry(kappa,legname)
        leg.Draw()
        c1.Update()
        fnew.cd()
        kappa.Write(kappa.GetName())
        c1.Write('c_'+kappa.GetName())
    #kappa.Write()
        funcs['f1'+ratname].Write()

print 'just made', fnew.GetName()
fnew.Close()
exit(0)
