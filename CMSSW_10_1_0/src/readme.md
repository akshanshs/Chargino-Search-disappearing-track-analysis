
Here Prompt, Fake Bkg and hadronic tau estimation is done, Signal is plotted , observed DATA is plotted , with uncertanity.  Final stacked Histograms is produced. 

Full analysis procedure from Estimation methid losure prediction till final trees for DATA cards.


1) Make Transfer factors from MC and DATA
2) Make closure test
3) Make prediction from DATA

prompt: 1 script for Hist making, 1 script for computimg, 1 script for comparing Kappas, 1 script for closure, 1 script for prediction.

1)Make kappa transfer factors for electrons and Muons.

python python/whip_condor.py python/TagNProbeHistMaker_CB.py   "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.DYJetsToLL_M-50*.root"
makes Hists for computing transfer factors. from MC DY for Tag and Probe and Gen info.

python python/whip_condor.py python/TagNProbeHistMaker_CB.py   "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu*.root" 
make hist for computing kappa factor from gen infi only.

python python/whip_condor.py python/TagNProbeHistMaker_CB.py "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Run2016*Single*.root"

make hists for kappa calculation from DATA Single electron and Muon data sets.


stores Hists in : TagProbeTrees/

hadd them: 

Compute kappa: with function up down error fits

python python/ComputeKappa_CB.py TagProbeTrees/TagnProbeHists_triggered_masked_Filtered_Lep2016_6Feb_dm30Variable.root Kappa_DATA_dmVariable.root
#Kappa_DATA_dmVariable.root file has the kappa factors

compute kappa for Muons and Electrons. Same code for DATA and MC.

Compare kappa from MC and tag and Probe MC as below
Important plots::

python python/CompareKappas_CB.py Kappa_MC_DY.root : Compares kappa from TagNProbe and Gen Info.

python python/CompareKappasDYandWJ_CB.py kappa_DYnoweightdm10dPhi1p0.root kappa_WJnoweightdm10dPhi1p0.root # plots WJ , DY from gen info over DY TagNprobe comparision

python python/MakeKappaDatahist.py Kappa_Run2016dm301p01p11p5rebin.root # mkae kappa plots for data with error fits

python python/CompareInvMass.py TagProbeTrees/TagnProbeHists_Run2016SmearDM30nodPhicutbjet0ForInvMass.root  TagProbeTrees/TagnProbeHists_Run2016SmearDM30nodPhicutbjet0ForInvMass.root  # compares invariant masses overlaid of tag + reco ele and tag+ DT 

python python/CompareResponse.py /nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/MCTemplatesBinned/BinnedTemplatesIIDY_WJ_TT.root  /nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/MCTemplatesBinned/BinnedTemplatesIIDY_WJ_TT.root    ## compare responc=se tempplates from MC

python python/MakeDataSmearTempHists.py usefulfiles/DataDrivenSmear_Run2016_PixAndStrips.root  # make smearing templates from data


currently not using following method for systematics:
python python/CreateKappaVariation.py Kappa_Run2016dm301p01p11p5rebin.root    # create several kapa distributions by gaussian spreading

 python python/MakeKappaDataVariationhists.py  # overlay the variation of kappas

python python/2D.py usefulfiles/Mask6mar.root  # plot 2D hists Masks


2)
Mke hists for Closure:
python python/whip_condor.py python/PromptBkgHistMaker_CB.py "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu*.root"

makes hists for Control region , expected counts('method' hists) and true counts(truth hists).

files stored in : TagProbeTrees/
mv TagProbeTrees/PromptBkgHists_WJetsToLNu*nFiles1Truth.root output/smallchunks/

Run closure script: python python/closurePromptBkg.py 

stores out hists in: pdfs/closure/prompt-bkg/

3)
Make prediction:


###################################
##python python/whipPrompt.py python/PromptBkgPredictionHistMakerwithSYS_CB.py "/pnfs/desy.de/cms/tier2##/store/user/sbein/NtupleHub/Production2016v2/Run2016*-03Feb2017_ver2-v2.Single*.root"
##
##Stores hists in :::::PromptHists
##makes hists for conrol region, prediction, prediction_up(down), and prediction_error
##new file with latest correction and also gives json for lumi calc:: PromptBkgPredictionHistMakerwithSYS_CB_withLumiCalc.py 
##Simply hadd them:
########################
Fakes:

1)script for Making hists in SideBand : same script makes jists in SR and CR region: python/ABCD_faketrack_histsSideBand.py

run: source submitEventBkg_fakeSB.sh

