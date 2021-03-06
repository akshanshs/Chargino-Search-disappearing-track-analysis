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
ClosureMode = False #false means run as if real data
verbose = False

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
identifier+='nFiles'+str(len(inputFiles))
print 'Identifier', identifier

output_json_filename = inputFiles[0].split("/")[-1].replace(".root", ".json")
newfname = 'Data_ObservationHists_'+identifier+'.root'

if genMatchEverything: newfname = newfname.replace('.root','Truth.root')
fnew_ = TFile(newfname,'recreate')
print 'Will write results to', newfname

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)

inf = 999999

varlist_ = ['Ht','Met','R','NTags','dPhi','NJets','TrkPt','TrkEta','BinNumber','nVtx']
 
regionCuts = {}


## Final SIgnal Region is :: 'SignalRegion1jet'


#regionVars:                       [HT   ,         MET,       R,      Ntag,    dPhi,    Njets,   TrkPt,   TrkEta, BinNumber, nVtx ]
#regionCuts['NoCuts']             = [(0,inf),   (0.0,inf), (-1.0,2), (0,inf), (-1,3.2), (0,inf), (0,inf), (0,2.4), (-1,inf), (0,inf)]
#regionCuts['LoweredMhtBaseline'] = [(250,inf), (150,inf), (-1.0,2), (0,inf), (-1,3.2), (0,inf), (0,inf), (0,2.4), (0,inf), (-1,inf)]
#regionCuts['Baseline']           = [(250,inf), (150,inf), (-1.0,2), (0,inf), (-1,3.2), (1,inf), (0,inf), (0,2.4), (0,inf), (-1,inf)]
#regionCuts['SignalRegion']       = [(250,inf), (200,inf), (-1.0,2), (0,inf), (-1,2.5), (1,inf), (0,inf), (0,2.4), (0,inf), (-1,inf)]
regionCuts['SignalRegion1jet']   = [(250,inf), (250,inf), (-1.0,2), (0,inf), (-1,2.5), (1,inf), (0,inf), (0,2.4), (0,inf), (-1,inf)]
#regionCuts['SignalRegion2jet']   = [(250,inf), (250,inf), (-1.0,2), (0,inf), (-1,2.5), (2,inf), (0,inf), (0,2.4), (0,inf), (-1,inf)]
#regionCuts['ClosureRegion']      = [(250,inf), (150,inf), (-1.0,2), (0,inf), (-1,2.5), (1,inf), (0,inf), (0,2.4), (0,inf), (-1,inf)]

indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructPredictDict = {}
for region in regionCuts:
    for var in varlist_:
        histname = 'Data'+region+'_'+var
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
			if not (fv[iwindow]>=window[0] and fv[iwindow]<=window[1]): foundbin = False
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

fMask = TFile('/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/usefulfiles/Mask6mar.root') #Masks.root')
if not ClosureMode : hMask = fMask.Get('hEtaVsPhiDT_maskData-2016Data-2016')  #'hEtaVsPhiDT_maskRun2016')
else: hMask = ''
        #hMask = fMask.Get('hEtaVsPhiDT_maskRun2016')   

if ClosureMode: fileKappa = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/SB_AlphaRun20nodPhi0p4Pt30Mu30.root'# replace with Alpha 
else: fileKappa = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDIII/CMSSW_10_1_0/src/SB_AlphaRun20nodPhi0p4Pt30Mu30.root'

fKappa  = TFile(fileKappa)

print 'testing alpha', fKappa.Get('f1Bkginclusive_nVtx_Alpha_0').Eval(5)
print 'testing alpha', fKappa.Get('f1Bkginclusive_nVtx_Alpha_0').Eval(10)
print 'testing alpha', fKappa.Get('f1Bkginclusive_nVtx_Alpha_0').Eval(25)
funcKappa      = 'f1Bkginclusive_nVtx_Alpha_0'
funcKappa_up   = 'f1Bkginclusive_nVtx_Alpha_0_up'
funcKappa_down = 'f1Bkginclusive_nVtx_Alpha_0_down'
def fetchKappa(nVtx , kappafuncname):   # replace with simple fetching alpha function
    if nVtx > 1 and nVtx < 55:
        print 'the kappa factor', fKappa.Get(kappafuncname).Eval(nVtx)
        return fKappa.Get(kappafuncname).Eval(nVtx)
    elif nVtx >= 55: return fKappa.Get(kappafuncname).Eval(55)
    elif nvtx < 2: return fKappa.Get(kappafuncname).Eval(2)

