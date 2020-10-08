from ROOT import *
import os, sys
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep
#from utils import *
from utilitiesII import *
lumi = 35900.0
istest = False

CombineLeptons_ = True

try: inputflist = sys.argv[1]
except: inputflist = 'fakeoutput/smallchunks/FakeBkgPredictionHists_*.root'

try: fnameOut = sys.argv[2]
except: fnameOut = 'FakeBkgPrediction.root'
import os, sys

command = 'python python/ahadd.py -f fakeoutput/totalFakePredictionbkgs.root '+inputflist
print 'command', command
fname = 'fakeoutput/totalFakePredictionbkgs.root'
print 'fname:', fname
pause()
os.system(command)

infile = TFile(fname)
infile.ls()

fnew2 = TFile(fnameOut,'recreate')

keys = infile.GetListOfKeys()

print 'len(keys)', len(keys)

print keys
pause()
for key in keys:#[:241]:
#	infile.cd()
	name = key.GetName()
	print name
	
	if not ('Control' in name.split('_')[-1]): continue
	print name.split('_')[-1]
	print name[:5]
	pause()
	if 'hFake'==name[:5]: lepname = 'fake'
#	if 'Ttbar' in name: continue
	print lepname, 'lepname'
	#pause()
	hVarControl = infile.Get(name)
	hVarControl.SetTitle('CR '+lepname)	
	truthname = name.replace('barControl','barBarf')
	truthname = truthname.replace('Control','Truth')
	truthname = truthname.replace('barBarf','barControl')
	hVarTruth = infile.Get(truthname)
	print truthname
	methodname = name.replace('barControl','barBarf')
	methodname = methodname.replace('Control','Method')
	methodname = methodname.replace('barBarf','barControl')
			
	hVarMethod = infile.Get(methodname)
	hVarMethod.SetTitle('Predicted SR '+lepname)
	hVarTruth.SetTitle('DATA SR '+lepname)
	shortname = name[1:].replace('Control','').replace('Truth','').replace('Method','')
	varname = shortname.split('_')[-1]
	hVarControl.GetXaxis().SetTitle(namewizard(varname))
	hVarTruth.GetXaxis().SetTitle(namewizard(varname))
	hVarMethod.GetXaxis().SetTitle(namewizard(varname))
		
	hVarControl.Scale(1.0,'width') #lumi*1.0/hHt.Integral(-1,9999))
	hVarTruth.Scale(1.0,'width') #lumi*1.0/hHt.Integral(-1,9999))
	hVarMethod.Scale(1.0,'width') #lumi*1.0/hHt.Integral(-1,9999))

	
	leg = mklegend(x1=.5, y1=.65, x2=.97, y2=.87, color=kWhite)
	leg.SetTextSize(0.07)
	legname = 'fake'
	if 'hFake' in name: legname.replace('lep','electron')
#	leg.AddEntry(hVarControl,'single-lep','l')
	leg.AddEntry(hVarControl,'single '+lepname,'l')
	#hVarMethod.Scale()
	themax = 1000*max([hVarControl.GetMaximum(),hVarMethod.GetMaximum(),hVarTruth.GetMaximum()])
	hVarMethod.GetYaxis().SetRangeUser(0.00001,themax)
	hVarMethod.SetFillStyle(1001)
	hVarMethod.SetFillColor(hVarMethod.GetLineColor())	
	hVarTruth.GetYaxis().SetRangeUser(0.01,themax)
	hVarControl.GetYaxis().SetRangeUser(0.01,themax)
	hVarMethod.SetLineColor(kGray+2)
	c1 = mkcanvas('c_'+shortname.replace('_',''))
	hratio = FabDrawNew(c1,leg,hVarTruth,hVarMethod,datamc='MC',lumi=lumi, title = '', LinearScale=False, fractionthing='expected / truth')
	#hratio.GetYaxis().SetRangeUser(0.0,2.5)
	hratio.GetYaxis().SetRangeUser(0.09,100)	
	hratio.SetLineColor(kBlack)
	hratio.SetMarkerColor(kBlack)
	c1.cd(2)
	c1.SetLogy()
	c1.Update()
	c1.cd(1)
	hVarControl.Draw('same p')
	c1.Update()
	fnew2.cd()
	c1.Write()
	c1.Print('pdfs/prediction/fake-bkg/'+shortname.replace('_','')+'.pdf')
	c1.Delete()
	hratio.Delete()
	

print 'test a'
	
import os, sys
print 'test b'
print 'just created', os.getcwd()+'/'+fnew2.GetName()
fnew2.Close()
print 'test c'

	
	
