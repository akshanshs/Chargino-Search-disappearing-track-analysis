import sys
import time
import numpy as np
from ROOT import *
from utilitiesII import *
from glob import glob
from random import shuffle
import random
import math
BTAG_CSV = 0.8484
check = 0
Pt_threshold = 30

gROOT.SetBatch()
gROOT.SetStyle('Plain')

try: inputFileNames = sys.argv[1]
#except: inputFileNames = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_88_RA2AnalysisTree.root"
except: inputFileNames = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2_285_RA2AnalysisTree.root"
#/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_267_RA2AnalysisTree.root 
inputFiles = glob(inputFileNames)
x = len(inputFiles)

c = TChain("TreeMaker2/PreSelection")
datamc = 'mc'
mZ = 91
genMatchEverything = False
ClosureMode = True #false means run as if real data
verbose = False

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
identifier+='nFiles'+str(len(inputFiles))
print 'Identifier', identifier

newfname = 'FakeBkgHists_'+identifier+'.root'

if genMatchEverything: newfname = newfname.replace('.root','Truth.root')
fnew_ = TFile(newfname,'recreate')
print 'Will write results to', newfname

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)

inf = 999999

varlist_ = ['Ht','Met','R','NTags','dPhi','NJets','CRdisptrack', 'TrkPt','TrkEta','BinNumber','nVtx']
 
regionCuts = {}

#regionVars:                       [HT   ,         MHT,       R,      Ntag,    dPhi,    Njets,   MBCRtrk,  TrkPt,   TrkEta, BinNumber, nVtx ]
regionCuts['NoCuts']             = [(0,inf),   (0.0,inf), (-1.0,2), (0,inf), (-1,3.2), (0,inf), (0,inf),  (0,inf), (0,2.4), (-1,inf), (0,inf)]
regionCuts['LoweredMhtBaseline'] = [(250,inf), (150,inf), (-1.0,2), (0,inf), (-1,3.2), (0,inf), (0,0  ), (0,inf  ), (0,2.4), (0,inf), (-1,inf)]
regionCuts['Baseline']           = [(250,inf), (150,inf), (-1.0,2), (0,inf), (-1,3.2), (1,inf), (0,0  ), (0,inf  ), (0,2.4), (0,inf), (-1,inf)]
regionCuts['SignalRegion']       = [(250,inf), (200,inf), (-1.0,2), (0,inf), (-1,2.5), (1,inf), (0,0  ), (0,inf  ), (0,2.4), (0,inf), (-1,inf)]
regionCuts['SignalRegion1jet']   = [(250,inf), (250,inf), (-1.0,2), (0,inf), (-1,2.5), (1,inf), (0,0  ), (0,inf  ), (0,2.4), (0,inf), (-1,inf)]
regionCuts['SignalRegion2jet']   = [(250,inf), (250,inf), (-1.0,2), (0,inf), (-1,2.5), (2,inf), (0,0  ), (0,inf  ), (0,2.4), (0,inf), (-1,inf)]
regionCuts['ClosureRegion']      = [(200,inf), (200,inf), (-1.0,2), (0,inf), (-1,2.5), (1,inf), (0,0  ), (0,inf  ), (0,2.4), (0,inf), (-1,inf)]

indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
for region in regionCuts:
    for var in varlist_:
        histname = 'Fake'+region+'_'+var
        histoStructDict[histname] = mkHistoStruct(histname)
                
binnumbers = {}

#BIN:          HT        MHT       R
 
binnumbers[((250,550),(150,350),(-1,1))] = 1
binnumbers[((550,inf),(150,350),(-1,1))] = 2
binnumbers[((250,550),(350,inf),(-1,1))] = 3
binnumbers[((550,inf),(350,inf),(-1,1))] = 4
binnumbers[((250,550),(150,350),( 1,2))] = 5
binnumbers[((550,inf),(150,350),( 1,2))] = 6
binnumbers[((250,550),(350,inf),( 1,2))] = 7
binnumbers[((550,inf),(350,inf),( 1,2))] = 8