Output in FakeHists/
for MC :do:
        rm -r haddFakeHistDir/ScaledHadd_*
        rm haddFakeHistDir/smallchunks/*
        mv SB_FakeHists*Tune*nFiles1.root haddFakeHistDir/smallchunks

run: python ../python/HaddWithScale.py 'haddFakeHistDir/smallchunks/*Hists_*CUET*.root' 'SB_+'WHATEVER_SUFFIX'+.root'

Get Histograms drawn: python python/StackFakeHists_trackSplit.py FakeHists/SB_FakeHists_Run20nodPhicut.root : makes hists for CR and SR both

For DTATA: Simple Hadd the output from

python python/whipFakes.py python/ABCD_faketrack_histsSideBand.py "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/*Run2016*SingleMuon*.root" 


Get Histograms drawn: python python/StackFakeHists_trackSplit.py FakeHists/SB_FakeHists_Run20nodPhicut.root : makes hists for CR and SR both.

the above combined BKG used to get transfer factors:
python python/ComputeAlpha.py FakeHists/haddFakeHistDir/SB_MCDYnoPhiCutPt20.root SB_AlphaMCDYnoPhiCutPt20.root  ## also gives UP and DOWN variations f functions for estimating errors.

2)script for Making hists in MainBand : same script makes jists in SR and CR region:  python/ABCD_faketrack_histsMainBand.py

source submitEventBkg_fakeMB.sh

do:
        rm -r haddFakeHistDir/ScaledHadd_*
        rm haddFakeHistDir/smallchunks/*
	mv MB_FakeHists*Tune*nFiles1.root haddFakeHistDir/smallchunks

run: python ../python/HaddWithScale.py 'haddFakeHistDir/smallchunks/*Hists_*CUET*.root' 'MB_+'WHATEVER_SUFFIX'+.root'

Get Histograms drawn: python python/StackFakeHists_trackSplit.py FakeHists/MB_FakeHists_Run20nodPhicut.root : makes hists for CR and SR both.

WARNING:  Only see the CR histograms especially in DATA, just to see the control region distribution, DONT see hists in MBSR.

Just for MC to check the consistncy of transfer factors: aka transfer factor closure: python python/ComputeAlpha.py FakeHists/haddFakeHistDir/MB_MCDYnoPhiCutPt20.root MB_AlphaMCDYnoPhiCutPt20.root


3) Closure:
run:
source submitEventBkg_fakeClosure.sh
it has commands like:
python python/whipFakes.py python/FakeBkgHistMaker.py "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.TTJets_TuneCUETP8M1_13TeV*.root" ........

do :
		rm -r fakeoutput/closure*
		rm fakeoutput/smallchunks/*
		mv FakeHists/FakeBkgHists*CUET*.root fakeoutput/smallchunks/
 python python/closureFakeBkg.py :  makes canvs for closure

4)Make prediction:
###########################################
##python python/whipFakes.py python/FakeBkgPredictionHistMakerwithSYS.py "/pnfs/desy.de/cms/tier2/store/##user/sbein/NtupleHub/Production2016v2/*Run2016*MET*.root"
new file(latest correctons too): also gives json for lumi calc:FakeBkgPredictionHistMakerwithSYS_withLumiCalc.py 
##stores hists in FakeHists/   :::::::::::Simply hadd them
##makes hists for conrol region, prediction, prediction_up(down), and prediction_error
############################################
Hadronic:
Estimated with MC, uncertanity taken 100% 
##########################################
##Prediction
##source submitTauPredict.sh
##
##has commands like ::  python python/whipTau.py python/TauhadPredictionHistMakerwithSYS.py   "MC SAMPLE##S"
##
##stores hists in ::: TauHists
##
##do : 
##        rm -r haddeventHists/ScaledHadd_*
##        rm haddeventHists/smallchunks/*
##        mv Tau*Hists*Tune*nFiles1.root haddeventHists/smallchunks
##Run: python ../python/HaddTauBkgWithScale.py 'haddeventHists/smallchunks/*Tau*Hists_*CUET*.root'  'Ou##tputFileName'
##########################################

Signal: Prediction:
############################################
##  source submitSigPredict.sh  
##  has commands like :: python python/whipChargino.py python/SignalPredictionHistMakerwithSYS.py "MC sa##mples"
##do:  
##	rm -r haddeventHists/ScaledHadd_*
##	rm haddeventHists/smallchunks/*
## 	mv Signal*Hists*nFiles1.root haddeventHists/smallchunks
##Run:  python ../python/HaddSigEventWithScale.py 'haddeventHists/smallchunks/*Signal*Hists_*CUET*.root'##  'Suffix'
##
##  Here we put suffix which we want to apper at the end of all Different Sigfiles...we dont lump them t##ogether
##############################################

DATA : Observation :

##########################################################
###
###python python/whipData.py python/DataObservationHistMakerwithSYS.py "DATA file list **"
###Hists stored in DataHists
###Simple hadd them
###############################################################

##########################

limi calculation::

merge jsons: python python/mergeJson_calclumi.py PromptHists  ## the argument is the dir where the jsons for each job is present.

creates a die with merged json in it.   use bril calc to get lumi




NEXT STACK hists with observation Make data cards plot limits.
refer readme_ResultandLimit.md