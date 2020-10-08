from ROOT import *
import os, sys
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep
#from utils import *
from utilitiesII import *
#lumi =   22000 #35900.0
lumi = 35500
istest = False

########################
#usage: python/HaddWithScale.py 'haddDir/smallchunks/*Hists_*CUET*.root' 'OutPUT file name'
#
#
#######################

try: inputflist = glob(sys.argv[1])
except: inputflist = glob('haddeventHists/smallchunks/*Hists_*AODSIM*.root')

try: suffix = sys.argv[2]
except: suffix = 'Signal'

import os, sys

if not os.path.exists("haddeventHists/ScaledHadd_lumixsec"): 
	os.system('mkdir haddeventHists/ScaledHadd_lumixsec')
	needshadd = True
else: needshadd = False
import os
if not os.path.exists("haddeventHists/ScaledHadd_lumixsecOnsim"): os.system('mkdir haddeventHists/ScaledHadd_lumixsecOnsim')

if needshadd:

	keysforxsec = []
	print 'for inputname in inputflist:'
	for inputname in inputflist:
		shortname = inputname.split('SYSHists_')[-1].split('_27_200970')[0]
		print 'shortname', shortname
		if not shortname in keysforxsec: keysforxsec.append(shortname)
		else: continue	
		
	print keysforxsec
#	exit(0)
	print 'printed the keys for xSec above'
	keysforxsec = sorted(keysforxsec)
	print keysforxsec, 'keysforxsec'
	print 'printing again after sorting'
	pause()
	for xkey in keysforxsec:
		import os
		if not os.path.exists("haddeventHists/ScaledHadd_lumixsec/"+xkey+'.root') or True:
			command = 'python ../python/ahadd.py -f haddeventHists/ScaledHadd_lumixsec/'+xkey+'.root haddeventHists/smallchunks/*Signal*'+xkey+'*.root'
			print command
			#pause()
			if not istest: os.system(command)
	while len(glob('haddeventHists/ScaledHadd_lumixsec/*.root'))<len(keysforxsec):
		sleep(1.0)
	print 'escaped the sleep!'
	print 'hadded all chunks in respective Chargino lifetimes'
	print 'for xkey in keysforxsec:'
#	exit(0)
	for xkey in keysforxsec:
		                print 'xkey', xkey
				print 'going to scale to lumi file:', 'haddeventHists/ScaledHadd_lumixsec/'+xkey+'.root'
				#pause()
				if istest: break
				
				fOld = TFile('haddeventHists/ScaledHadd_lumixsec/'+xkey+'.root')
				hHt = fOld.Get('hHt')
				try: nentries = hHt.GetEntries()
				except:
					print 'stuck at ', xkey, fOld.GetName()
					exit(0)
				print 'number of entries here are', nentries
				keys = sorted(fOld.GetListOfKeys())  #Made the hists very organised, easy to look
				pause()
				fnew = TFile('haddeventHists/ScaledHadd_lumixsecOnsim/'+xkey+'Scaled'+suffix+'.root','recreate')
				print 'the file to which it will write is: ', fnew.GetName()
				pause()
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

	command = 'mv haddeventHists/ScaledHadd_lumixsecOnsim/*.root haddeventHists/'
	print command
	pause()
	os.system(command)

if needshadd: 
	print 'exiting on needshadd'
#	exit(0)	

print 'test a'
import os, sys
print 'test b'
print 'test c'

	
	
