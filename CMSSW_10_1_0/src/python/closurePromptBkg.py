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
try: inputflist = glob(sys.argv[1])
except: inputflist = glob('output/smallchunks/PromptBkgHists_*.root')

try: fnameOut = sys.argv[2]
except: fnameOut = 'closure.root'
import os, sys

if not os.path.exists("output/closure_lumixsec"): 
	os.system('mkdir output/closure_lumixsec')
	needshadd = True
else: needshadd = False
import os
if not os.path.exists("output/closure_lumixsecOnsim"): os.system('mkdir output/closure_lumixsecOnsim')
if not os.path.exists("output/closure_finalcontribs"): os.system('mkdir output/closure_finalcontribs')


if needshadd:

	keysforxsec = []
	keysforcontrib = []
	print 'for inputname in inputflist:'
	for inputname in inputflist:
		shortname = inputname.split('Hists_')[-1].split('CUET')[0]
		print 'shortname', shortname
		if not shortname in keysforxsec: keysforxsec.append(shortname)
		else: continue	
		veryshortname = shortname.split('_')[0]
		print 'veryshortname', veryshortname
		if not veryshortname in keysforcontrib: keysforcontrib.append(veryshortname)
	print keysforxsec
#	exit(0)

	keysforxsec = sorted(keysforxsec)
	print keysforxsec
	for xkey in keysforxsec:
		import os
		if not os.path.exists("output/closure_lumixsec/"+xkey+'.root') or True:
			command = 'python python/ahadd.py -f output/closure_lumixsec/'+xkey+'.root output/smallchunks/Prompt*'+xkey+'*.root'
			print command
			
			if not istest: os.system(command)
	while len(glob('output/closure_lumixsec/*.root'))<len(keysforxsec):
		sleep(1.0)
	print 'escaped the sleep!'
	print 'hadded all chunks in respective HT ranges'
	print 'for xkey in keysforxsec:'
#	exit(0)
	for xkey in keysforxsec:
		                print 'xkey', xkey
				print 'going to scale to lumi file:', 'output/closure_lumixsec/'+xkey+'.root'
				if istest: break
				
				fOld = TFile('output/closure_lumixsec/'+xkey+'.root')
				hHt = fOld.Get('hHt')
				try: nentries = hHt.GetEntries()
				except:
					print 'stuck at ', xkey, fOld.GetName()
					exit(0)
				print 'number of entries here are', nentries
				keys = sorted(fOld.GetListOfKeys())
				fnew = TFile('output/closure_lumixsecOnsim/'+xkey+'.root','recreate')
				for key in keys:
					name = key.GetName()
					if 'c_' in name: continue
					if 'hHt'==name: continue
					h = fOld.Get(name)
					try:
						if nentries>0: h.Scale(lumi*1.0/nentries)
					except:
						fOld.ls()
						print 'that didnt work', xkey, name, h
						exit(0)
						
					fnew.cd()
					h.Write(name)
				fOld.Close()
				print 'finished scaling xkey'
				print 'just created', fnew.GetName()
				fnew.Close()
	print 'for contribname in keysforcontrib:'			
	for contribname in keysforcontrib:
		command = 'python python/ahadd.py -f output/closure_finalcontribs/'+contribname+'.root output/closure_lumixsecOnsim/*'+contribname+'*.root'
		print 'command', command
		if not istest: os.system(command)
		print 'just created', 'output/closure_finalcontribs/'+contribname+'.root'
	biglumpcommand = 'hadd -f output/totalweightedbkgs.root output/closure_finalcontribs/*.root'
	print 'biglumpcommand', biglumpcommand
	if not istest: os.system(biglumpcommand)
	print 'just created output/totalweightedbkgs.root : the complete BKG scales to lumi hadded'

#pause()
			
if needshadd: 
	print 'exiting on needshadd'
