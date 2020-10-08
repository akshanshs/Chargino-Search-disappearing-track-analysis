import sys
import time
import numpy as np
from ROOT import *
from utils_Sam import *
from glob import glob
from random import shuffle
from FWCore.ParameterSet.VarParsing import VarParsing
import random

#options = VarParsing ('python')
#options.parseArguments()

 
gROOT.SetBatch()
gROOT.SetStyle('Plain')

verbose = False
try: inputFileNames = sys.argv[1]
except:
        print 'running on small default DYtoLL sample'
	inputFileNames = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_117_RA2AnalysisTree.root"
inputFiles = glob(inputFileNames)
x_ = len(inputFiles)

c = TChain("TreeMaker2/PreSelection")
datamc = 'mc'
mZ = 91
print mZ
##pause()
doGenVersion = True
RelaxGenKin = True

fileKappa = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/Kappa.root'
fKappa  = TFile(fileKappa)
KappaMap = fKappa.Get("kappaPtvsEta")
KappaMapPlus = fKappa.Get("kappaPtvsEtaPlus")
KappaMapMinus = fKappa.Get("kappaPtvsEtaMinus")
KappaMapPt = fKappa.Get("kappaGenInfoPt")

print KappaMapPt.GetBinContent(0)
print KappaMapPt.GetBinContent(1)
print KappaMapPt.GetBinContent(2)
print KappaMapPt.GetBinContent(3)
print KappaMapPt.GetBinContent(4)
print KappaMapPt.GetBinContent(5)
print KappaMapPt.GetBinContent(6)
print KappaMapPt.GetBinContent(7)
print KappaMapPt.GetBinContent(8)
print KappaMapPt.GetBinContent(9)
print KappaMapPt.GetBinContent(10)
print KappaMapPt.GetBinContent(11)


print KappaMap.GetBinContent(1,1)
print KappaMap.GetBinContent(2,2)
print KappaMap.GetBinContent(3,3)
print KappaMap.GetBinContent(4,4)
print KappaMap.GetBinContent(5,1)
print KappaMap.GetBinContent(6,2)
print KappaMap.GetBinContent(7,3)
print KappaMap.GetBinContent(8,4)
print KappaMap.GetBinContent(9,1)
print KappaMap.GetBinContent(10,2)

#pause()
hHTmad         = TH1F("hHTmad","hHTmad", 150,40,2500)
hPtControl     = TH1D("hPtControl", "PtControl", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
hPtMethod      = TH1D("hPtMethod", "PtMethod", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
hPtTruth       = TH1D("hPtTruth", "PtTruth", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
histoStyler(hPtControl,1)
histoStyler(hPtMethod,1)
histoStyler(hPtTruth ,1)
# (Ptbin,Etabin)::(x,y)
for f in range(0,x_):
	print 'file number:', f, ':',inputFiles[f]
	c.Add(inputFiles[f])
nentries = c.GetEntries()

verbosity = 1000
identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
identifier+='nFiles'+str(len(inputFiles))
print 'Identifier', identifier


newfname = 'PromptBkgHists_'+identifier+'.root'

if doGenVersion: newfname = newfname.replace('.root','Truth.root')
fnew_ = TFile(newfname,'recreate')
print 'Will write results to', newfname

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)

inf = 999999999
regionCuts = {}
regionCuts['NoCuts']              = [(0,inf),(0,inf),(0,inf),(0,inf),(0,2.4),(0,inf)]
regionCuts['LowMhtBaseline']      = [(200,inf),(150,inf),(1,inf),(15,inf),(0,2.4),(0,inf)]


dKappaBinList = {}
for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
        for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
                newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))
                dKappaBinList[newHistKey] = [iPtBin+1,iEtaBin+1]



varlist_ = ['Ht','Mht','NJets','TrkPt','TrkEta','BTags']
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


#sfname = 'ScaleFactors/EleDtSfMC.root'
#if doGenVersion: sfname = sfname.replace('.root','Truth.root')
'''
fSF = TFile(sfname)
fSF.ls()
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
		name = name.replace('9999','Inf')
		hDtElRatioDict[(etabin_,ptbin)] = fSF.Get(name)
'''
for histkey in dKappaBinList:
	print histkey, 'Ptbin', dKappaBinList[histkey][0],'EtaBin', dKappaBinList[histkey][1]
#pause()
#fname = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/MCTemplatesBinned/BinnedTemplatesIIDY_WJ_TT.root'
fname = '/nfs/dust/cms/user/beinsam/LongLiveTheChi/Analyzer/CMSSW_8_0_21/src/DataDrivenSmear.root' #from Benjamin
fSmear  = TFile(fname)

dResponseHist = {}
for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
        for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
                newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))
                dResponseHist[newHistKey] = fSmear.Get("htrkresp"+str(newHistKey))



##pause()
#c.Show(0)
nEvents = c.GetEntries()
verbosity = round(100000)