def getBinNumber(fv):
	for binkey in binnumbers:
		foundbin = True
		for iwindow, window in enumerate(binkey):
			if not (fv[iwindow]>window[0] and fv[iwindow]<=window[1]): foundbin = False
		if foundbin: return binnumbers[binkey]        #returns the bin number
	return -1

for f in inputFiles:
	print 'adding file:', f
	c.Add(f)
	break
nentries = c.GetEntries()
#nentries = 100

c.Show(0)
#nentries = 5

def selectionFeatureVector(fvector, regionkey='', omitcuts=''):
    iomits = []
    for cut in omitcuts.split('Vs'): iomits.append(indexVar[cut])
    for i, feature in enumerate(fvector):
        if i in iomits: continue
        if not (feature>=regionCuts[regionkey][i][0] and feature<=regionCuts[regionkey][i][1]):
            return False
    return True


if 'TTJets_TuneCUET' in inputFileNames:  madranges = [(0,600),(800,1200)]
elif 'TTJets_HT' in inputFileNames: madranges = [(600,inf)]
elif 'WJetsToLNu_TuneCUET' in inputFileNames: madranges = [(0, 100), (600,800)]
elif 'WJetsToLNu_HT' in inputFileNames: madranges = [(100, inf)]
elif 'DYJetsToLL_M-50_TuneCUETP8M1' in inputFileNames: madranges = [(0, 100)]
else: madranges = [(0, inf)]

fMask = TFile('/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/usefulfiles/Masks.root')
if not ClosureMode : hMask = fMask.Get('hEtaVsPhiDT_maskRun2016')
else: hMask = ''
        #hMask = fMask.Get('hEtaVsPhiDT_maskRun2016')   

if ClosureMode: fileKappa = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/SB_AlphaRun20nodPhi0p5Pt30Mu3oTAPpionsVeto.root'#MB_Alpha_SelfCalcVar.root'
#'/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/Kappa_DY_Weighted5Feb.root'# replace with Alpha 
else: fileKappa = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/MB_Alpha_SelfCalcVar.root' 
#'/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/Kappa_DATA_dmVariable.root'

fKappa = TFile(fileKappa)     #replace with fAlpha

alphahist = fKappa.Get('Bkginclusive_nVtx_Alpha_0')

bin= alphahist.GetXaxis().FindBin(45)
print 'bin is', bin

print 'alpha test', alphahist.GetBinContent(4)
def fetchKappa(nVtx = 2):   # replace with simple fetching alpha function
    if nVtx < 5 : return 0.03
    if nVtx > 39 : return 0.75
#    nVtx_val1 = nVtx//4
#    nVtx_val2 = nVtx_val1 + 1
#    v1 = alphahist.GetBinContent(nVtx_val1)
#    v2 = alphahist.GetBinContent(nVtx_val2)
    bin= alphahist.GetXaxis().FindBin(nVtx)
    bin = bin - 1
    v = alphahist.GetBinContent(bin)
#    v = (v1+v2)/2
    return v

#def fetchKappa(nVtx = 2):
#    bin = alphahist.GetXaxis().FindBin()

def TriggerResult(trigger):
    for i, index in enumerate(trigger):
        if c.TriggerPass[index] ==1: return True
    return False

def getGenID(track):
    drsmall = 0.2
    gen_id = 0
    for igen, gen in enumerate(c.GenParticles):
        if not ((c.GenParticles_Status[igen] == 1) or (abs(c.GenParticles_PdgId[igen]) == 15)) : continue
        if gen.Pt() < 15:continue
        dr = gen.DeltaR(track)
        if dr < drsmall:
            drsmall = dr
            gen_id  = abs(c.GenParticles_PdgId[igen])
    if drsmall < 0.01: return gen_id
    else : return 0

