import sys
import time
import numpy as np
from ROOT import *
from utilitiesII import *
from glob import glob
from random import shuffle
import random
import math
import json
BTAG_CSV = 0.8484
check = 0
Pt_threshold = 30
debug = True
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
useGenKappa = False
RelaxGenKin = True
ClosureMode = False #false means run as if real data  so basicallly perform prediction
SmearLeps = False
verbose = False


identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
identifier+='nFiles'+str(len(inputFiles))
output_json_filename = inputFiles[0].split("/")[-1].replace(".root", ".json")

print 'filename:' , inputFiles[0]
#print 'identifier:', identifier
print 'json`identifier:', output_json_filename


newfname = 'Prompt_BkgPredictionwithSYSHists_'+identifier+'.root'

if genMatchEverything: newfname = newfname.replace('.root','Truth.root')
fnew_ = TFile(newfname,'recreate')
print 'Will write results to', newfname

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)

###for debugging
hGenPtvsEtaRECO_den    = TH2D("hGenPtvsEtaRECO_den","hGenPtvsEtaRECO_den",len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
hGenPtvsEtaDT_num    = TH2D("hGenPtvsEtaDT_num","hGenPtvsEtaDT_num",len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
########


inf = 999999
SingleMuonEvents = 0
SingleElectronEvents = 0



varlist_ = ['Ht','Met','R','NTags','dPhi','NJets','NElectrons','NMuons', 'TrkPt','TrkEta','BinNumber','nVtx']
 
regionCuts = {}

#regionVars:                       [HT   ,         MET,       R,      Ntag,    dPhi,    Njets,   NElectrons, NMuons,  TrkPt,   TrkEta, BinNumber ]

#regionVars:                       [HT   ,         MET,       R,      Ntag,    dPhi,    Njets,  NElectrons, NMuons , TrkPt,   TrkEta, BinNumber , nVtx]      
#regionCuts['NoCuts']             = [(0,inf),   (0.0,inf), (-1.0,2), (0,inf), (-1,3.2), (0,inf), (0,0),      (0,0), (0,inf), (0,2.4), (-1,inf), (0,inf)]
#regionCuts['LoweredMhtBaseline'] = [(250,inf), (150,inf), (-1.0,2), (0,inf), (-1,3.2), (1,inf), (0,0  ),    (0,0  ), (0,inf), (0,2.4), (-1,inf), (-1,inf)]
#regionCuts['Baseline']           = [(250,inf), (150,inf), (-1.0,2), (0,inf), (-1,2.5), (1,inf), (0,0  ),    (0,0  ), (0,inf), (0,2.4), (-1,inf), (-1,inf)]
#regionCuts['SignalRegion']       = [(250,inf), (200,inf), (-1.0,2), (0,inf), (-1,2.5), (1,inf), (0,0  ),    (0,0  ), (0,inf), (0,2.4), (-1,inf), (-1,inf)]
regionCuts['SignalRegion1jet']   = [(250,inf), (250,inf), (-1.0,2), (0,inf), (-1,2.5), (1,inf), (0,0  ),    (0,0  ), (0,inf), (0,2.4), (-1,inf), (-1,inf)]
#regionCuts['SignalRegion2jet']   = [(250,inf), (250,inf), (-1.0,2), (0,inf), (-1,2.5), (2,inf), (0,0  ),    (0,0  ), (0,inf), (0,2.4), (-1,inf), (-1,inf)]
#regionCuts['ClosureRegion']      = [(250,inf), (150,inf), (-1.0,2), (0,inf), (-1,2.5), (1,inf), (0,0  ),    (0,0  ), (0,inf), (0,2.4), (0,inf), (-1,inf)]
indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructPredictDict = {}
for region in regionCuts:
    for var in varlist_:
        histname = 'El'+region+'_'+var
        histoStructPredictDict[histname] = mkHistoStructPredict(histname)
        histname = 'Mu'+region+'_'+var
        histoStructPredictDict[histname] = mkHistoStructPredict(histname)        
                
binnumbers = {}

#BIN:          HT        MET       R

binnumbers[((250,600),(250,400),(-1,1))] = 1
binnumbers[((600,inf),(250,400),(-1,1))] = 2
binnumbers[((250,600),(400,inf),(-1,1))] = 3
binnumbers[((600,inf),(400,inf),(-1,1))] = 4
binnumbers[((250,600),(250,400),( 1,2))] = 5
binnumbers[((600,inf),(250,400),( 1,2))] = 6
binnumbers[((250,600),(400,inf),( 1,2))] = 7
binnumbers[((600,inf),(400,inf),( 1,2))] = 8

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
else: madranges = [(0, inf)]


#pause()
#fname_MC = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/MCTemplatesBinned/BinnedTemplatesIIDY_WJ_TT.root'
#fname_MC = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/usefulfiles/DataDrivenSmear_2016MC.root'
fname_MC = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/usefulfiles/DataDrivenSmear_DYJets_PixAndStrips.root'
#fname_DATA = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/usefulfiles/DataDrivenSmear_2016Data.root'
fname_DATA = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/usefulfiles/DataDrivenSmear_Run2016_PixAndStrips.root'

if ClosureMode: fSmear  = TFile(fname_MC)
else: fSmear  = TFile(fname_DATA)

fMask = TFile('/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/usefulfiles/Mask6mar.root')
if not ClosureMode : hMask = fMask.Get('hEtaVsPhiDT_maskData-2016Data-2016')   #'hEtaVsPhiDT_maskRun2016')
else: hMask = ''

dResponseHist = {}
for iPtBinEdge, PtBinEdge in enumerate(PtBinEdgesForSmearing[:-1]):
    for iEtaBinEdge, EtaBinEdge_ in enumerate(EtaBinEdgesForSmearing[:-1]):
        newHistKey = ((EtaBinEdge_,EtaBinEdgesForSmearing[iEtaBinEdge + 1]),(PtBinEdge,PtBinEdgesForSmearing[iPtBinEdge + 1]))
        dResponseHist[newHistKey] = fSmear.Get("htrkresp"+str(newHistKey))

print 'dResponseHist', dResponseHist
def getSmearFactor(Eta, Pt, Draw = False):
	for histkey in  dResponseHist:
		if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
			if SmearLeps: return 10**(dResponseHist[histkey].GetRandom())
			else: return 1.0
	print 'returning 1', Eta, Pt, dResponseHist
	return 1


if ClosureMode: fileKappa = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/'#Kappa_DY_Weighted5Feb.root'#Kappa_DY_noWeight5Feb.root'#kappa_smearLeps_Pt1000.root'
else: fileKappa = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/kappa_plots3.root' #Kappa_DATA_dphi0p8_jetleq1_3_June.root'#using new currently, oldfile:'Kappa_Run2016dm301p01p11p5rebin31Marbinextentionforfunction.root' # the new file has lower kappa for muons, slightly lower kappa for electrons, larger uncertainty for electros, May consider using old kappa for electrons and new file for kappa for muons

fileKappaMu = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/kappaMuII.root'
fileKappaEle = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/kappaEleII.root'

fKappa  = TFile(fileKappa)

fKappaEle  = TFile(fileKappaEle)
fKappaMu  = TFile(fileKappaMu)

fElProbePt_Kappas = {}
fElProbePt_Kappas_up = {}
fElProbePt_Kappas_down = {}

fGenElProbePt_Kappas = {}

fMuProbePt_Kappas = {}
fMuProbePt_Kappas_up = {}
fMuProbePt_Kappas_down = {}

fGenMuProbePt_Kappas = {}


for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
	etakey = (EtaBin,EtaBinEdges[iEtaBin + 1])
	specialpart = '_eta'+str(etakey).replace('(','').replace(')','').replace(', ','to')

	oldNumName = "hElProbePtDT"+specialpart+"_num"
	newKappaName = oldNumName.replace('_num','').replace('DT','Kappa')
#############
	newKappaFuncName = 'f1'+newKappaName+'base'
        newKappaFuncName_up   = 'f1'+newKappaName+'_up'
        newKappaFuncName_down = 'f1'+newKappaName+'_down'
        fElProbePt_Kappas[etakey] = fKappaEle.Get(newKappaFuncName).Clone()
        fElProbePt_Kappas_up[etakey] = fKappaEle.Get(newKappaFuncName_up).Clone()
        fElProbePt_Kappas_down[etakey] = fKappaEle.Get(newKappaFuncName_down).Clone()
#	fElProbePt_Kappas[etakey] = fKappa.Get(newKappaFuncName).Clone()
#        fElProbePt_Kappas_up[etakey] = fKappa.Get(newKappaFuncName_up).Clone()
#        fElProbePt_Kappas_down[etakey] = fKappa.Get(newKappaFuncName_down).Clone()
############
	oldNumName = "hMuProbePtDT"+specialpart+"_num"
	newKappaName = oldNumName.replace('_num','').replace('DT','Kappa')
############
	newKappaFuncName = 'f1'+newKappaName+'base'
        newKappaFuncName_up   = 'f1'+newKappaName+'_up'
        newKappaFuncName_down = 'f1'+newKappaName+'_down'
        fMuProbePt_Kappas[etakey] = fKappaMu.Get(newKappaFuncName).Clone()
        fMuProbePt_Kappas_up[etakey] = fKappaMu.Get(newKappaFuncName_up).Clone()
        fMuProbePt_Kappas_down[etakey] = fKappaMu.Get(newKappaFuncName_down).Clone()
#	fMuProbePt_Kappas[etakey] = fKappa.Get(newKappaFuncName).Clone()
#        fMuProbePt_Kappas_up[etakey] = fKappa.Get(newKappaFuncName_up).Clone()
#        fMuProbePt_Kappas_down[etakey] = fKappa.Get(newKappaFuncName_down).Clone()
###########
		
if useGenKappa: 
	kappadictEl = fGenElProbePt_Kappas   # this dictionary has eta bins as keys which points to the kappa fitted function
	kappadictMu = fGenMuProbePt_Kappas	
else: 
	kappadictEl      = fElProbePt_Kappas
        kappadictEl_up   = fElProbePt_Kappas_up
        kappadictEl_down = fElProbePt_Kappas_down
	kappadictMu      = fMuProbePt_Kappas	
        kappadictMu_up   = fMuProbePt_Kappas_up
        kappadictMu_down = fMuProbePt_Kappas_down


dKappaBinList = {}
for iPtBinEdge, PtBinEdge in enumerate(PtBinEdges[:-1]):
        for iEtaBinEdge, EtaBinEdge in enumerate(EtaBinEdges[:-1]):
                newHistKey = ((EtaBinEdge,EtaBinEdges[iEtaBinEdge + 1]),(PtBinEdge,PtBinEdges[iPtBinEdge + 1]))
                dKappaBinList[newHistKey] = [iPtBinEdge+1,iEtaBinEdge+1]
                
                
def fetchKappa(Eta, Pt, KappaDict=fGenElProbePt_Kappas):   # will fetch kappa for up down and mean kappa
	for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
		etakey = (EtaBin,EtaBinEdges[iEtaBin + 1])
		if abs(Eta) >= etakey[0] and abs(Eta) <= etakey[1]:
			#return 1
			kappa = KappaDict[etakey].Eval(Pt)
#			print 'got an', kappa
			return kappa
	print etakey, Eta
	print 'didnt get anything meaningful', Eta, Pt
	return 1


def TriggerResult(trigger):
    for i, index in enumerate(trigger):
        if c.TriggerPass[index] ==1: return True
    return False
	
ElectronTriggers = [14, 15, 16, 17, 18, 19, 20, 21]
MuonTriggers = [24,25,26,27,28,30,31,32]
MetTriggers = [53, 54, 55, 56, 57, 58, 59, 60, 109,110,111,112,113,114,115,116,117,118,119,120,124,125,126,127,128,129,130,131,132,133,134,135,136]

	
import time
t1 = time.time()
i0=0
verbosity = 10000
runs = {}
print nentries, 'evets to be analyzed'
for ientry, event in enumerate(c):

################                                                                                                                                               
        if (ientry+1) % 10000 == 0:
            PercentProcessed = int( 20 * ientry / nentries )
            line = "[" + PercentProcessed*"#" + (20-PercentProcessed)*" " + "]\t" + "Processing event %s / %s" % (ientry + 1, nentries)
            print line

        runnum = event.RunNum
        lumisec = event.LumiBlockNum

        if runnum not in runs:
            runs[runnum] = []

        if lumisec not in runs[runnum]:
            runs[runnum].append(lumisec)


############### 




	if verbose:
		if not ientry in [670]: continue
	if ientry%verbosity==0:
		print 'now processing event number', ientry, 'of', nentries
		
	if verbose: print 'getting entry', ientry
	c.GetEntry(ientry) 
	hHt.Fill(c.HT)
        if not ClosureMode: weight = 1
	else: weight = c.CrossSection
	hHtWeighted.Fill(c.HT,weight)
	
        nVtx = c.nAllVertices
	isValidHtRange = False
#        isValidHtRange = True     # removing madHT requiremnt for # to has to be updated
        if ClosureMode:
            for madrange in madranges:
		if (c.madHT>madrange[0] and c.madHT<madrange[1]):
                    isValidHtRange = True
                    break
        if ClosureMode:
            if not isValidHtRange: continue

        if not ClosureMode:
            if TriggerResult(MetTriggers) == False : continue
#            if (TriggerResult(ElectronTriggers) or TriggerResult(MuonTriggers) ) == False: continue
        if not passesUniversalSelection(c): continue

	if ClosureMode:
		genels = []
		genmus = []
		for igp, gp in enumerate(c.GenParticles):
			if not gp.Pt()>5: continue
			if not abs(gp.Eta())<2.4: continue
			if not (abs(gp.Eta())<1.445 or abs(gp.Eta())>1.56): continue	
			if not c.GenParticles_Status[igp] == 1: continue		
			#if not abs(c.GenParticles_ParentId[igp]) == 24: continue
			if abs(c.GenParticles_PdgId[igp])==11: genels.append(gp)
			if abs(c.GenParticles_PdgId[igp])==13: genmus.append(gp)			
		if genMatchEverything:
			if not (len(genels)==1): continue # or len(genmus) ==1): continue
        if verbose: print 'passed presence of genleps' 
        if verbose: print 'passed calo met and pfmet relation'
	#if not c.JetID: continue
	if verbose: "print test gen electron"
	muons = []		
	for imu, muon in enumerate(c.Muons):
		if not muon.Pt()>10: continue
		#if abs(muon.Eta()) < 1.566 and abs(muon.Eta()) > 1.4442: continue
		if not abs(muon.Eta())<2.4: continue	
		muons.append([muon,c.Muons_charge[imu]])
	#if not len(muons)==0: continue	
	#if verbose: "print test muon"
	basicTracks = []
	disappearingTracks = []	
	for itrack, track in enumerate(c.tracks):
                #if verbose: print "enter the track loop"
		if not track.Pt() > 20 : continue
		if not abs(track.Eta()) < 2.4: continue
		if not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
		if not isBaselineTrack(track, itrack, c, hMask): continue
		basicTracks.append([track,c.tracks_charge[itrack], itrack])
		if not (track.Pt() > Pt_threshold and track.Pt()<9999): continue		
		if not isDisappearingTrack_(track, itrack, c): continue
		drlep = 99                                        # should apply dPhi cuts in the closure mode , this collection is ofcourse not used in data because we just wanted to know total events with disappearing tracks


		passeslep = True # passeslep = does not match any lepton
		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)+list(c.TAPPionTracks)): 
			drlep = min(drlep, lep.DeltaR(track))
			if drlep<0.01: 
				passeslep = False
				break			
		if not passeslep: continue		
		disappearingTracks.append(track)		
    
	SmearedElectrons = []
	RecoElectrons = []
	for iel, ele in enumerate(c.Electrons):
		if verbose: print ientry, iel,'ele with Pt' , ele.Pt()
		if (abs(ele.Eta()) < 1.566 and abs(ele.Eta()) > 1.4442): continue
		if not abs(ele.Eta())<2.4: continue
		if verbose: print 'passed eta and Pt'
		if not c.Electrons_passIso[iel]: continue
		if not c.Electrons_mediumID[iel]: continue
                if verbose: print 'passed iso amd medium ID'
		drmin = inf
		matchedTrk = TLorentzVector()
		for trk in basicTracks:
			drTrk = trk[0].DeltaR(ele)
			if drTrk<drmin:
				if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
				drmin = drTrk
				matchedTrk = trk
				if drTrk<0.01: 
					break
		if not drmin<0.01: continue
                if verbose: print 'found matched track'
		if ele.Pt()>10: RecoElectrons.append([ele, c.Electrons_charge[iel]])
		smear = getSmearFactor(abs(matchedTrk[0].Eta()), min(matchedTrk[0].Pt(),299.999))
		smearedEl = TLorentzVector()
		smearedEl.SetPtEtaPhiE(0, 0, 0, 0)		
		smearedEl.SetPtEtaPhiE(smear*matchedTrk[0].Pt(),matchedTrk[0].Eta(),matchedTrk[0].Phi(),smear*matchedTrk[0].E())
		if not (smearedEl.Pt()> Pt_threshold and smearedEl.Pt()<2499): continue
		SmearedElectrons.append([smearedEl,c.Electrons_charge[iel]])
                if verbose: print 'Pt of matched track =', matchedTrk[0].Pt()
		#print 'a lovely ele', ele.Pt(), smearedEle.Pt()

		
	SmearedMuons = []
	RecoMuons = []
	for ilep, mu in enumerate(c.Muons):
		if verbose: print ientry, ilep,'mu with Pt' , mu.Pt()
		if (abs(mu.Eta()) < 1.566 and abs(mu.Eta()) > 1.4442): continue
		if not abs(mu.Eta())<2.4: continue
		if verbose: print 'passed eta and Pt'
		if not c.Muons_passIso[ilep]: continue
            #    if not c.Muons_tightID[ilep] : continue
                if not c.Muons_mediumID[ilep] : continue
		drmin = inf
		matchedTrk = TLorentzVector()
		for trk in basicTracks:
			drTrk = trk[0].DeltaR(mu)
			if drTrk<drmin:
				if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
				drmin = drTrk
				matchedTrk = trk
				if drTrk<0.01: 
					break
		if not drmin<0.01: continue
		if mu.Pt()>10: RecoMuons.append([mu,c.Muons_charge[ilep]])	
		smear = getSmearFactor(abs(matchedTrk[0].Eta()), min(matchedTrk[0].Pt(),299.999))
		smearedMu = TLorentzVector()
		smearedMu.SetPtEtaPhiE(0, 0, 0, 0)		
		smearedMu.SetPtEtaPhiE(smear*matchedTrk[0].Pt(),matchedTrk[0].Eta(),matchedTrk[0].Phi(),smear*matchedTrk[0].E())
		if not (smearedMu.Pt()> Pt_threshold and smearedMu.Pt()<9999): continue
		SmearedMuons.append([smearedMu,c.Muons_charge[ilep]])	


	singleElEvent_ = len(SmearedElectrons) ==1 #>=1
	singleMuEvent_ = len(SmearedMuons) ==1 #>=1	

        if len(SmearedMuons) > 0 :SingleMuonEvents = SingleMuonEvents + 1
        if len(SmearedElectrons) > 0: SingleElectronEvents = SingleElectronEvents + 1

