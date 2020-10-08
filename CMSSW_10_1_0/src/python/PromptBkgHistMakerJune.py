import sys
import time
from ROOT import *
from utils import *
from utilsII import *
from glob import glob
from random import shuffle
from FWCore.ParameterSet.VarParsing import VarParsing
import random
datamc = 'mc'
mZ = 91

doGenVersion = True
RelaxGenKin = False

options = VarParsing ('python')
options.parseArguments()
weight = 1 #################################WEIGHT                                                                                                                                                              

gROOT.SetBatch()
gROOT.SetStyle('Plain')
inputFiles = options.inputFiles

if inputFiles ==  []:
        print 'running on small default DYtoLL sample'
        inputFiles = ["/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v1/Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_4_RA2AnalysisTree.root"]
x = len(inputFiles)


c = TChain('TreeMaker2/PreSelection')
datamc == 'mc' 

for f in range(0,x):
        print 'file number:', f, ':',inputFiles[f]
        c.Add(inputFiles[f])
nentries = c.GetEntries()

verbosity = 1000
identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
identifier+='nFiles'+str(len(inputFiles))

newfname = 'PromptBkgHists_'+identifier+'.root'

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)

inf = 9999
regionCuts = {}
regionCuts['NoCuts']              = [(0,inf),(0,inf),(15,inf),(0,2.4),(0,inf)]
regionCuts['LowMhtBaseline']      = [(150,inf),(1,inf),(15,inf),(0,2.4),(0,inf)]

if doGenVersion: newfname = newfname.replace('.root','Truth.root')
fnew_ = TFile(newfname,'recreate')

varlist_ = ['Mht','NJets','TrkPt','TrkEta','BTags']
indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
for region in regionCuts:
    for var in varlist_:
        histname = region+'_'+var
        histoStructDict[histname] = mkHistoStruct(histname)

def selectionFeatureVector(fvector, regionkey='', omitcuts=''):
    iomits = []
    for cut in omitcuts.split('Vs'): iomits.append(indexVar[cut])
    for i, feature in enumerate(fvector):
        if i in iomits: continue
        if not (feature>=regionCuts[regionkey][i][0] and feature<=regionCuts[regionkey][i][1]):
            return False
    return True


sfname = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/test_KappaMC_TruthWTDTruth.root'
#if doGenVersion: sfname = sfname.replace('.root','Truth.root')
fSF = TFile(sfname)
#fSF.ls()
hDtElRatioDict = {}

ptbins = []
print binning['TrkPt']
for ibin, bin in enumerate(binning['TrkPt'][:-1]):
	ptbins.append((binning['TrkPt'][ibin],binning['TrkPt'][ibin+1]))
print 'ptbins', ptbins

etabins = []
print binning['TrkEta']
for ibin, bin in enumerate(binning['TrkEta'][:-1]):
	etabins.append((binning['TrkEta'][ibin],binning['TrkEta'][ibin+1]))
print etabins


for etabin_ in etabins:
	for ptbin in ptbins:
		name = 'hInvMassDtElRatio_eta%dto%d_pt%dto%d' % (10*etabin_[0],10*etabin_[1],ptbin[0],ptbin[1])
		print name
		name = name.replace('9999','Inf')
		print etabin_,ptbin
		
		hDtElRatioDict[(etabin_,ptbin)] = fSF.Get(name)
		print hDtElRatioDict[(etabin_,ptbin)]
		print hDtElRatioDict[(etabin_,ptbin)].GetBinContent(hDtElRatioDict[(etabin_,ptbin)].FindBin(mZ))
#		pause()
#c.Show(0)
nEvents = c.GetEntries()
verbosity = round(100000)

