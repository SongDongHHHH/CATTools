import FWCore.ParameterSet.Config as cms

## for egamma pid https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Recipe_for_regular_users_for_8_0
def enableElectronVID(process):
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import switchOnVIDElectronIdProducer, DataFormat, setupAllVIDIdsInModule, setupVIDElectronSelection
    switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)

    electron_ids = [
        'cutBasedElectronHLTPreselecition_Summer16_V1_cff',
        'cutBasedElectronID_Summer16_80X_V1_cff',
        'heepElectronID_HEEPV70_cff',
        'mvaElectronID_Spring16_GeneralPurpose_V1_cff',
        'mvaElectronID_Spring16_HZZ_V1_cff',
    ]
    for idmod in electron_ids:
        idmod = "RecoEgamma.ElectronIdentification.Identification."+idmod
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

    electron_idNames = [
        "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto",
        "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose",
        "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium",
        "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight",
        "egmGsfElectronIDs:cutBasedElectronHLTPreselection-Summer16-V1",
        "egmGsfElectronIDs:heepElectronID-HEEPV70",
        "egmGsfElectronIDs:mvaEleID-Spring16-GeneralPurpose-V1-wp90",
        "egmGsfElectronIDs:mvaEleID-Spring16-GeneralPurpose-V1-wp80",
        "egmGsfElectronIDs:mvaEleID-Spring16-HZZ-V1-wpLoose",
    ]
    process.catElectrons.electronIDSources = cms.PSet()
    for idName in electron_idNames:
        setattr(process.catElectrons.electronIDSources,
                idName.split(':',1)[1].replace('-','_'),
                cms.InputTag(idName))
        process.catElectrons.electronIDs.append(idName.split(':',1)[1])

    process.egmGsfElectronIDs.physicsObjectSrc = process.catElectrons.unsmaredElectrons
    process.electronMVAValueMapProducer.srcMiniAOD = process.catElectrons.unsmaredElectrons

    return process

def enablePhotonVID(process):
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import switchOnVIDPhotonIdProducer, DataFormat, setupAllVIDIdsInModule, setupVIDPhotonSelection
    switchOnVIDPhotonIdProducer(process, DataFormat.MiniAOD)

    #Use IDs from https://github.com/cms-sw/cmssw/blob/CMSSW_7_4_X/RecoEgamma/PhotonIdentification/python/Identification/ 
    photon_ids = [
        'cutBasedPhotonID_Spring16_V2p2_cff',
        'mvaPhotonID_Spring16_nonTrig_V1_cff',
    ]
    for idmod in photon_ids:
        idmod = 'RecoEgamma.PhotonIdentification.Identification.'+idmod
        setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)

    photon_idNames = [
        "egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-loose",
        "egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-medium",
        "egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-tight",
        "egmPhotonIDs:mvaPhoID-Spring16-nonTrig-V1-wp80",
        "egmPhotonIDs:mvaPhoID-Spring16-nonTrig-V1-wp90",
    ]
    process.catPhotons.photonIDSources = cms.PSet()
    for idName in photon_idNames:
        setattr(process.catPhotons.photonIDSources,
                idName.split(':',1)[1].replace('-','_'),
                cms.InputTag(idName))
        process.catPhotons.photonIDs.append(idName.split(':',1)[1])

    process.egmPhotonIDs.physicsObjectSrc = process.catPhotons.unsmearedPhotons
    process.photonMVAValueMapProducer.srcMiniAOD = process.catPhotons.unsmearedPhotons
    process.photonIDValueMapProducer.srcMiniAOD = process.catPhotons.unsmearedPhotons

    return process

