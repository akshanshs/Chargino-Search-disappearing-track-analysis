from ROOT import *
from utilsII import *
from histlib import *
import sys


gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendTextSize(0.026)

try:fname =sys.argv[1]
except:
    fname = 'Sig56.root'
    print 'files not specified, will run on 4 default files:'
    print 'catau: 55 cm'
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
#    c1.SetLogy()
    hist = key.GetName()
    print hist
    if not ('GenInfo' in hist):continue 
    histlist.append(hist[1:])
    h     =  f.Get(hist)
    h2    =  f.Get(hist.replace('GenInfo','tagNprobe'))

    overflow(h)
    overflow(h2)
#    h2.Scale(0.5)
######Normlise Hists
    n = 1
#    s1= n/(h.Integral())
#    h.Scale(s1)
#    s2= n/(h2.Integral())
#    h2.Scale(s2)
   # leg = mklegend()
    leg = TLegend(0.56,0.67,0.77,0.89)
    leg.SetTextFont(42)
    leg.SetTextSize(0.035)
    leg.SetHeader("#kappa from MC:DYtoLNuLNu")
    histoStyler(h,2)
    h.SetLineWidth(2)
    h.SetLineStyle(1)
    h.GetXaxis().SetTitle(histlib[hist[1:]])
    h.GetYaxis().SetRangeUser(0.0001,1.2*(max(h.GetMaximum(),h2.GetMaximum())))
    h.GetYaxis().SetTitle('#kappa')
    stamp(35.9)
    if ('L' in hist): title = "Kappa factor for long tracks"
    if ('M' in hist): title = "Kappa factor for medium tracks"
    if ('S' in hist): title = "Kappa factor for small tracks"
#    h.SetTitle(title)
    h.SetTitle("")
    h.Draw('hist e1')
    histoStyler(h2,4)
    h2.SetLineWidth(2)
    h2.SetLineStyle(1)

    leg.AddEntry(h,"Gen Info ","l")
    leg.AddEntry(h2,"Tag and Probe","l")

    h2.Draw('histsame e1')
#    stamp(35.9)
#    stampE(13)
    leg.SetFillStyle(0)
    leg.Draw()
    stamp(35.9)
    stampE(13)
    c1.Update()
#    stamp(35.9)
    pause()
    c1.Print('compHist_pdf/'+hist+'HT.pdf')

print 'histlib= {}'
for hist in histlist:
    print 'histlib["' + hist + '"] = "' + hist +'"'
