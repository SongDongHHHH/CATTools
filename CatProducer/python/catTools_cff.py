import FWCore.ParameterSet.Config as cms

def catTool(process, runOnMC=True, doSecVertex=True, useMiniAOD = True):
    catJetsSource = "slimmedJets"
    catGenJetsSource = "slimmedGenJets"
    catMETsSource = "slimmedMETs"
    catJetsPuppiSource = "slimmedJetsPuppi"
    catMETsPuppiSource = "slimmedMETsPuppi"
    catMuonsSource = "slimmedMuons"
    catElectronsSource = "slimmedElectrons"
    catPhotonsSource = "slimmedPhotons"
    catTausSource = "slimmedTaus"
    catVertexSource = "offlineSlimmedPrimaryVertices"
    catMCsource = "prunedGenParticles"
    catBeamSpot = "offlineBeamSpot"
    catRho = "fixedGridRhoAll"
    ePidNames = cms.vstring()
    btagNames = cms.vstring("pfCombinedInclusiveSecondaryVertexV2BJetTags")
    #JECUncertainlyPayload = cms.string("AK4PFchs")
    JECUncertainlyPayload = cms.string("")

    process.nEventsTotal = cms.EDProducer("EventCountProducer")
    process.nEventsFiltered = cms.EDProducer("EventCountProducer")
    process.load("CATTools.CatProducer.catCandidates_cff")
#######################################################################
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
    ## Hcal HBHE
    process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
    process.HBHENoiseFilterResultProducer.minZeros = cms.int32(99999)
    process.ApplyBaselineHBHENoiseFilter = cms.EDFilter('BooleanFlagFilter',
        inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResult'),
        reverseDecision = cms.bool(False)
    )

    process.p = cms.Path(
        process.nEventsTotal*
        process.HBHENoiseFilterResultProducer* #produces HBHE bools
        process.ApplyBaselineHBHENoiseFilter*  #reject events based
        process.nEventsFiltered
    )
#######################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription
# recompute the T1 PFMET
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    runMetCorAndUncFromMiniAOD( process, isData= not runOnMC )

# MET without HF
    process.noHFCands = cms.EDFilter("CandPtrSelector",
                                     src=cms.InputTag("packedPFCandidates"),
                                     cut=cms.string("abs(pdgId)!=1 && abs(pdgId)!=2 && abs(eta)<3.0")
                                     )
    runMetCorAndUncFromMiniAOD( process, isData=not runOnMC, pfCandColl=cms.InputTag("noHFCands"), postfix="NoHF")
    process.catMETsNoHF = process.catMETs.clone()
    process.catMETsNoHF.src = cms.InputTag("slimmedMETsNoHF")
    
    ## no residuals currently available 
    process.patPFMetT1T2Corr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT1T2SmearCorr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT2Corr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT2SmearCorr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.shiftedPatJetEnDown.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
    process.shiftedPatJetEnUp.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
    process.patPFMetT1T2CorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT1T2SmearCorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT2CorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT2SmearCorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.shiftedPatJetEnDownNoHF.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
    process.shiftedPatJetEnUpNoHF.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
#######################################################################    
# adding pfMVAMet
    process.load("RecoJets.JetProducers.ak4PFJets_cfi")
    process.ak4PFJetsForPFMVAMet = process.ak4PFJets.clone()
    process.ak4PFJetsForPFMVAMet.src = cms.InputTag("packedPFCandidates")
    #This is temporary solution to avoid the circular dependenc error. Hope the recipe for miniAOD is available soon.(Tae Jeong) 
    #https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideUnscheduledExecution#Circular_Dependence_Errors
    from JetMETCorrections.Configuration.DefaultJEC_cff import ak4PFJetsL1FastL2L3
    process.load("RecoMET.METPUSubtraction.mvaPFMET_cff")
    process.pfMVAMEt.srcUncorrJets = cms.InputTag("ak4PFJetsForPFMVAMet")
    process.pfMVAMEt.srcPFCandidates = cms.InputTag("packedPFCandidates")
    process.pfMVAMEt.srcVertices = cms.InputTag("offlineSlimmedPrimaryVertices")
    process.pfMVAMEt.srcCorrJets = cms.InputTag("calibratedAK4PFJetsForPFMVAMEt")
    process.pfMVAMEt.inputFileNames = cms.PSet(
        U     = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru_7_4_X_miniAOD_50NS_July2015.root'),
        DPhi  = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrphi_7_4_X_miniAOD_50NS_July2015.root'),
        CovU1 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru1cov_7_4_X_miniAOD_50NS_July2015.root'),
        CovU2 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru2cov_7_4_X_miniAOD_50NS_July2015.root')
    )
    process.calibratedAK4PFJetsForPFMVAMEt.src = cms.InputTag("ak4PFJetsForPFMVAMet")
    process.puJetIdForPFMVAMEt.jec =  cms.string('AK4PF')
    process.puJetIdForPFMVAMEt.vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")
    process.puJetIdForPFMVAMEt.rho = cms.InputTag("fixedGridRhoFastjetAll")
    process.load("PhysicsTools.PatAlgos.producersLayer1.metProducer_cfi")
    process.patMETsPfMva = process.patMETs.clone()
    process.patMETsPfMva.addGenMET    = cms.bool(False)
    process.patMETsPfMva.metSource  = cms.InputTag("pfMVAMEt")
    process.patMETsPfMva.muonSource = cms.InputTag(catMuonsSource)
    process.catMETsPfMva = process.catMETs.clone()
    process.catMETsPfMva.src = cms.InputTag("patMETsPfMva")
