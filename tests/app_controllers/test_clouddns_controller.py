from app_controllers.clouddns_controller import CloudDnsController
import json
import os
import pytest

pytest.globalData = []

c = CloudDnsController()

def loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

def test_loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

def test_setParentDomain():
    loadGlobalData()
    assert c.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"]) == True

def test_setSubDomainPrefix():
    loadGlobalData()
    assert c.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"]) == True

def test_setParentManagedZone():
    loadGlobalData()
    assert c.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"]) == True

def test_setSubManagedZonePrefix():
    loadGlobalData()
    assert c.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"]) == True

def test_deleteChildExternalDNSManagedZones():
    loadGlobalData()
    c.setGoogleProjectId(pytest.globalData["googleProjectId"])
    c.setGoogleKubernetesProject()
    c.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    c.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    c.setCurrentDirectory()
    c.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    c.loadGoogleKubernetesServiceAccount()
    c.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"])
    c.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"])
    c.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"])
    c.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"])
    assert c.deleteChildExternalDNSManagedZones() == True

def test_createChildExternalDNSManagedZones():
    loadGlobalData()
    c.setGoogleProjectId(pytest.globalData["googleProjectId"])
    c.setGoogleKubernetesProject()
    c.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    c.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    c.setCurrentDirectory()
    c.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    c.loadGoogleKubernetesServiceAccount()
    c.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"])
    c.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"])
    c.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"])
    c.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"])
    assert c.createChildExternalDNSManagedZones() == True

def test_deleteParentDNSManagedZone():
    loadGlobalData()
    c.setGoogleProjectId(pytest.globalData["googleProjectId"])
    c.setGoogleKubernetesProject()
    c.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    c.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    c.setCurrentDirectory()
    c.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    c.loadGoogleKubernetesServiceAccount()
    c.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"])
    c.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"])
    c.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"])
    c.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"])
    assert c.deleteParentDNSManagedZone() == True

def test_createParentDNSManagedZone():
    loadGlobalData()
    c.setGoogleProjectId(pytest.globalData["googleProjectId"])
    c.setGoogleKubernetesProject()
    c.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    c.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    c.setCurrentDirectory()
    c.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    c.loadGoogleKubernetesServiceAccount()
    c.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"])
    c.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"])
    c.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"])
    c.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"])
    assert c.createParentDNSManagedZone() == True