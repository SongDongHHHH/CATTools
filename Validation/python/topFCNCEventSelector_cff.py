import FWCore.ParameterSet.Config as cms
from CATTools.CatAnalyzer.leptonSF_cff import *
from CATTools.CatAnalyzer.flatGenWeights_cfi import *

eventsFCNC = cms.EDFilter("TopFCNCEventSelector",
    isMC = cms.bool(True),
    channel = cms.string("electron"),
    ## alwaysAcceptAfter : Accept event even though selection may fail _AFTER_ this step
    ## Use case: store ntuple only for events that passes step4
    applyFilterAt = cms.int32(9), ## 9 is nJet3

    # Physics objects
    muon = cms.PSet(
        src = cms.InputTag("catMuons"),
        scaleDirection = cms.int32(0),
        #scaleDirection = cms.int32(-1),
        #scaleDirection = cms.int32(+1),
        efficiencySF = muonSFTight,
        efficiencySFDirection = cms.int32(0),
    ),

    electron = cms.PSet(
        src = cms.InputTag("catElectrons"),
        idName = cms.string("cutBasedElectronID-Summer16-80X-V1-medium"),
        vetoIdName = cms.string("cutBasedElectronID-Summer16-80X-V1-loose"),

        #idName = cms.string("mvaEleID-Spring15-25ns-Trig-V1-wp90"),
        scaleDirection = cms.int32(0),
        #scaleDirection = cms.int32(-1),
        #scaleDirection = cms.int32(+1),
        efficiencySF = electronSFCutBasedIDMediumWP,
        efficiencySFDirection = cms.int32(0),
        #applyEcalCrackVeto = cms.bool(True),
        applyEcalCrackVeto = cms.bool(False),
        skipSmearing = cms.bool(False), # Needed for synchronization
    ),

    jet = cms.PSet(
        src = cms.InputTag("catJets"),
        bTagName = cms.string("pfCombinedInclusiveSecondaryVertexV2BJetTags"),
        bTagWP = cms.string("CSVM"),
        scaleDirection = cms.int32(0),
        #scaleDirection = cms.int32(-1),
        #scaleDirection = cms.int32(+1),
        resolDirection = cms.int32(0),
        #resolDirection = cms.int32(-1),
        #resolDirection = cms.int32(+1),
        skipJER = cms.bool(False), # Needed for synchronization
    ),

    met = cms.PSet(
        src = cms.InputTag("catMETs"),
    ),

    vertex = cms.PSet(
        useGoodPV = cms.bool(True), # Use the good PV to select event
        nVertex = cms.InputTag("catVertex", "nGoodPV"),
        src = cms.InputTag("catVertex"),
        #src = cms.InputTag("offlineSlimmedPrimaryVertices"),
        pileupWeight = cms.InputTag("pileupWeight"),
    ),

    # Filters
    filters = cms.PSet(
        filterRECO = cms.InputTag("filterRECO"),
        trigMU = cms.InputTag("filterTrigMU"),
        trigEL = cms.InputTag("filterTrigEL"),
        ignoreTrig = cms.bool(False), # Accept event even if it does not pass HLT. Needed for synchronization
        efficiencySFDirection = cms.int32(0),
    ),

    # Event weights
    genWeight = cms.PSet(
        index = cms.int32(-1),
        src = cms.InputTag("flatGenWeights"),
    ),
    extWeights = cms.VInputTag(),
)