readerPixelOnly = TMVA.Reader()
pixelXml = '/nfs/dust/cms/user/kutznerv/cmsdas/BDTs/newpresel3-200-4-short-nodxyVtx/weights/TMVAClassification_BDT.weights.xml'
#pixelXml = '/nfs/dust/cms/user/kutznerv/shorttrack/CMSSW_10_1_7/src/shorttrack/cutoptimization/tmva/newpresel3-200-4-short/weights/TMVAClassification_BDT.weights.xml'
prepareReader(readerPixelOnly, pixelXml)
readerPixelStrips = TMVA.Reader()
trackerXml = '/nfs/dust/cms/user/kutznerv/cmsdas/BDTs/newpresel2-200-4-medium-nodxyVtx/weights/TMVAClassification_BDT.weights.xml'
#trackerXml = '/nfs/dust/cms/user/kutznerv/shorttrack/CMSSW_10_1_7/src/shorttrack/cutoptimization/tmva/newpresel2-200-4-medium/weights/TMVAClassification_BDT.weights.xml'
prepareReader(readerPixelStrips, trackerXml)

def getSF(Eta, Pt, Draw = False):
	for histkey in  dResponseHist:
		if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
			SF_trk = 10**(dResponseHist[histkey].GetRandom())
			return SF_trk
	return 1

def getKappa_(Eta, Pt, charge = 0):
        for histkey in dKappaBinList:
                if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
			if charge == 0:kappa = KappaMap.GetBinContent(dKappaBinList[histkey][0],dKappaBinList[histkey][1])  #10**(dResponseHist[histkey].GetRandom())
			#kappa = KappaMapPt.GetBinContent(dKappaBinList[histkey][0])
			if charge == 1  : kappa = KappaMapPlus.GetBinContent(dKappaBinList[histkey][0],dKappaBinList[histkey][1])
			if charge == -1 : kappa = KappaMapMinus.GetBinContent(dKappaBinList[histkey][0],dKappaBinList[histkey][1])
                        return kappa
        return 1
import time
#pause()
t1 = time.time()
i0=0
verbosity = 1000
print c.GetEntries(), 'evets to be Analysed'
for ientry in range(nentries):
	if ientry%verbosity==0:
		a = 1
		print 'now processing event number', ientry
	if verbose:
		if not ientry in [15385]: continue
#	print 'getting entry', ientry
	c.GetEntry(ientry)
	files = str(inputFiles)
	if 'QCD' in files:
		if  ((not '_HT' in files) and c.madHT > 100): continue
	if 'DYJetsToLL' in files:
		if  ((not '_HT' in files) and c.madHT > 100): continue
        if 'TTJets_' in files:
                if  ((not '_HT' in files) and c.madHT > 600): continue
        if 'WJetsToLNu_' in files:
		if  ((not '_HT' in files) and c.madHT > 100): continue

	hHt.Fill(c.HT)
	hHTmad.Fill(c.madHT)
#	weight = 1
	weight = (c.CrossSection*35.9)/(1*.001)
	#hHtWeighted.Fill(c.HT,c.CrossSection)
#	weight = c.CrossSection
	if doGenVersion:
		genels = []
		for igp, gp in enumerate(c.GenParticles):
			if not gp.Pt()>10: continue
			if not abs(gp.Eta())<2.4: continue
			if ((abs(gp.Eta()) < 1.566) and abs(gp.Eta()) > 1.4442): continue
#			if not abs(c.GenParticles_ParentId[igp]) == 24: continue 
			if not (abs(c.GenParticles_PdgId[igp])==11 and c.GenParticles_Status[igp] == 1) : continue
			genels.append(gp)
#		if doGenVersion:
		if not len(genels)==1: continue

	basicTracks = []
	disappearingTracks = []
	for itrack, track in enumerate(c.tracks):
		if not track.Pt() > 5 : continue
		if not abs(track.Eta()) < 2.4: continue
		if abs(abs(track.Eta()) < 1.566) and abs(track.Eta()) > 1.4442: continue
		if not isBaselineTrack(track, itrack, c): continue
		basicTracks.append(track)
		if not (track.Pt() > 15 and track.Pt()<600): continue
		if not isDisappearingTrack_(track, itrack, c, readerPixelOnly, readerPixelStrips): continue
		disappearingTracks.append(track)

	mva, dedx, trkpt, trketa, trkp = -999, -999, -999, -999, -999
	nprompt = 0
	moh = -1
	pt = -1

	RecoElectrons = []
	SmearedElectrons = []
	for iel, ele in enumerate(c.Electrons):
		if verbose: print ientry, iel,'ele with Pt' , ele.Pt()
		smearedEle = TLorentzVector()
		smearedEle.SetPtEtaPhiE(0, 0, 0, 0)
		if not ele.Pt() > 5 : continue
		if ((abs(ele.Eta()) < 1.566) and abs(ele.Eta()) > 1.4442): continue
		if not abs(ele.Eta())<2.4: continue
		if verbose: print 'passed eta and Pt'
		if not c.Electrons_passIso[iel]: continue
		drBig4Trk = 9999
		matchedTrack = TLorentzVector()

		for trk in basicTracks:
			drTrk = trk.DeltaR(c.Electrons[iel])
			if drTrk<drBig4Trk:
				matchedTrack = trk 
				drBig4Trk = drTrk
				if drTrk<0.01: break
		if not drBig4Trk<0.01: continue
		if verbose: print 'passed baseline track'
		RecoElectrons.append(ele)
		sf = getSF(abs(matchedTrack.Eta()), min(matchedTrack.Pt(),309.999))
		smearedEle.SetPtEtaPhiE(sf*c.Electrons[iel].Pt(),c.Electrons[iel].Eta(),c.Electrons[iel].Phi(),sf*c.Electrons[iel].E())
		if not (smearedEle.Pt()>15 and smearedEle.Pt()<600): continue
		SmearedElectrons.append([smearedEle,c.Electrons_charge[iel]])
	muons = []		
	for imu, muon in enumerate(c.Muons):
		if not muon.Pt()>15: continue
		if abs(abs(muon.Eta()) < 1.566) and abs(muon.Eta()) > 1.4442: continue
		if not abs(muon.Eta())<2.4: continue	
		muons.append([muon,c.Muons_charge[imu]])

	if not len(muons)==0: continue	

	singleEleEvent_ = bool(len(SmearedElectrons)==1)
	singleDisTrkEvent = bool(len(disappearingTracks)==1)
	if not (singleEleEvent_ or singleDisTrkEvent): continue