#        if (len(SmearedElectrons) + len(SmearedMuons) ) > 1 : continue  # already embedded in region cuts def
        
#        if debug:
#            if singleElEvent_ : SingleElectronEvents = SingleElectronEvents + 1 
#            if singleMuEvent_ : SingleMuonEvents = SingleMuonEvents + 1

#	presentDisTrkEvent = len(disappearingTracks) >=1# and len(SmearedElectrons) ==0 and len(SmearedMuons)==0 ##try commenting out last two
	if not (singleElEvent_ or singleMuEvent_): continue # single lepton control region
#	if not (singleElEvent_ or presentDisTrkEvent or singleMuEvent_): continue
	
	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region

	if singleElEvent_:
		elec = random.sample(SmearedElectrons,1)[0][0]
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
                adjustedMet = metvec + elec
		adjustedJets = []
		adjustedHt = 0
		adjustedBTags = 0
		if genMatchEverything:
			dr = elec.DeltaR(genels[0])
			if verbose: print dr
			if not dr<0.02: continue
                        check =check + 1
                        #print ientry, 'found electron with pt =', elec.Pt()
		#print ientry, 'found a tawdry se', elec.Pt()			
		fillth2(hGenPtvsEtaRECO_den, elec.Pt(), abs(elec.Eta()))
		for ijet, jet in enumerate(c.Jets):
                    
			if not jet.Pt()>30: continue
			if not jet.DeltaR(elec)> 0.4: continue####update 
			if not abs(jet.Eta())< 5.0: continue####update to 2.4
			adjustedMht-=jet
			if not abs(jet.Eta()) < 2.4: continue####update to 2.4
			adjustedJets.append(jet)			
			adjustedHt+=jet.Pt()
			if c.Jets_bDiscriminatorCSV[ijet]>BTAG_CSV: adjustedBTags+=1
		adjustedNJets = len(adjustedJets)
		mindphi = 4
		for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))
		
		if genMatchEverything:
		        if RelaxGenKin:
		                pt = elec.Pt()
		                eta = abs(elec.Eta())
                                phi = abs(elec.Phi())
		        else:
		                pt = genels[0].Pt()
		                eta = abs(genels[0].Eta())
                                phi = abs(genels[0].Phi())
		else:
		        pt = elec.Pt()
		        eta = abs(elec.Eta())	
                        phi = abs(elec.Phi())
		ptForKappa = pt
                R = 2*(abs(pt - adjustedMht.Pt())/(pt + adjustedMht.Pt()))