#######################################################################
# redoing puppi from miniAOD as recommended
# https://twiki.cern.ch/twiki/bin/view/CMS/PUPPI
    process.load('CommonTools/PileupAlgos/Puppi_cff')
    process.puppi.candName = cms.InputTag('packedPFCandidates')
    process.puppi.vertexName = cms.InputTag('offlineSlimmedPrimaryVertices')
    # remaking puppi jets
    from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox
    jetToolbox( process, 'ak4', 'ak4JetSubs', 'out', PUMethod='Puppi', JETCorrLevels = ['L1FastJet', 'L2Relative', 'L3Absolute'] ) 
    catJetsPuppiSource = "selectedPatJetsAK4PFPuppi"
    # remaking puppi met
    from RecoMET.METProducers.PFMET_cfi import pfMet
    process.pfMetPuppi = pfMet.clone();
    process.pfMetPuppi.src = cms.InputTag('puppi')
    process.patPfMetPuppi = process.patMETs.clone()
    process.patPfMetPuppi.addGenMET    = cms.bool(False)
    process.patPfMetPuppi.metSource  = cms.InputTag("pfMetPuppi")
    process.patPfMetPuppi.muonSource = cms.InputTag(catMuonsSource)
    catMETsPuppiSource = "patPfMetPuppi"

    # for puppi isolation
    #process.packedPFCandidatesWoMuon  = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV>=2 && abs(pdgId)!=13 " ) )
    #process.particleFlowNoMuonPUPPI.candName         = 'packedPFCandidatesWoMuon'
    #process.particleFlowNoMuonPUPPI.vertexName       = 'offlineSlimmedPrimaryVertices'
#######################################################################    
# getting jec from file for jec on the fly from db file
# currently only for mc
    if runOnMC:
        #era = "PHYS14_V4_MC"
        era = "Summer15_50nsV2_MC"
        from CondCore.DBCommon.CondDBSetup_cfi import CondDBSetup
        process.jec = cms.ESSource("PoolDBESSource",CondDBSetup,
            connect = cms.string('sqlite_fip:CATTools/CatProducer/data/'+era+'.db'),
            toGet = cms.VPSet(
                cms.PSet(
                    record = cms.string("JetCorrectionsRecord"),
                    tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PF"),
                    label= cms.untracked.string("AK4PF")),
                cms.PSet(
                    record = cms.string("JetCorrectionsRecord"),
                    tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PFchs"),
                    label= cms.untracked.string("AK4PFchs")),
                cms.PSet(
                    record = cms.string("JetCorrectionsRecord"),
                    tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PUPPI"),
                    label= cms.untracked.string("AK4PUPPI")),
            ))
        process.es_prefer_jec = cms.ESPrefer("PoolDBESSource","jec")
        print "JEC based on", process.jec.connect