def leptonVeto():

    flag = True
    nleptons = 0
    for imu, mu in enumerate(c.Muons):
        if abs(mu.Eta()) > 2.4: continue
        if (abs(mu.Eta()) > 1.445 and abs(mu.Eta()) < 1.56): continue
        if not mu.Pt() > 30:continue
        if not c.Muons_passIso[imu]: continue
        nleptons = nleptons + 1
    for iele, electron in enumerate(c.Electrons):
        if abs(electron.Eta()) > 2.4:continue
        if (abs(electron.Eta()) > 1.445 and abs(electron.Eta()) < 1.56): continue
        if not electron.Pt() > 30:continue
        if not c.Electrons_passIso[iele]: continue
        if not c.Electrons_mediumID[iele]: continue
        nleptons = nleptons + 1
    if nleptons > 0 : flag = False
    return flag

	
import time
t1 = time.time()
i0=0
verbosity = 10000
print nentries, 'evets to be analyzed'
for ientry in range(nentries):
	if verbose:
		if not ientry in [670]: continue
	if ientry%verbosity==0:
		print 'now processing event number', ientry, 'of', nentries
		
	if verbose: print 'getting entry', ientry
	c.GetEntry(ientry) 
	hHt.Fill(c.HT)
	weight = c.CrossSection
	hHtWeighted.Fill(c.HT,weight)
	
        nVtx = c.nAllVertices
	isValidHtRange = False
#        isValidHtRange = True     # removing madHT requiremnt for # to has to be updated

	for madrange in madranges:
		if (c.madHT>madrange[0] and c.madHT<madrange[1]):
			isValidHtRange = True
			break 
	if not isValidHtRange: continue

        if not passesUniversalSelection(c): continue
        if leptonVeto() == False: continue
#        if not passesLepveto(c): continue   # lep veto put seperately in utils , taken out from universal selection

	basicTracks = []
	MBCRdisappearingTracks = []	
        MBSRdisappearingTracks = []
	for itrack, track in enumerate(c.tracks):
                #if verbose: print "enter the track loop"
		if not track.Pt() > 20 : continue
		if not abs(track.Eta()) < 2.4: continue
		if not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
		if not isNminusOneBaselineTrack(track, itrack, c, hMask): continue
		basicTracks.append([track,c.tracks_charge[itrack], itrack]) # actually N-1 basic track as dxy req removed
		if not (track.Pt() > Pt_threshold and track.Pt()<9999): continue		
		if not isDisappearingTrack_(track, itrack, c): continue  # in principle it is N minus one disappearing track 
		drlep = 99
		passeslep = True # passeslep = does not match any lepton
		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)+list(c.TAPPionTracks)): 
			drlep = min(drlep, lep.DeltaR(track))
			if drlep<0.01: 
				passeslep = False
				break			
		if not passeslep: continue		
                if abs(c.tracks_dxyVtx[itrack]) < 0.01: MBSRdisappearingTracks.append(track)
                if ((abs(c.tracks_dxyVtx[itrack]) > 0.02) and (abs(c.tracks_dxyVtx[itrack]) < 0.1)) : MBCRdisappearingTracks.append(track)
    
	MBCRevent = len(MBCRdisappearingTracks) ==1 #>=1	
	MBSRevent = len(MBSRdisappearingTracks) >=1 #
#	if (MBSRevent and MBCRevent): continue # if a vent has a track in CR and a track in SR...then WHAT
	if not (MBSRevent or MBCRevent): continue
	
	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region

	if MBCRevent:
		track = random.sample(MBCRdisappearingTracks,1)[0]
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
                adjustedMet = metvec
		adjustedJets = []
		adjustedHt = 0
		adjustedBTags = 0
		if genMatchEverything:
                    getID = getGenID(track)
                    if not getID == 0 : continue
		#print ientry, 'found a tawdry se', elec.Pt()			
		for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue
			if not jet.DeltaR(track)>0.4: continue####update 
			if not abs(jet.Eta())<5.0: continue####update to 2.4
			adjustedMht-=jet
			if not abs(jet.Eta())<2.4: continue####update to 2.4
			adjustedJets.append(jet)			
			adjustedHt+=jet.Pt()
			if c.Jets_bDiscriminatorCSV[ijet]>BTAG_CSV: adjustedBTags+=1
		adjustedNJets = len(adjustedJets)
		mindphi = 4
		for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))
		
                pt = track.Pt()
                eta = abs(track.Eta())	
                phi = abs(track.Phi())
