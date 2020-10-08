from ROOT import *
from utils import *
from histlib import *
from titlelib import *
import sys


gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendTextSize(0.026)

try:fname =sys.argv[1]
except:
    fname = 'Sample.root'
    print 'files not specified, will run on 4 default files:'
    print 'catau: 55 cm'

try:HISTI = sys.argv[2]
except:
    HISTI = 'htrkresp'
    print 'catau: 90 cm'

try:HISTII = sys.argv[3]
except:
    HISTII = 'hmuonresp'
    print 'catau: 90 cm'

#histolib = {}
#histolib['iso'] = 'relIso'


f  = TFile(fname)

keys = f.GetListOfKeys()
#f.ls()
#*=*=*=*=*=for makinghist from a flat tuple
#t1 = f1.Get('Analysis')

#t1.Show(0)

#for histkey in histolib:
#    t1.Draw(histolib[histkey])
#    t2.Draw(histolib[histkey],'same')
    
#    c1.Update()
#    pause()

c1 = mkcanvas('c1')
histlist = []

for key in keys:
    c1.SetLogy()
    hist = key.GetName()
    print hist
 #   if ('vs' in hist):continue 
    if not ('hInvMass' in hist):continue #hIMmuZsmear
    if not ('RECOeff' in hist):continue
   # hist = HISTI
   # hist2 = HISTII
    histlist.append(hist[1:])
    h     =  f.Get(hist)
    hist2 = hist.replace('RECOeff','DTeff')
    h2    =  f.Get(hist2)

    overflow(h)
    overflow(h2)
    
######Normlise Hists
    n = 1
    h_integral = (h.Integral())
    if not (h.Integral()) > 0:h_integral = 1
    s1= n/h_integral
    h.Scale(s1)
    h2_integral = (h2.Integral())
    if not (h2.Integral()) > 0:h2_integral = 1
    s2= n/h2_integral
    h2.Scale(s2)

    leg = TLegend(0.40,0.67,0.77,0.89)
#    leg = TLegend(0.66,0.67,0.87,0.89)
  #  leg.SetHeader("MC Sample")
    leg.SetHeader("MC:DYtoLNuLNu")
    leg.SetTextSize(0.035)
    histoStyler(h,2)
    h.SetLineWidth(3)
    h.SetLineStyle(1)
    h.GetXaxis().SetTitle('Invariant Mass(ee)')#histlib[hist[1:]])
    h.GetYaxis().SetRangeUser(0.0001,9*(max(h.GetMaximum(),h2.GetMaximum())))
    h.GetYaxis().SetTitle('Events norm to unity')
    h.SetTitle('')
#    h.SetTitle(titlelib[hist[1:]])
    h.Draw('hist e1')
    histoStyler(h2,4)
    h2.SetLineWidth(3)
    h2.SetLineStyle(1)

    leg.AddEntry(h,hist,"l")
    leg.AddEntry(h2,hist2,"l")

    h2.Draw('histsame e1')
    stamp(1)
    leg.SetFillStyle(0)
    leg.Draw()
    c1.Update()

    pause()
    c1.Print('compHist_pdf/'+hist+'HT.pdf')

print 'histlib= {}'
for hist in histlist:
    print 'histlib["' + hist + '"] = "' + hist +'"'