#	exit(0)	
if istest: fname = 'test.root'
else: fname = 'output/totalweightedbkgs.root'


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
	if CombineLeptons_: 
		if not ('Control' in name.split('_')[-1] and 'hEl'==name[:3]): continue
		lepname = '(el or #mu)'
	else: 
		if not ('Control' in name.split('_')[-1]): continue
		if 'hEl'==name[:3]: lepname = 'el'
		if 'hMu'==name[:3]: lepname = '#mu'
	if 'Ttbar' in name: continue
	print lepname, 'lepname'
	#pause()
	hVarControl = infile.Get(name)
	if CombineLeptons_: hVarControl.Add(infile.Get(name.replace('hEl','hMu')))
	hVarControl.SetTitle('single '+lepname)	
	truthname = name.replace('barControl','barBarf')
	truthname = truthname.replace('Control','Truth')
	truthname = truthname.replace('barBarf','barControl')
	hVarTruth = infile.Get(truthname)
	print truthname
	if CombineLeptons_: hVarTruth.Add(infile.Get(truthname.replace('hEl','hMu')))
	methodname = name.replace('barControl','barBarf')
	methodname = methodname.replace('Control','Method')
	methodname = methodname.replace('barBarf','barControl')
			
	hVarMethod = infile.Get(methodname)
	if CombineLeptons_: hVarMethod.Add(infile.Get(methodname.replace('hEl','hMu')))
	hVarMethod.SetTitle('Expected single '+lepname)
	hVarTruth.SetTitle('Truth single '+lepname)
	shortname = name[1:].replace('Control','').replace('Truth','').replace('Method','')
	varname = shortname.split('_')[-1]
	hVarControl.GetXaxis().SetTitle(namewizard(varname))
	hVarTruth.GetXaxis().SetTitle(namewizard(varname))
	hVarMethod.GetXaxis().SetTitle(namewizard(varname))
		
	hVarControl.Scale(1.0,'width') #lumi*1.0/hHt.Integral(-1,9999))
	hVarTruth.Scale(1.0,'width') #lumi*1.0/hHt.Integral(-1,9999))
	hVarMethod.Scale(1.0,'width') #lumi*1.0/hHt.Integral(-1,9999))

	
	leg = mklegend(x1=.48, y1=.65, x2=.95, y2=.87, color=kWhite)
	leg.SetTextSize(0.065)
	legname = 'single-lep'
	if 'hEl' in name: legname.replace('lep','electron')
	if 'hMu' in name: legname.replace('lep','muon')
#	leg.AddEntry(hVarControl,'single-lep','l')
	leg.AddEntry(hVarControl,'single '+lepname,'l')
	#hVarMethod.Scale()
	themax = 1000*max([hVarControl.GetMaximum(),hVarMethod.GetMaximum(),hVarTruth.GetMaximum()])
	hVarMethod.GetYaxis().SetRangeUser(0.00002,themax)
	hVarMethod.SetFillStyle(1001)
	hVarMethod.SetFillColor(hVarMethod.GetLineColor())	
	hVarTruth.GetYaxis().SetRangeUser(0.01,themax)
	hVarControl.GetYaxis().SetRangeUser(0.01,themax)
	hVarMethod.SetLineColor(kGray+2)
	if CombineLeptons_: shortname = shortname.replace('El','Lep').replace('Mu','Lep')
	c1 = mkcanvas('c_'+shortname.replace('_',''))
	hratio = FabDrawNew(c1,leg,hVarTruth,hVarMethod,datamc='MC',lumi=lumi, title = '', LinearScale=False, fractionthing='expected / truth')
	#hratio.GetYaxis().SetRangeUser(0.0,2.5)
	hratio.GetYaxis().SetRangeUser(0.09,99)	
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
	c1.Print('pdfs/closure/prompt-bkg/'+shortname.replace('_','')+'.png')
#	c1.Delete()
#	hratio.Delete()
	

print 'test a'
	
import os, sys
print 'test b'
print 'just created', os.getcwd()+'/'+fnew2.GetName()
fnew2.Close()
print 'test c'

	
	
