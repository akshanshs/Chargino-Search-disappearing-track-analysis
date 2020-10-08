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
except: fnames = ['Kappa.root']

print fnames[0], 'checking which file is accepted'
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
fnew = TFile('kappaClosure.root','recreate')
hists = []
for key in keys:
  leg = TLegend(0.59,0.71,0.91,0.88)
#  tex = TText(.59,.7,'text')
#  leg = TLegend(0.5,0.67,0.7,0.89)
  leg.SetTextFont(42)
#  leg.SetTextSize(0.65)
  colors = [kAzure, kViolet, 1]
#  colors = [1,2,4, kTeal-5]
  icolor=0
  arg = ''
  histname = key.GetName()
  print 'ahistname', histname
  if 'c_' in histname: continue  #if 'ckappa' in histname: continue
  print 'bhistname', histname
  if not 'Gen' in histname:continue #if not 'GenInfo' in histname:continue
  if 'f1h' in histname: continue
  print 'doing key', key.GetName()
  for fname in fnames:
    f = TFile(fname)
    h     =  f.Get(histname).Clone(histname+fname)
    h2    =  f.Get(histname.replace('Gen','')).Clone(histname.replace('Gen','')+fname)
    h.SetDirectory(0)
    h2.SetDirectory(0)
    hists.append(h)
    hists.append(h2)
    overflow(h)
    overflow(h2)
    leg.SetTextFont(42)
    leg.SetTextSize(0.055)
    TGaxis.SetMaxDigits(3)
    h.GetXaxis().SetTitle('P_{T}')#histlib[histname[1:]])
    h.GetYaxis().SetTitleOffset(.6)
    if not isdata: h.GetYaxis().SetTitle('#kappa')
    else: h2.GetYaxis().SetTitle('#kappa')

    if isdata:
      if 'ElProbePtKappa_eta0to1.4442' in histname: h2.GetYaxis().SetRangeUser(0.00,.04)
      if 'MuProbePtKappa_eta0to1.4442' in histname: h2.GetYaxis().SetRangeUser(0.00,.012)
      if 'ElProbePtKappa_eta1.566to2.4' in histname: h2.GetYaxis().SetRangeUser(0.00,.009)
      if 'MuProbePtKappa_eta1.566to2.4' in histname: h2.GetYaxis().SetRangeUser(0.00,.004)
    else:
      if 'ElProbePtKappa_eta0to1.4442' in histname: h.GetYaxis().SetRangeUser(0.00,.0012)
      if 'MuProbePtKappa_eta0to1.4442' in histname: h.GetYaxis().SetRangeUser(0.00,.0003)
      if 'ElProbePtKappa_eta1.566to2.4' in histname: h.GetYaxis().SetRangeUser(0.00,.0035)
      if 'MuProbePtKappa_eta1.566to2.4' in histname: h.GetYaxis().SetRangeUser(0.00,.00002)
#    h.GetYaxis().SetRangeUser(0.00,1.2*(max(h.GetMaximum(),h2.GetMaximum())))
#    h.GetYaxis().SetTitle('#kappa')
    h.SetTitle("")
    histoStyler(h2,4)
    h2.SetLineWidth(2)
    h2.SetLineStyle(1)
    if h.GetEntries()>0:
       histoStyler(h, colors[icolor])
       h.SetLineWidth(3)
       h.SetLineStyle(1)
       icolor+=1
       h.Draw(arg)
       c1.Update()
       
       print histname
       pause()
       
       arg = 'same'
       leg.AddEntry(h,"Gen Info ","l")
       print 'here in 1', fname
    if h2.GetEntries()>0:
       histoStyler(h2,colors[icolor])
       icolor+=1
       h2.SetLineWidth(3)
       h2.SetLineStyle(1)
       if not isdata:
         leg.AddEntry(h2,"Tag and Probe ","l")  # 'Data','data (2016C)' 
       else: leg.AddEntry(h2,"Data:Run 2016","l")  # 'Data','data (2016C)'
       h2.Draw(arg)
       arg = 'same'
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
  stamp()
  tex.Draw()
  leg.Draw()
  c1.Update()
  c1.Print('kappaPlots/'+histname.replace('hGen','').replace('Probe','')+'.png')
  print 'created ' , 'kappaPlots/'+histname.replace('hGen','').replace('Probe','')+'.png'
  pause()
  fnew.cd()
  c1.Write(histname)

print 'just created', fnew.GetName()
fnew.Close()