def TriggerResult(trigger):
    for i, index in enumerate(trigger):
        if c.TriggerPass[index] ==1: return True
    return False

MetTriggers = [53, 54, 55, 56, 57, 58, 59, 60,109,110,111,112,113,114,115,116,117,118,119,120,124,125,126,127,128,129,130,131,132,133,134,135,136]

def getGenID(track):
    drsmall = 0.2
    gen_id = False
    for igen, gen in enumerate(c.GenParticles):
        if not ((abs(c.GenParticles_PdgId[igen]) == 15)) : continue
#        if not (abs(c.GenParticles_PdgId[igen]) == 1000024 and c.GenParticles_Status[igen] == 1): continue
        if gen.Pt() < 15:continue
        dr = gen.DeltaR(track)
        if dr < drsmall:
            drsmall = dr
    if drsmall < 0.01: return True
    else : return gen_id
	
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

runs = {}
print nentries, 'evets to be analyzed'
for ientry, event  in enumerate(c):

###############   LUMI CALC part: making json                                              

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

        if TriggerResult(MetTriggers) == False: continue
        if not passesUniversalSelection(c): continue
        if not leptonVeto(): continue

	basicTracks = []
	disappearingTracks = []	
        tauTracks = []
	for itrack, track in enumerate(c.tracks):
                #if verbose: print "enter the track loop"
		if not track.Pt() > 20 : continue
		if not abs(track.Eta()) < 2.4: continue
		if not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
                if not isBaselineTrack(track, itrack, c, hMask): continue
		basicTracks.append([track,1, itrack])
		if not (track.Pt() > Pt_threshold and track.Pt()<9999): continue		
		if not isDisappearingTrack_(track, itrack, c): continue  # in principle it is N minus one disappearing track 
		drlep = 99
		passeslep = True # passeslep = does not match any lepton
		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)): 
			drlep = min(drlep, lep.DeltaR(track))
			if drlep<0.01: 
				passeslep = False
				break			
		if not passeslep: continue
                disappearingTracks.append(track)  # 
    
        dataevent = len(disappearingTracks) > 0 

	if not (dataevent): continue
	
	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region

	if dataevent:
		track = random.sample(disappearingTracks,1)[0]
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
                adjustedMet = metvec
		adjustedJets = []
		adjustedHt = 0
		adjustedBTags = 0
		for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue
#			if not jet.DeltaR(track)>0.04: continue####update 
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
                R = 2*(abs(pt - adjustedMht.Pt())/(pt + adjustedMht.Pt()))
                dPhi =  math.acos(math.cos((adjustedMet.Phi()-phi)))
                fv = [adjustedHt,adjustedMht.Pt(),R,len(disappearingTracks),dPhi,adjustedNJets, pt,eta]
		fv.append(getBinNumber(fv))
                fv.append(nVtx)
                uncertainity = 0 
		k      = 1
                k_up   = 1 + uncertainity
                k_down = 1 - uncertainity
                if abs(k-k_up) > abs(k-k_down): k_error = abs(k-k_up)
                else : k_error = abs(k-k_down)

		for regionkey in regionCuts:
                    for ivar, varname in enumerate(varlist_):
                        hname = 'Data'+regionkey+'_'+varname
                        if selectionFeatureVector(fv,regionkey,varname):
                            fillth1(histoStructPredictDict[hname].Control,fv[ivar], weight)
                            fillth1(histoStructPredictDict[hname].Method,fv[ivar], k*weight)
                            fillth1(histoStructPredictDict[hname].Method_up,fv[ivar], k_up*weight)
                            fillth1(histoStructPredictDict[hname].Method_down,fv[ivar], k_down*weight)
                            fillth1(histoStructPredictDict[hname].Method_error,fv[ivar], k_error*weight)
					
					
print 'number of electrons', check
fnew_.cd()
hHt.Write()
hHtWeighted.Write()
writeHistoStructPredict(histoStructPredictDict)
print 'just created', fnew_.GetName()
fnew_.Close()
fKappa.Close()   # remore these file close commands


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
print 'just created json:', output_json_filename
############# LUMI calc part finishes #############                
