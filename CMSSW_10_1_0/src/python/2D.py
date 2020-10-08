from ROOT import *
from utilities import *
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

f  = TFile(fname)

keys = f.GetListOfKeys()

c1 = mkcanvas2D('c1')

namelist = []

###########Olny for 2D Hists

c1.SetLogz()
for key in keys:
    name = key.GetName()
    if 'c_' in name: continue
    h    = f.Get(name)
    histoStyler(h,kGreen+1)
    TGaxis.SetMaxDigits(1)
    h.GetYaxis().SetTitleOffset(.8)
    h.GetYaxis().SetTitleSize(.055)
    h.GetXaxis().SetTitleOffset(.8)
#    h.GetZaxis().SetNoExponent(kTRUE)
    h.GetXaxis().SetTitleSize(.055)
    h.GetXaxis().SetTitle("#phi")
    h.GetYaxis().SetTitle("#eta")
    if not ('maskD' in name or 'maskM' in name) : h.GetZaxis().SetTitle("Normalized/Bin area")
    else: h.GetZaxis().SetTitle('')
    
    print name
    h.Draw('colz')
#    stamp()
    c1.Update()
    
    pause()
    c1.Print('pdf/'+name+'.png')
############