#	print len(SmearedElectrons), "SmearedElectrons"
	#print ientry, 'SmearedElectrons', SmearedElectrons, 'disappearingTracks', disappearingTracks
#	print len(disappearingTracks), "disappearing tracks"
	#pause()
	#print 'D'
#	if (len(SmearedElectrons)>0 and len(disappearingTracks)>0): continue	
	#print 'passed event cuts'
	
	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET)

	if singleEleEvent_:
		if doGenVersion: yo =1
			#if not SmearedElectrons[0][0].DeltaR(genels[0])<0.02: continue
		#adjustedMet = metvec.Pt()-RecoElectrons[0]
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
		adjustedNJets = 0
		for jet in c.Jets:
			if not jet.Pt()>30: continue
			if not abs(jet.Eta())<5.0: continue
			if not jet.DeltaR(RecoElectrons[0])>0.5: continue
			adjustedMht-=jet
			adjustedNJets+=1
		#if not adjustedNJets>0: continue
		if doGenVersion:
                        if RelaxGenKin:
				pt = SmearedElectrons[0][0].Pt()
				eta = abs(SmearedElectrons[0][0].Eta())
                        else:
				pt = genels[0].Pt()
                                eta = abs(genels[0].Eta())
		else:
			pt = SmearedElectrons[0][0].Pt()
			eta = abs(SmearedElectrons[0][0].Eta())		
	#	ptbin = findbin(ptbins,pt)
	#	etabin = findbin(etabins,abs(eta))
	#	if abs(eta) > 1.4442 and abs(eta) < 1.566 : print abs(eta), 'eta of electron'
		fv = [c.HT,adjustedMht.Pt(),adjustedNJets,pt,abs(SmearedElectrons[0][0].Eta()),c.BTags]		
		k = getKappa_(abs(eta),min(pt,309.99),SmearedElectrons[0][1])
		#print 'Kappa is', k
#		fillth1(hPtControl,fv[3],1*weight)
#		fillth1(hPtMethod,fv[3],k*weight)
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					#print 'In filling place', fv[ivar]
					
					#pause()
					#if 'NoCuts' in regionkey and 'TrkPt' in varname:
					#	if (fv[3] < 20) : print ientry, 'found electron, pT=', fv[3], 'kappa is ', k#, SmearedElectrons, disappearingTracks
					fillth1(histoStructDict[hname].Control,fv[ivar], weight)	
					fillth1(histoStructDict[hname].Method,fv[ivar], k*weight)						
#	pause()
	if singleDisTrkEvent:
		adjustedNJets = 0
		if not disappearingTracks[0].DeltaR(genels[0])<0.02: continue
		#if doGenVersion:
		#	if not disappearingTracks[0].DeltaR(genels[0])<0.02: continue
		adjustedNJets = 0
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)		
		for jet in c.Jets:
			if not jet.Pt()>30: continue
			if not abs(jet.Eta())<5.0: continue
			if not jet.DeltaR(disappearingTracks[0])>0.5: continue	
			adjustedMht-=jet			
			adjustedNJets+=1	
	#	if not adjustedNJets>0: continue				
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
		fv = [c.HT,adjustedMht.Pt(),adjustedNJets,pt,abs(disappearingTracks[0].Eta()),c.BTags]					
#		fillth1(hPtTruth,fv[3], weight)
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
#					if 'NoCuts' in regionkey and 'TrkPt' in varname:
#						print ientry,'found disappearing track, pT=', fv[3]
					fillth1(histoStructDict[hname].Truth,fv[ivar], weight)
	
fnew_.cd()
hHTmad.Write()
hHt.Write()
hHtWeighted.Write()
writeHistoStruct(histoStructDict)
print 'just created', fnew_.GetName()

#pause()



fnew_.Close()
print 'file closed'
#pause()