#                dPhi =  math.acos(math.cos((adjustedMht.Phi()-phi)))

                dPhi =  math.acos(math.cos((adjustedMet.Phi()-phi)))
#regionVars:             [HT   ,      MET,        R,             Ntag,        dPhi,    Njets,            NElectrons,        NMuons,TrkPt,TrkEta,BinNumber ] 
		fv = [adjustedHt,adjustedMht.Pt(),R,1+len(disappearingTracks),dPhi,adjustedNJets, len(SmearedElectrons)-1, len(SmearedMuons), pt,eta]
		fv.append(getBinNumber(fv))
                fv.append(nVtx)
		k      = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictEl)
                k_up   = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictEl_up)
                k_down = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictEl_down)
                if not (k >0): k = .0000000001
                if not (k_up >0): k_up = k+0.3*k
                if not (k_down >0): k_down = k-0.3*k
              #  if (k_up-k) < (k-k_down) :
              #      k_down =2*k- k_up
              #  else:
              #      k_up = 2*k-k_down
                #k_up = k + 0.9*(k_up-k)
                #k_down = k - 0.9*(k-k_down)
                if abs(k-k_up) > abs(k-k_down): k_error = abs(k-k_up)
                else : k_error = abs(k-k_down)

		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'El'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					if 'TtbarCtrEl' in regionkey: print 'TtbarCtrEl', fv
					fillth1(histoStructPredictDict[hname].Control,fv[ivar], weight)
					fillth1(histoStructPredictDict[hname].Method,fv[ivar], k*weight)
                                        fillth1(histoStructPredictDict[hname].Method_up,fv[ivar], k_up*weight)
                                        fillth1(histoStructPredictDict[hname].Method_down,fv[ivar], k_down*weight)
					fillth1(histoStructPredictDict[hname].Method_error,fv[ivar], k_error*weight)