#                R = 2*(abs(pt - adjustedMht.Pt())/(pt + adjustedMht.Pt()))
                R = 2*(abs(pt - adjustedMet.Pt())/(pt + adjustedMet.Pt()))
                dPhi =  math.acos(math.cos((adjustedMet.Phi()-phi)))
                fv = [adjustedHt,adjustedMht.Pt(),R,1+len(MBSRdisappearingTracks),dPhi,adjustedNJets, len(MBCRdisappearingTracks)-1, pt,eta]
		fv.append(getBinNumber(fv))
                fv.append(nVtx)
                k = fetchKappa(nVtx)
#		k = fetchKappa(nVtx) # replace fetchKappa with alpha and if binned alpha pas nvtx
                print 'alpha for # vertices',nVtx,' is ', k

		for regionkey in regionCuts:
                    for ivar, varname in enumerate(varlist_):
                        hname = 'Fake'+regionkey+'_'+varname
                        if selectionFeatureVector(fv,regionkey,varname):
                            fillth1(histoStructDict[hname].Control,fv[ivar], weight)
                            fillth1(histoStructDict[hname].Method,fv[ivar], k*weight)
					
					
										
	if MBSRevent:
                for idisp, disp in enumerate(MBSRdisappearingTracks):
                    dt = MBSRdisappearingTracks[0]
                    getID = getGenID(dt)
                    if not getID == 0 : continue  # always match as it is plotting the truth
                    adjustedNJets = 0		
                    adjustedBTags = 0		
                    adjustedJets = []
                    adjustedHt = 0
                    adjustedMet = metvec
                    adjustedMht = TLorentzVector()
                    adjustedMht.SetPxPyPzE(0,0,0,0)
                    for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue
			if not abs(jet.Eta())<5.0: continue###update to 2.4
			if not jet.DeltaR(dt)>0.4: continue###update to include second disappearing track
			adjustedMht-=jet
			if not abs(jet.Eta())<2.4: continue###update to 2.4			
			if c.Jets_bDiscriminatorCSV[ijet]>BTAG_CSV: adjustedBTags+=1
			adjustedJets.append(jet)
			adjustedHt+=jet.Pt()
                    adjustedNJets = len(adjustedJets)
                    mindphi = 4
                    for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))			
                #	if not adjustedNJets>0: continue				
                    pt = dt.Pt()
                    eta = abs(dt.Eta())
                    phi = abs(dt.Phi())

#                    R = 2*(abs(pt - adjustedMht.Pt())/(pt + adjustedMht.Pt()))
                    R = 2*(abs(pt - adjustedMet.Pt())/(pt + adjustedMet.Pt()))
                    dPhi =  math.acos(math.cos((adjustedMet.Phi()-phi)))

                    fv = [adjustedHt,adjustedMht.Pt(),R,len(MBSRdisappearingTracks),dPhi,adjustedNJets, len(MBCRdisappearingTracks), pt,eta]
                    fv.append(getBinNumber(fv))
                    fv.append(nVtx)
                    for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
                            if selectionFeatureVector(fv,regionkey,varname):
                                fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Truth,fv[ivar], weight)



print 'number of electrons', check
fnew_.cd()
hHt.Write()
hHtWeighted.Write()
writeHistoStruct(histoStructDict)
print 'just created', fnew_.GetName()
fnew_.Close()
fKappa.Close()   # remore these file close commands
