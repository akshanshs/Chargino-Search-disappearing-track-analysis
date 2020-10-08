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
except: inputflist = glob('haddHistDir/smallchunks/*Hists_*CUET*.root')

try: fnameOut = sys.argv[2]
except: fnameOut = 'ScaledHaddTnPHists.root'
import os, sys

if not os.path.exists("haddHistDir/ScaledHadd_lumixsec"): 
	os.system('mkdir haddHistDir/ScaledHadd_lumixsec')
	needshadd = True
else: needshadd = False
import os
if not os.path.exists("haddHistDir/ScaledHadd_lumixsecOnsim"): os.system('mkdir haddHistDir/ScaledHadd_lumixsecOnsim')
if not os.path.exists("haddHistDir/ScaledHadd_finalcontribs"): os.system('mkdir haddHistDir/ScaledHadd_finalcontribs')

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
	pause()
#	exit(0)

	keysforxsec = sorted(keysforxsec)
	print keysforxsec
	print 'printed sorted keys'
	pause()
	for xkey in keysforxsec:
		import os
		if not os.path.exists("haddHistDir/ScaledHadd_lumixsec/"+xkey+'.root') or True:
			command = 'python ../python/ahadd.py -f haddHistDir/ScaledHadd_lumixsec/'+xkey+'.root haddHistDir/smallchunks/CB_TagnProbeHists*'+xkey+'*.root'
			print command
			
			if not istest: os.system(command)
	while len(glob('haddHistDir/ScaledHadd_lumixsec/*.root'))<len(keysforxsec):
		sleep(1.0)
	print 'escaped the sleep!'
	print 'hadded all chunks in respective HT ranges'
	print 'for xkey in keysforxsec:'
	pause()
#	exit(0)
	for xkey in keysforxsec:
		                print 'xkey', xkey
				print 'going to scale to lumi file:', 'haddHistDir/ScaledHadd_lumixsec/'+xkey+'.root'
				pause()
				if istest: break
				
				fOld = TFile('haddHistDir/ScaledHadd_lumixsec/'+xkey+'.root')
				hHt = fOld.Get('hHt')
				try:
					nentries = hHt.GetEntries()
					print 'number of entries here are', nentries
					pause()
				except:
					print 'stuck at ', xkey, fOld.GetName()
					exit(0)
				print 'number of entries here are', nentries
				pause()
				keys = sorted(fOld.GetListOfKeys())
				fnew = TFile('haddHistDir/ScaledHadd_lumixsecOnsim/'+xkey+'.root','recreate')
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
		command = 'python ../python/ahadd.py -f haddHistDir/ScaledHadd_finalcontribs/'+contribname+'.root haddHistDir/ScaledHadd_lumixsecOnsim/*'+contribname+'*.root'
		print 'command', command
		if not istest: os.system(command)
		print 'just created', 'haddHistDir/ScaledHadd_finalcontribs/'+contribname+'.root'
	biglumpcommand = 'hadd -f haddHistDir/'+fnameOut+' haddHistDir/ScaledHadd_finalcontribs/*.root'
	print 'biglumpcommand', biglumpcommand
	if not istest: os.system(biglumpcommand)
	print 'just created haddHistDir/'+fnameOut+' : the complete BKG scales to lumi hadded'

#pause()
			
if needshadd: 
	print 'exiting on needshadd'
#	exit(0)	
if istest: fname = 'test.root'
else: fname = 'haddHistDir/'+fnameOut


print 'test a'
import os, sys
print 'test b'
print 'test c'

	
	