import time
t1 = time.time()
i0=0
for ientry in range(i0,c.GetEntries()):
	#if not ientry in [71503,127912,128655,128893]: continue ##skip
	if ientry<i0+2: 
		import time
		t0 = time.time()    
	if ientry%verbosity==0:
		t1 = time.time()
		rtime1 = (time.time()-t0)*nEvents/(ientry+1)*(1-1.0*ientry/nEvents), 'sec'
		print 'processing', ientry,'/',nEvents, ' = ', 1.0*ientry/nEvents,'remaining time estimate: ', rtime1 		

	c.GetEntry(ientry) 
	hHt.Fill(c.HT)
	#hHtWeighted.Fill(c.HT,c.CrossSection)

	if doGenVersion:
		if not c.NJets>=1: continue
		genels = []
		for igp, gp in enumerate(c.GenParticles):
			if not gp.Pt()>15: continue
			#if not gp.Pt()<45: continue			
			if not abs(gp.Eta())<2.4: continue
			#if not abs(gp.Eta())<0.6: continue			
			if not abs(c.GenParticles_PdgId[igp])==11: continue
			genels.append(gp)
		if not len(genels)==1: continue
		#print 'yeah, we passed it..hmmm'

	RecoElectrons = []
	for iel, ele in enumerate(c.Electrons):
		if not ele.Pt()>15: continue
		#if not ele.Pt()<45: continue		
		if not abs(ele.Eta())<2.4: continue
		if not c.Electrons_passIso[iel]: continue		
		RecoElectrons.append(ele)
	muons = []		
	for imu, muon in enumerate(c.Muons):
		if not muon.Pt()>15: continue
		if not abs(muon.Eta())<2.4: continue	
		muons.append([muon,c.Muons_charge[imu]])
		
	if not len(muons)==0: continue	
	electrons = []
	disappearingTracks = []
	for itrack, track in enumerate(c.tracks):
		#print itrack	
		if not track.Pt()>15: continue
		#if not track.Pt()<45: continue
		if not abs(track.Eta())<2.4: continue       
		phits = c.tracks_nValidPixelHits[itrack]
		thits = c.tracks_nValidTrackerHits[itrack]
		tlayers = c.tracks_trackerLayersWithMeasurement[itrack]			
		short = phits>0 and thits==phits
		medium = tlayers< 7 and (thits-phits)>0
		LONG   = tlayers>=7 and (thits-phits)>0      
		if short: passesDXY = abs(c.tracks_dxyVtx[itrack])<0.02
		else: passesDXY = abs(c.tracks_dxyVtx[itrack])<0.01
		if not passesDXY: continue		
		#print 'c', itrack  
		isElectron = False
		for ele in RecoElectrons:
			#print 'electron', ele.Pt(), ele.DeltaR(track)
			if ele.DeltaR(track)<0.02:
				isElectron = True
				electrons.append([track,c.tracks_charge[itrack]])
				#print 'iselectron!', ele.Pt()				
				break
		if isElectron: continue		
		if not (c.tracks_nMissingOuterHits[itrack]>=2): continue		
		if not abs(c.tracks_dzVtx[itrack])<0.05: continue
		neutralIso = c.tracks_neutralPtSum[itrack]/track.Pt()
		if not (c.tracks_neutralPtSum[itrack]<=10 and neutralIso<=0.1): continue
		chargedIso = c.tracks_chargedPtSum[itrack]/track.Pt()
		if not (c.tracks_chargedPtSum[itrack]<=10 and chargedIso<=0.1): continue
		if not c.tracks_passPFCandVeto[itrack]: continue												
		if not c.tracks_trkRelIso[itrack]<0.2: continue
		if not track.Pt()*c.tracks_trkRelIso[itrack]<10: continue				
		nhits = c.tracks_nValidTrackerHits[itrack]
		nlayers = c.tracks_trackerLayersWithMeasurement[itrack]
		if not (nlayers>=2 and nhits>=2): continue
		if not (c.tracks_nMissingInnerHits[itrack]==0): continue
		pterr = c.tracks_ptError[itrack]/(track.Pt()*track.Pt())
		if short: 
			if not (pterr<0.2): continue
		if medium: 
			if not (pterr<0.05): continue
		if LONG: 
			if not (pterr<0.005): continue								
		if not (c.tracks_trackQualityHighPurity[itrack]): continue
		disappearingTracks.append(track)



	singleEleEvent_ = bool(len(electrons)==1)	
	#print ientry, 'electrons', electrons, 'disappearingTracks', disappearingTracks
	singleDisTrkEvent = bool(len(disappearingTracks)==1)

	if not (singleEleEvent_ or singleDisTrkEvent): continue
	#print 'D'
	if (len(electrons)>0 and len(disappearingTracks)>0): continue	
	#print 'passed event cuts'
	
	weight = c.CrossSection
	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET)

	if singleEleEvent_:
		if doGenVersion:
			if not electrons[0][0].DeltaR(genels[0])<0.02: continue
		#adjustedMet = metvec.Pt()-RecoElectrons[0]
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
		adjustedNJets = 0
		for jet in c.Jets:
			if not jet.Pt()>30: continue
			if not abs(jet.Eta())<5.0: continue
			if not jet.DeltaR(electrons[0][0])>0.5: continue
			adjustedMht-=jet
			adjustedNJets+=1
		#if not adjustedNJets>0: continue
		if doGenVersion:
			if RelaxGenKin:
				pt = electrons[0][0].Pt()
				eta = abs(electrons[0][0].Eta())
			else: 
				pt = genels[0].Pt()
				eta = abs(genels[0].Eta())
		else:
			pt = electrons[0][0].Pt()
			eta = abs(electrons[0][0].Eta())		
		ptbin = findbin(ptbins,pt)
		etabin = findbin(etabins,abs(eta))
		fv = [adjustedMht.Pt(),adjustedNJets,pt,abs(eta),c.BTags]		
		print hDtElRatioDict[(etabin,ptbin)]
		#pause()
		sf = hDtElRatioDict[(etabin,ptbin)].GetBinContent(hDtElRatioDict[(etabin,ptbin)].FindBin(mZ))
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					#if 'NoCuts' in regionkey and 'TrkPt' in varname:
					#	print ientry, 'found electron, pT=', fv[2]#, electrons, disappearingTracks
					histoStructDict[hname].Control.Fill(fv[ivar], weight)	
					histoStructDict[hname].Method.Fill(fv[ivar], sf*weight)						
	
	if singleDisTrkEvent: 
		if doGenVersion:
			if not disappearingTracks[0].DeltaR(genels[0])<0.02: continue
		adjustedNJets = 0
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)		
		for jet in c.Jets:
			if not jet.Pt()>30: continue
			if not abs(jet.Eta())<5.0: continue
			if not jet.DeltaR(disappearingTracks[0])>0.5: continue	
			adjustedMht-=jet			
			adjustedNJets+=1	
		if not adjustedNJets>0: continue				
		if doGenVersion:
			if RelaxGenKin: 
				pt = disappearingTracks[0].Pt()
				eta = abs(disappearingTracks[0].Eta())
			else: 
				pt = genels[0].Pt()
				eta = abs(genels[0].Eta())
		else: 
			pt = disappearingTracks[0].Pt()
			eta = abs(disappearingTracks[0].Eta())			
		fv = [adjustedMht.Pt(),adjustedNJets,pt,abs(eta),c.BTags]					
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					if 'NoCuts' in regionkey and 'TrkPt' in varname:
						print ientry,'found disappearing track, pT=', fv[2]
					histoStructDict[hname].Truth.Fill(fv[ivar], weight)
	
fnew_.cd()
hHt.Write()
hHtWeighted.Write()
writeHistoStruct(histoStructDict)
print 'just created', fnew_.GetName()
fnew_.Close()


