from ROOT import *
from utils import *
from namelib import *
import sys

gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendTextSize(0.026)
try:fname =sys.argv[1]
except:
    fname = 'TagProbeTrees/TagnProbe_DYJetsToLL_M-50_100HT.root'
    print 'files not specified, will run on 4 default files:'
    print 'catau: 55 cm'

f  = TFile(fname)
keys = f.GetListOfKeys()

c1 = mkcanvas('c1')

for key in keys:
    name = key.GetName()

    if not ('Gen' in name):continue
    hnum   = f.Get(name)
    hden    = f.Get(name.replace('Gen','Probe'))
    hden.GetXaxis().SetTitle(name.replace('DTeff','').replace('RECOeff','').replace('MuProbe','').replace('h',''))
    leg2 = TLegend(0.17,0.67,0.51,0.89)
    leg2.SetHeader("MC sample")
    hden.GetYaxis().SetTitle('#frac{DT}{reco}')
    hden.GetYaxis().SetRangeUser(0,3.0)
    stamp(1)
    print "hnum", hnum.GetBinContent(2)

    hnum.Divide(hden)
    print "hnum", hnum.GetBinContent(2)
    print 10*'*'
    leg2.AddEntry(hden," DYtoLL  ","lep")

    hden.SetTitle('ratio #frac{gen}{DY}')
#    hden.SetTitle(namelib[name[1:]])
    hden.Reset()
    hden.Draw()

    hnum.Draw('same')   #cool trick  
    leg2.SetFillStyle(0)
#    leg2.Draw()
    c1.Update()

    pause()
    c1.Print('pdfef/ratio'+name+'.pdf')
    hnum.Write('hist_'+name)
    print 'root file updated with histo'
