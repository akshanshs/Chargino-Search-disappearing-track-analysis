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
except: fnames = ['Alpha.root']

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
fnew = TFile('DATAalpha.root','recreate')
hists = []
for key in keys:
  leg = TLegend(0.16,0.78,0.42,0.89)
#  tex = TText(.59,.7,'text')
#  leg = TLegend(0.5,0.67,0.7,0.89)
  leg.SetTextFont(42)
#  leg.SetTextSize(0.65)
  colors = [kAzure, kViolet,28, 1]
#  colors = [1,2,4, kTeal-5]
  icolor=0
  arg = ''
  histname = key.GetName()
  if 'c_' in histname: continue  #if 'ckappa' in histname: continue
  if 'f1' in histname: continue
#  for fname in fnames:
  f = TFile(fnames[0])
  h =  f.Get(histname).Clone(histname+fnames[0])
  h.SetDirectory(0)
  hists.append(h)
  overflow(h)
  leg.SetTextFont(42)
  leg.SetTextSize(0.055)
#  TGaxis.SetMaxDigits(2)
  h.GetXaxis().SetTitle('p_{T} GeV')#histlib[histname[1:]])
  if not isdata: h.GetYaxis().SetTitle('#alpha = n(SBSR)/n(SBCR)')
  else: h.GetYaxis().SetTitle('#alpha = n(SBSR)/n(SBCR)')
  h.GetYaxis().SetTitleOffset(1.7)


  if isdata:
    h.GetYaxis().SetTitleOffset(1.7)
    h.GetYaxis().SetRangeUser(0,0.6)
    h.SetTitle("")
    if h.GetEntries()>0:
       histoStyler(h, colors[3])
       h.SetLineWidth(2)
       h.SetLineStyle(1)
  leg.AddEntry(h,"DATA: Run 2016","l")
  leg.SetFillStyle(0) 
#  if 'MuProbePtKappa_eta1.566to2.4' in histname: 
#    tex = mktext(0.59,0.6,0.91,0.77, "blNDC")
#    tex.AddText("#mu^{#pm} End Cap")    
  h.Draw(arg)
  stamp2fig()
#  tex.Draw()
  leg.Draw()
  c1.Update()
  c1.Print('alphaPlots/'+histname.replace('Bkginclusive_','')+'.png')
  print 'created ' , 'alphaPlots/'+histname.replace('Bkginclusive_','')+'.png'
  pause()
  fnew.cd()
  c1.Write(histname)

print 'just created', fnew.GetName()
fnew.Close()