## applying new jec on the fly
        if useMiniAOD:
            process.load("PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff")
            catJetsSource = "patJetsUpdated"
            ### updating puppi jet jec
            process.patJetPuppiCorrFactorsUpdated = process.patJetCorrFactorsUpdated.clone(
                payload = cms.string('AK4PUPPI'),
                src = cms.InputTag(catJetsPuppiSource),
            )
            process.patJetsPuppiUpdated = process.patJetsUpdated.clone(
                jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetPuppiCorrFactorsUpdated")),
                jetSource = cms.InputTag(catJetsPuppiSource),
            )
            catJetsPuppiSource = "patJetsPuppiUpdated"

#######################################################################
## for egamma pid temp 
## https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Recipe_for_regular_users_for_74X
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import DataFormat,switchOnVIDElectronIdProducer,setupAllVIDIdsInModule,setupVIDElectronSelection
    if not useMiniAOD :
        dataFormat = DataFormat.AOD
    else :
        dataFormat = DataFormat.MiniAOD
    
    switchOnVIDElectronIdProducer(process, dataFormat)    
    my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_PHYS14_PU20bx25_V2_cff',
                    'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV51_cff']
    for idmod in my_id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

    if useMiniAOD:
        process.catElectrons.electronIDSources = cms.PSet(
            eleVetoIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-veto"),
            eleLooseIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-loose"),
            eleMediumIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-medium"),
            eleTightIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-tight"),
            eleHEEPIdMap = cms.InputTag("egmGsfElectronIDs:heepElectronID-HEEPV51"),
        )
#######################################################################    
    if runOnMC:## Load MC dependent producers
        ## FIX ME - pile up and pdf weight
        process.load("CATTools.CatProducer.pdfWeight_cff")
        process.load("CATTools.CatProducer.pileupWeight_cff")
        process.pileupWeight.vertex = cms.InputTag(catVertexSource)

        if not useMiniAOD:
            process.load("CATTools.CatProducer.genTopProducer_cfi")
                    
        process.catMuons.shiftedEnDownSrc = cms.InputTag("shiftedPatMuonEnDown")
        process.catMuons.shiftedEnUpSrc = cms.InputTag("shiftedPatMuonEnUp")
        process.catElectrons.shiftedEnDownSrc = cms.InputTag("shiftedPatElectronEnDown")
        process.catElectrons.shiftedEnUpSrc = cms.InputTag("shiftedPatElectronEnUp")

    if doSecVertex:
        from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import TransientTrackBuilderESProducer
        setattr(process, "TransientTrackBuilderESProducer", TransientTrackBuilderESProducer)
        #process.makeCatCandidates += process.catSecVertexs
                
    process.catJets.src = cms.InputTag(catJetsSource)
    process.catJets.genJetMatch = cms.InputTag("patJetGenJetMatch")
    process.catJets.btagNames = btagNames
    process.catJets.payloadName = JECUncertainlyPayload
    process.catTaus.src = cms.InputTag(catTausSource)
    process.catTaus.genJetMatch = cms.InputTag("tauGenJetMatch")
    process.catMuons.src = cms.InputTag(catMuonsSource)
    process.catMuons.mcLabel = cms.InputTag(catMCsource)
    process.catMuons.vertexLabel = cms.InputTag(catVertexSource)
    process.catMuons.beamLineSrc = cms.InputTag(catBeamSpot)
    process.catElectrons.src = cms.InputTag(catElectronsSource)
    process.catElectrons.ePidNames = ePidNames
    process.catElectrons.vertexLabel = cms.InputTag(catVertexSource)
    process.catElectrons.mcLabel = cms.InputTag(catMCsource)
    process.catElectrons.beamLineSrc = cms.InputTag(catBeamSpot)
    process.catElectrons.rhoLabel = cms.InputTag(catRho)
    process.catPhotons.src = cms.InputTag(catPhotonsSource)
    process.catMETs.src = cms.InputTag(catMETsSource)
    process.catSecVertexs.muonSrc = cms.InputTag(catMuonsSource)
    process.catSecVertexs.elecSrc = cms.InputTag(catElectronsSource)
    process.catSecVertexs.vertexLabel = cms.InputTag(catVertexSource)

    process.catJetsPuppi.src = cms.InputTag(catJetsPuppiSource)
    process.catJetsPuppi.genJetMatch = cms.InputTag("patJetGenJetMatch")
    process.catJetsPuppi.btagNames = btagNames
    process.catJetsPuppi.payloadName = JECUncertainlyPayload    
    process.catMETsPuppi.src = cms.InputTag(catMETsPuppiSource)
    process.catVertex.vertexLabel = cms.InputTag(catVertexSource)
