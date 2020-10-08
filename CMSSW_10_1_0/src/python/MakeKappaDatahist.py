from ROOT import *
from utilitiesII import *
from histlib import *
import sys


gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendTextSize(0.026)
#gROOT.SetBatch(1)


#fnames = ['KappaDY.root','KappaData.root']
#fnames = ['KappaNoZCut.root', 'Kappa.root']
#fnames = ['UsefulThings/Kappa.root']

try: fnames = [sys.argv[1]]
except: fnames = ['KappaDY.root']

print fnames[0], 'checking which file is accepted for DY'
pause()
isdata = True

f0 = TFile(fnames[0])
keys = f0.GetListOfKeys().Clone()
f0.ls()
f0.Close()
c1 = mkcanvas('c1')

#leg = TLegend(0.5,0.67,0.7,0.89)
#leg.SetTextFont(42)
#leg.SetTextSize(0.035)
fnew = TFile('DATAkappa.root','recreate')
hists = []
for key in keys:
  leg = TLegend(0.56,0.75,0.82,0.86)
#  tex = TText(.59,.7,'text')
#  leg = TLegend(0.5,0.67,0.7,0.89)
  leg.SetTextFont(42)
#  leg.SetTextSize(0.65)
  colors = [kAzure, kViolet,28, 1]
#  colors = [1,2,4, kTeal-5]
  icolor=0
  arg = ''
  histname = key.GetName()
  print 'A_histname', histname
  if 'c_' in histname: continue  #if 'ckappa' in histname: continue
  print 'B_histname', histname
  if 'f1h' in histname: continue
  if 'eta1.4442to1.566' in histname: continue
#  for fname in fnames:
  f = TFile(fnames[0])
  h     =  f.Get(histname).Clone(histname+fnames[0])
  h.SetDirectory(0)
  hists.append(h)
  overflow(h)
  leg.SetTextFont(42)
  leg.SetTextSize(0.055)
  TGaxis.SetMaxDigits(3)
  h.GetXaxis().SetTitle('P_{T}[GeV]')#histlib[histname[1:]])
  h.GetYaxis().SetTitleOffset(.95)
  if not isdata: h.GetYaxis().SetTitle('#kappa = n(DT)/n(reco-lep)')
  else: h.GetYaxis().SetTitle('#kappa = n(DT)/n(reco-lep)')

  if isdata:
    if 'ElProbePtKappa_eta0to1.4442' in histname: h.GetYaxis().SetRangeUser(0.00001,.0044)
    if 'MuProbePtKappa_eta0to1.4442' in histname: h.GetYaxis().SetRangeUser(0.00001,.00035)
    if 'ElProbePtKappa_eta1.566to2.4' in histname: h.GetYaxis().SetRangeUser(0.00001,.0057)
    if 'MuProbePtKappa_eta1.566to2.4' in histname: h.GetYaxis().SetRangeUser(0,.00056)
#    h.GetYaxis().SetRangeUser(0.00,1.2*(max(h.GetMaximum(),h2.GetMaximum())))
#    h.GetYaxis().SetTitle('#kappa')
    h.SetTitle("")
    if h.GetEntries()>0:
       histoStyler(h, colors[3])
       h.SetLineWidth(2)
       h.SetLineStyle(1)
       h.Draw(arg)
       c1.Update()
       print histname
       pause()
       arg = 'same'
       leg.AddEntry(h,"DATA: Run 2016","l")
  leg.SetFillStyle(0) 
  if 'ElProbePtKappa_eta0to1.4442' in histname: 
    tex = mktext(0.59,0.6,0.91,0.77, "blNDC")
    tex.AddText("e^{#pm} Barrel")
  if 'MuProbePtKappa_eta0to1.4442' in histname:
    tex = mktext(0.59,0.6,0.91,0.77, "blNDC")
    tex.AddText("#mu^{#pm} Barrel")
  if 'ElProbePtKappa_eta1.566to2.4' in histname:
    tex = mktext(0.59,0.6,0.91,0.77, "blNDC")
    tex.AddText("e^{#pm} End Cap")
  if 'MuProbePtKappa_eta1.566to2.4' in histname: 
    tex = mktext(0.59,0.6,0.91,0.77, "blNDC")
    tex.AddText("#mu^{#pm} End Cap")    
  stamp2fig()
  tex.Draw()
  leg.Draw()
  c1.Update()
  c1.Print('kappaPlots/'+histname.replace('hGen','').replace('Probe','')+'.png')
  print 'created ' , 'kappaPlots/DATA'+histname.replace('hGen','').replace('Probe','')+'.png'
  pause()
  fnew.cd()
  c1.Write(histname)

print 'just created', fnew.GetName()
fnew.Close()


