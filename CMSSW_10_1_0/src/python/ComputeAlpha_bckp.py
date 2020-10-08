from ROOT import *
from utils import *
from namelib import *
import sys
from random import shuffle
gROOT.SetBatch(1)

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

isdata = True
splitFit = False

funcs = {}

keys = file.GetListOfKeys()

c1 = mkcanvas('c1')
fnew = TFile(foname,'recreate')
fnew.cd()

for key in keys:
    name = key.GetName()
    if not (('MBSRnum' in name or 'SBSRnum' in name) and '_0' in name and 'inclusive' in name): continue
    print 'histo name', name
    pause()

    hnum   = file.Get(name)
#    if 'Gen' in name: hnum.SetLineColor(kAzure)
#    else: hnum.SetLineColor(kViolet)
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
#    hratio.Draw()
    hratio.SetLineColor(hratio.GetLineColor())
    hratio.Draw()
    leg = mklegend(x1=.22, y1=.66, x2=.79, y2=.82)
    legname = ratname.split('_')[-1].replace('eta','eta ')
#    if 'Gen' in name: legname+=' (DY MC, 2016 geom)'                                                                                        
    leg.AddEntry(hratio,legname)
    leg.Draw()
    c1.Update()
    fnew.cd()
    hratio.Write(hratio.GetName())
    c1.Write('c_'+hratio.GetName())
    #hratio.Write()                                                                                                                          
#    funcs['f1'+ratname].Write()                                                                                                             

print 'just made', fnew.GetName()
fnew.Close()
exit(0)



'''
    if not splitFit: funcs['f1'+ratname] = TF1('f1'+ratname,'[0]*TMath::Landau(x,[1],[2])',20,760)
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
    funcs['f1'+ratname].SetLineColor(hratio.GetLineColor())
    
    if not splitFit: hratio.Fit('f1'+ratname,'','SN',20,760) # replace 1000 by 2500 for PtBinEdges
    else:
        if '2.4' in name:   hratio.Fit('f1'+ratname,'','SN',20,300) # replace 1000 by 2500 for PtBinEdges
        else: hratio.Fit('f1'+ratname,'','SN',20,600)
'''
'''
    hratio.SetLineColor(hratio.GetLineColor())
    hratio.Draw()
    leg = mklegend(x1=.22, y1=.66, x2=.79, y2=.82)
    legname = ratname.split('_')[-1].replace('eta','eta ')
#    if 'Gen' in name: legname+=' (DY MC, 2016 geom)'
    leg.AddEntry(hratio,legname)
    leg.Draw()
    c1.Update()
    fnew.cd()
    hratio.Write(hratio.GetName())
    c1.Write('c_'+hratio.GetName())
    #hratio.Write()
#    funcs['f1'+ratname].Write()

print 'just made', fnew.GetName()
fnew.Close()
exit(0)
'''
