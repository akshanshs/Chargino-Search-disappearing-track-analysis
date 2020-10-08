from ROOT import *
from utils import *
from namelib import *
import sys

print 'Histogram factory starting........'
gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendTextSize(0.026)
try:fname =sys.argv[1]
except:
    fname = 'output55.root'
    print 'files not specified, will run on 4 default files:'
    print 'catau: 55 cm'
try:fname2 = sys.argv[2]
except:
    fname2 = 'output90.root'
    print 'catau: 90 cm'
try:fname3 = sys.argv[3]
except:
    fname3 = 'output10.root'
    print 'catau: 10 cm'
try:fname4 = sys.argv[4]
except:
    fname4 = 'output22.root'
    print 'catau: 22 cm'

f  = TFile(fname)
f2 = TFile(fname2)
f3 = TFile(fname3)
f4 = TFile(fname4)
keys = f.GetListOfKeys()

c1 = mkcanvas('c1')

namelist = []

for key in keys:
    name = key.GetName()
    print name
    if not ('Tag' in name):continue
    hpass    = f.Get(name)
    hAll    = f.Get(name.replace('Tag',''))

    histoStyler(hpass,kGreen+1)
    hpass.GetXaxis().SetTitle(namelib[name[1:].replace('Tag','')])

#    hpass.Divide(hAll)                                                                                                                    

    leg = TLegend(0.17,0.67,0.51,0.89)
    leg.SetHeader("Signal point (ctau,mass)")
    hpass.GetYaxis().SetTitle('efficiency #epsilon')
    hpass.GetYaxis().SetRangeUser(0,1.25)
    stamp(1)
    hpass2    = f2.Get(name)
    hAll2    = f2.Get(name.replace('Tag',''))
    hpass3    = f3.Get(name)
    hAll3    = f3.Get(name.replace('Tag',''))
    hpass4    = f4.Get(name)
    hAll4    = f4.Get(name.replace('Tag',''))

    eff2 =TEfficiency(hpass2,hAll2)
    eff3 =TEfficiency(hpass3,hAll3)
    eff4 =TEfficiency(hpass4,hAll4)

    eff3.SetLineWidth(1)
    eff3.SetLineStyle(2)
    eff3.SetMarkerStyle(20)
    eff3.SetMarkerColor(3)

    eff4.SetLineWidth(1)
    eff4.SetLineStyle(2)
    eff4.SetMarkerStyle(23)
    eff4.SetMarkerColor(4)
    eff =TEfficiency(hpass,hAll)
    eff.SetLineWidth(1)
    eff.SetLineStyle(2)
    eff.SetMarkerStyle(22)
    eff.SetMarkerColor(1)
    eff2.SetLineWidth(1)
    eff2.SetLineStyle(10)
    eff2.SetMarkerStyle(33)
    eff2.SetMarkerColor(2)

    leg.AddEntry(eff,"10 cm ,177 GeV ","lep")
    leg.AddEntry(eff2,"100 cm,177 GeV","lep")
    leg.AddEntry(eff3,"1000  cm,177 GeV","lep")
    leg.AddEntry(eff4,"56 cm,177 GeV","lep")
    hpass.SetTitle("Detecting disappearing tracks from gen information")
    hpass.Reset()
    hpass.Draw()
    eff.Draw('same')   #cool trick            
    eff2.Draw('same')
    eff3.Draw('same')
    eff4.Draw('same')
    leg.SetFillStyle(0)
    leg.Draw()
    c1.Update()

    pause()
    c1.Print('pdf/eff'+name+'.pdf')
