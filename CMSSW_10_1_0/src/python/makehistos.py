from ROOT import *
from utils import *
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
try:fname2 = sys.argv[2]
except:
    fname2 = 'Sig100.root'
    print 'catau: 90 cm'
try:fname3 = sys.argv[3]
except:
    fname3 = 'WJets.root'
    print 'catau: 10 cm'
try:fname4 = sys.argv[4]
except:
    fname4 = 'TTbar.root'
    print 'catau: 22 cm'
#try:fname5 = sys.argv[5]
#except:
#    fname5 = 'DY.root'
#    print 'background: WJets2LNu'

#histolib = {}
#histolib['iso'] = 'relIso'


f  = TFile(fname)
f2 = TFile(fname2)
f3 = TFile(fname3)
f4 = TFile(fname4)
#f5 = TFile(fname5)
keys = f.GetListOfKeys()
#f.ls()
#*=*=*=*=*=for makinghist from a flat tuple
#t1 = f1.Get('Analysis')
#t2 = f2.Get('Analysis')
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
#    if ('Vdisp' in hist):continue 
    histlist.append(hist[1:])
    if ('Vdisp' in hist):continue
    h     = f.Get(hist)
    h2    = f2.Get(hist)
    h3    = f3.Get(hist)
    h4    = f4.Get(hist)
#    h5    = f5.Get(hist)
    overflow(h)
    overflow(h2)
    overflow(h3)
    overflow(h4)
#    overflow(h5)
    
######Normlise Hists
    n = 1
    s1= n/(h.Integral())
    h.Scale(s1)
    s2= n/(h2.Integral())
    h2.Scale(s2)
    s3= n/(h3.Integral())
    h3.Scale(s3)
    s4= n/(h4.Integral())
    h4.Scale(s4)
#    s5= n/(h5.Integral())
#    h5.Scale(s5)    

    leg = TLegend(0.66,0.67,0.87,0.89)
    leg.SetHeader("Signal point (ctau,mass)")
    histoStyler(h,1)
    h.SetLineWidth(2)
    h.SetLineStyle(2)
    h.GetXaxis().SetTitle(histlib[hist[1:]])
    h.GetYaxis().SetRangeUser(0.0001,5*max(h4.GetMaximum(),(max(h.GetMaximum(),h2.GetMaximum()))))
    h.GetYaxis().SetTitle('Events norm to unity')
    h.Draw('hist')
    histoStyler(h2,2)
    histoStyler(h3,3)
    histoStyler(h4,4)
#    histoStyler(h5,24)
    h2.SetLineWidth(2)
    h2.SetLineStyle(2)
    h3.SetLineWidth(1)
    h3.SetLineStyle(1)
    h4.SetLineWidth(1)
    h4.SetLineStyle(1)
#    h5.SetLineWidth(1)
#    h5.SetLineStyle(1)    
    leg.AddEntry(h,"56 cm ,177 GeV ","l")
    leg.AddEntry(h2,"10 cm,177 GeV","l")
    leg.AddEntry(h3,"100 cm, 177 GeV","l")
    leg.AddEntry(h4,"1000 cm, 177 GeV""l")
#    leg.AddEntry(h5,"DrellYan","l")
    h2.Draw('histsame')
    h3.Draw('histsame')
    h4.Draw('histsame')
#    h5.Draw('histsame')
    leg.SetFillStyle(0)
    leg.Draw()
    c1.Update()

    pause()
    c1.Print('Eselectpdf/'+hist+'.pdf')

print 'histlib= {}'
for hist in histlist:
    print 'histlib["' + hist + '"] = "' + hist +'"'
