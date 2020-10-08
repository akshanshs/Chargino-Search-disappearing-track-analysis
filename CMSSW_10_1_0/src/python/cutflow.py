from ROOT import *
from utils import *
from histlib import *
import sys

try:fname =sys.argv[1]
except:
    fname = 'Sig56.root'
    print 'files not specified, will run on 4 default files:'
    print 'catau: 55 cm'

f  = TFile(fname)

keys = f.GetListOfKeys()

c1 = mkcanvas('c1')
histlist = []

for key in keys:
    c1.SetLogy()
    hist = key.GetName()
    print hist
    histlist.append(hist[1:])
    if ('cutflowL' in hist):hL     = f.Get(hist)
    if ('cutflowM' in hist):hM     = f.Get(hist)
    if ('cutflowS' in hist):hS     = f.Get(hist)
    print 'long', '**', 'medium','**', 'small'

    for x in range(0,15):
        print hL.GetBinContent(x), '**' , hM.GetBinContent(x), '**', hS.GetBinContent(x)


'''
    n = 1
    s1= n/(hL.Integral())
    hL.Scale(s1)
    s2= n/(hM.Integral())
    hM.Scale(s2)
    s3= n/(hS.Integral())
    hS.Scale(s3)

'''