#					if debug : print 'filled hists for electrons'
	if singleMuEvent_:
		muon = random.sample(SmearedMuons,1)[0][0]
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
                adjustedMet = metvec + muon
		adjustedJets = []
		adjustedHt = 0
		adjustedBTags = 0
		if genMatchEverything:
			dr = muon.DeltaR(genmus[0])
			if verbose: print dr
			if not dr<0.02: continue
		#print ientry, 'found a tawdry se', elec.Pt()			
		fillth2(hGenPtvsEtaRECO_den, muon.Pt(), abs(muon.Eta()))
		for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue
			if not jet.DeltaR(muon)>0.4: continue####update 
			if not abs(jet.Eta())<5.0: continue####update to 2.4
			adjustedMht-=jet
			if not abs(jet.Eta())<2.4: continue####update to 2.4
			adjustedJets.append(jet)			
			adjustedHt+=jet.Pt()
			if c.Jets_bDiscriminatorCSV[ijet]>BTAG_CSV: adjustedBTags+=1
		adjustedNJets = len(adjustedJets)
		mindphi = 4
		for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))
		
		if genMatchEverything:
		        if RelaxGenKin:
		                pt = muon.Pt()
		                eta = abs(muon.Eta())
                                phi = abs(muon.Phi())
		        else:
		                pt = genmus[0].Pt()
		                eta = abs(genmus[0].Eta())
                                phi = abs(genmus[0].Phi())
		else:
		        pt = muon.Pt()
		        eta = abs(muon.Eta())	
                        phi = abs(muon.Phi())
		ptForKappa = pt
                R = 2*(abs(pt - adjustedMht.Pt())/(pt + adjustedMht.Pt()))
                dPhi =  math.acos(math.cos((adjustedMet.Phi()-phi)))
                fv = [adjustedHt,adjustedMht.Pt(),R,1+len(disappearingTracks),dPhi,adjustedNJets, len(SmearedElectrons), len(SmearedMuons)-1, pt,eta]
		fv.append(getBinNumber(fv))
                fv.append(nVtx)
		k      = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictMu)
                k_up   = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictMu_up)
                k_down = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictMu_down)
                if not (k >0): k = .0000000001
                if not (k_up >0): k_up = k+0.3*k
                if not (k_down >0): k_down = k-0.3*k
                if k_up > 2*k: k_up = k+0.35*k
                if k_down < k- 2*k:k_down = k-0.35*k
               # if (k_up-k) < (k-k_down) :
               #     k_down =2*k- k_up
               # else:
               #     k_up = 2*k-k_down
                #k_up = k + 0.9*(k_up-k)
                #k_down = k - 0.9*(k-k_down)
                if abs(k-k_up) > abs(k-k_down):k_error = abs(k-k_up)
                else : k_error = abs(k-k_down)
                
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'Mu'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					fillth1(histoStructPredictDict[hname].Control,fv[ivar], weight)
					fillth1(histoStructPredictDict[hname].Method,fv[ivar], k*weight)
					fillth1(histoStructPredictDict[hname].Method_up,fv[ivar], k_up*weight)
                                        fillth1(histoStructPredictDict[hname].Method_down,fv[ivar], k_down*weight)
					fillth1(histoStructPredictDict[hname].Method_error,fv[ivar], k_error*weight)
#                                        if debug : print 'filled hists for muons'
print 'number of electrons', check
#if debug:
print 'SingleMuonEvents : ', SingleMuonEvents
print 'SingleElectronEvents : ', SingleElectronEvents
fnew_.cd()
hHt.Write()
hHtWeighted.Write()
hGenPtvsEtaDT_num.Write()
hGenPtvsEtaRECO_den.Write()
writeHistoStructPredict(histoStructPredictDict)
print 'just created', fnew_.GetName()
fnew_.Close()
fKappa.Close()
fSmear.Close()

##############LUMI Calc Part ############ 

runs_compacted = {}
for run in runs:
    if run not in runs_compacted:
        runs_compacted[run] = []
    for lumisec in runs[run]:
        if len(runs_compacted[run]) > 0 and lumisec == runs_compacted[run][-1][-1]+1:
            runs_compacted[run][-1][-1] = lumisec
        else:
            runs_compacted[run].append([lumisec, lumisec])
json_content = json.dumps(runs_compacted)
with open(output_json_filename, "w") as fo:
    fo.write(json_content)

#   fin.Close()                      
print 'just created json:', output_json_filename
############# LUMI calc part finishes ############# 
