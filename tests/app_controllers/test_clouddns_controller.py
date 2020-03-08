from app_controllers.clouddns_controller import CloudDnsController
import json
import os
import pytest

pytest.globalData = []

c = CloudDnsController()

def test_loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

def test_setParentDomain():
    assert c.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"]) == True

def test_setSubDomainPrefix():
    assert c.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"]) == True

def test_setParentManagedZone():
    assert c.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"]) == True

def test_setSubManagedZonePrefix():
    assert c.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"]) == True

def test_deleteChildExternalDNSManagedZones():
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