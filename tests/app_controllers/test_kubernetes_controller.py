from app_controllers.kubernetes_controller import KubernetesController
from app_controllers.clouddns_controller import CloudDnsController
import json
import os
import pytest
import time

pytest.globalData = []

c = KubernetesController()
x = CloudDnsController()

def loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

def test_loadGlobalData():
    with open(str(os.getcwd())+"/tests/globalData.json", "r") as f:
        pytest.globalData = json.load(f)

# ##############################################################################

# #              COMMENT ALL BELOW TO NOT APPLY DEPLOYMENT

# ##############################################################################

def test_setEnvironmentVariables():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        assert c.setEnvironmentVariable(var) == True

def test_setCurrentDirectory():
    loadGlobalData()
    assert c.setCurrentDirectory() == True

def test_setFileName():
    loadGlobalData()
    for file in pytest.globalData["unencryptedFileNames"]:
        assert c.setFileName(file) == True

def test_setGoogleKubernetesComputeCluster():
    loadGlobalData()
    assert c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"]) == True

def test_setServiceName():
    loadGlobalData()
    assert c.setServiceName(pytest.globalData["serviceName_service"]) == True

def test_setUserName():
    loadGlobalData()
    assert c.setUserName(pytest.globalData["userName"]) == True

def test_setEmailAddress():
    loadGlobalData()
    assert c.setEmailAddress(pytest.globalData["emailAddress"]) == True

def test_setKubernetesPodId():
    loadGlobalData()
    assert c.setKubernetesPodId(pytest.globalData["kubernetesPodId"]) == True

def test_setKubectlAction():
    loadGlobalData()
    assert c.setKubectlAction(pytest.globalData["kubectlAction_apply"]) == True
    assert c.setKubectlAction(pytest.globalData["kubectlAction_delete"]) == True

def test_generateIngressYamlFiles():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.setServiceName(pytest.globalData["serviceName_ingress"])
    c.setUserName(pytest.globalData["userName"])
    c.setEmailAddress(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    assert c.generateIngressYamlFiles() == True

def test_generateServiceYamlFiles():
    loadGlobalData()
    c.setCurrentDirectory()
    for service in pytest.globalData["serviceName_service"]:
        c.setServiceName(service)
        c.setUserName(pytest.globalData["userName"])
        c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
        assert c.generateServiceYamlFiles() == True

def test_generateAuthenticationYamlFiles():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.setServiceName(pytest.globalData["serviceName_authentication"])
    c.setUserName(pytest.globalData["userName"])
    c.setEmailAddress(pytest.globalData["emailAddress"])
    for var in pytest.globalData["environmentVariablesList"]:
        assert c.setEnvironmentVariable(var) == True
    assert c.generateAuthenticationYamlFiles() == True

def test_generateDnsYamlFiles():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.setServiceName(pytest.globalData["serviceName_dns"])
    c.setUserName(pytest.globalData["userName"])
    c.setEmailAddress(pytest.globalData["emailAddress"])
    for var in pytest.globalData["environmentVariablesList"]:
        assert c.setEnvironmentVariable(var) == True
    assert c.generateDnsYamlFiles() == True

def test_generateStorageYamlFiles():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setUserName(pytest.globalData["userName"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert c.generateStorageYamlFiles() == True

def test_setGoogleProjectId():
    loadGlobalData()
    assert c.setGoogleProjectId(pytest.globalData["googleProjectId"]) == True

def test_setGoogleKubernetesComputeZone():
    loadGlobalData()
    assert c.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"]) == True

def test_setGoogleKubernetesComputeCluster():
    loadGlobalData()
    assert c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"]) == True

def test_setGoogleKubernetesComputeRegion():
    loadGlobalData()
    assert c.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"]) == True

def test_setGoogleServiceAccountEmail():
    loadGlobalData()
    assert c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"]) == True

def test_loadGoogleKubernetesServiceAccount():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    assert c.loadGoogleKubernetesServiceAccount() == True

def test_setGoogleKubernetesProject():
    loadGlobalData()
    c.setGoogleProjectId(pytest.globalData["googleProjectId"])
    assert c.setGoogleKubernetesProject() == True

def test_deleteChildExternalDNSManagedZones():
    loadGlobalData()
    x.setGoogleProjectId(pytest.globalData["googleProjectId"])
    x.setGoogleKubernetesProject()
    x.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    x.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    x.setCurrentDirectory()
    x.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    x.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    x.loadGoogleKubernetesServiceAccount() 
    x.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"])
    x.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"])
    x.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"])
    x.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"])
    assert x.deleteChildExternalDNSManagedZones() == True

def test_createChildExternalDNSManagedZones():
    loadGlobalData()
    x.setGoogleProjectId(pytest.globalData["googleProjectId"])
    x.setGoogleKubernetesProject()
    x.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    x.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    x.setCurrentDirectory()
    x.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    x.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    x.loadGoogleKubernetesServiceAccount() 
    x.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"])
    x.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"])
    x.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"])
    x.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"])
    assert x.createChildExternalDNSManagedZones() == True

def test_deleteParentDNSManagedZone():
    loadGlobalData()
    x.setGoogleProjectId(pytest.globalData["googleProjectId"])
    x.setGoogleKubernetesProject()
    x.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    x.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    x.setCurrentDirectory()
    x.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    x.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    x.loadGoogleKubernetesServiceAccount() 
    x.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"])
    x.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"])
    x.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"])
    x.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"])
    assert x.deleteParentDNSManagedZone() == True

def test_createParentDNSManagedZone():
    loadGlobalData()
    x.setGoogleProjectId(pytest.globalData["googleProjectId"])
    x.setGoogleKubernetesProject()
    x.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    x.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    x.setCurrentDirectory()
    x.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    x.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    x.loadGoogleKubernetesServiceAccount()
    x.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"])
    x.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"])
    x.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"])
    x.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"])
    assert x.createParentDNSManagedZone() == True

def test_createGoogleKubernetesCluster():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    c.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    c.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    c.setGoogleProjectId(pytest.globalData["googleProjectId"])
    c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert c.createGoogleKubernetesCluster() == True

def test_getGoogleKubernetesClusterCredentials():
    loadGlobalData()
    c.setCurrentDirectory()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    c.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    assert c.getGoogleKubernetesClusterCredentials() == True

def test_createClusterRoleBinding():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    c.setServiceName(pytest.globalData["serviceName_dns"])
    c.setUserName(pytest.globalData["userName"])
    c.setKubectlAction(pytest.globalData["kubectlAction_apply"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.setEmailAddress(pytest.globalData["emailAddress"])
    assert c.createClusterRoleBinding() == True

def test_manageKubernetesAuthenticationPod_apply():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    c.setServiceName(pytest.globalData["serviceName_authentication"])
    c.setUserName(pytest.globalData["userName"])
    c.setKubectlAction(pytest.globalData["kubectlAction_apply"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert c.manageKubernetesAuthenticationPod() == True

def test_manageKubernetesDnsPod_apply():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    c.setServiceName(pytest.globalData["serviceName_dns"])
    c.setUserName(pytest.globalData["userName"])
    c.setKubectlAction(pytest.globalData["kubectlAction_apply"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert c.manageKubernetesDnsPod() == True

def test_manageKubernetesIngressPod_apply():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    c.setServiceName(pytest.globalData["serviceName_ingress"])
    c.setKubectlAction(pytest.globalData["kubectlAction_apply"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.selectGoogleKubernetesClusterContext()
    assert c.manageKubernetesIngressPod() == True

def test_manageKubernetesStoragePod_apply():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    c.setUserName(pytest.globalData["userName"])
    c.setKubectlAction(pytest.globalData["kubectlAction_apply"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert c.manageKubernetesStoragePod() == True

def test_manageKubernetesServicePod_apply():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    for service in pytest.globalData["serviceName_service"]:
        c.setServiceName(service)
        c.setUserName(pytest.globalData["userName"])
        c.setKubectlAction(pytest.globalData["kubectlAction_apply"])
        c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
        assert c.manageKubernetesServicePod() == True

def test_getKubernetesPodId():
    loadGlobalData()
    for x in range(30):
        time.sleep(1)
        print(x)
    c.setUserName(pytest.globalData["userName"])
    for service in pytest.globalData["serviceName_service"]:
        c.setServiceName(service)
        value, podId = c.getKubernetesPodId()
        assert value == True
        assert podId != "0"

def test_getKubernetesPodStatus():
    loadGlobalData()
    c.setUserName(pytest.globalData["userName"])
    for service in pytest.globalData["serviceName_service"]:
        c.setServiceName(service)
        value, podId = c.getKubernetesPodId()
        c.setKubernetesPodId(podId)
        value, podStatus = c.getkubernetesPodStatus()
        assert value == True

def test_addAuthARecordInParentDNSManagedZone():
    loadGlobalData()
    x.setGoogleProjectId(pytest.globalData["googleProjectId"])
    x.setGoogleKubernetesProject()
    x.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    x.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    x.setCurrentDirectory()
    x.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    x.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    x.loadGoogleKubernetesServiceAccount() 
    x.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"])
    x.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"])
    x.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"])
    x.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"])
    assert x.addAuthARecordInParentDNSManagedZone() == True

# ##############################################################################

# #              COMMENT ALL BELOW TO NOT DELETE DEPLOYMENT

# ##############################################################################

def test_manageKubernetesServicePod_delete():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    for service in pytest.globalData["serviceName_service"]:
        c.setServiceName(service)
        c.setUserName(pytest.globalData["userName"])
        c.setKubectlAction(pytest.globalData["kubectlAction_delete"])
        c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
        assert c.manageKubernetesServicePod() == True

def test_manageKubernetesAuthenticationPod_delete():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    c.setServiceName(pytest.globalData["serviceName_authentication"])
    c.setUserName(pytest.globalData["userName"])
    c.setKubectlAction(pytest.globalData["kubectlAction_delete"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert c.manageKubernetesAuthenticationPod() == True

def test_manageKubernetesStoragePod_delete():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    c.setUserName(pytest.globalData["userName"])
    c.setKubectlAction(pytest.globalData["kubectlAction_delete"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert c.manageKubernetesStoragePod() == True

def test_manageKubernetesIngressPod_delete():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    c.setServiceName(pytest.globalData["serviceName_ingress"])
    c.setKubectlAction(pytest.globalData["kubectlAction_delete"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.selectGoogleKubernetesClusterContext()
    assert c.manageKubernetesIngressPod() == True

def test_manageKubernetesDnsPod_delete():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    c.setServiceName(pytest.globalData["serviceName_dns"])
    c.setUserName(pytest.globalData["userName"])
    c.setKubectlAction(pytest.globalData["kubectlAction_delete"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert c.manageKubernetesDnsPod() == True

def test_deleteClusterRoleBinding():
    loadGlobalData()
    for var in pytest.globalData["environmentVariablesList"]:
        c.setEnvironmentVariable(var)
    c.setCurrentDirectory()
    c.setServiceName(pytest.globalData["serviceName_dns"])
    c.setUserName(pytest.globalData["userName"])
    c.setKubectlAction(pytest.globalData["kubectlAction_apply"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    assert c.deleteClusterRoleBinding() == True

def test_deleteGoogleKubernetesCluster():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    c.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    c.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    c.setGoogleProjectId(pytest.globalData["googleProjectId"])
    c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.selectGoogleKubernetesClusterContext()
    assert c.deleteGoogleKubernetesCluster() == True

def test_deleteIngressYamlFiles():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.setServiceName(pytest.globalData["serviceName_ingress"])
    c.setUserName(pytest.globalData["userName"])
    assert c.deleteIngressYamlFiles() == True

def test_deleteServiceYamlFiles():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    for service in pytest.globalData["serviceName_service"]:
        c.setServiceName(service)
        c.setUserName(pytest.globalData["userName"])
        assert c.deleteServiceYamlFiles() == True

def test_deleteAuthenticationYamlFiles():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.setServiceName(pytest.globalData["serviceName_authentication"])
    c.setUserName(pytest.globalData["userName"])
    assert c.deleteAuthenticationYamlFiles() == True
    
def test_deleteDnsYamlFiles():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.setServiceName(pytest.globalData["serviceName_dns"])
    c.setUserName(pytest.globalData["userName"])
    assert c.deleteDnsYamlFiles() == True

def test_deleteStorageYamlFiles():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.setUserName(pytest.globalData["userName"])
    assert c.deleteStorageYamlFiles() == True

def test_deleteFirewallRules():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    c.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    c.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    c.setGoogleProjectId(pytest.globalData["googleProjectId"])
    c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.selectGoogleKubernetesClusterContext()
    c.getGoogleKubernetesClusterCredentials()
    assert c.deleteFirewallRules() == True

def test_deleteStaticIPsStatusReserved():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    c.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    c.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    c.setGoogleProjectId(pytest.globalData["googleProjectId"])
    c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.selectGoogleKubernetesClusterContext()
    c.getGoogleKubernetesClusterCredentials()
    assert c.deleteStaticIPsStatusReserved() == True

def test_deleteTargetPools():
    loadGlobalData()
    c.setCurrentDirectory()
    c.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    c.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    c.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    c.setGoogleProjectId(pytest.globalData["googleProjectId"])
    c.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    c.setGoogleKubernetesComputeCluster(pytest.globalData["googleKubernetesComputeCluster"])
    c.selectGoogleKubernetesClusterContext()
    c.getGoogleKubernetesClusterCredentials()
    assert c.deleteTargetPools() == True

def test_deleteChildExternalDNSManagedZones():
    loadGlobalData()
    x.setGoogleProjectId(pytest.globalData["googleProjectId"])
    x.setGoogleKubernetesProject()
    x.setGoogleKubernetesComputeRegion(pytest.globalData["googleKubernetesComputeRegion"])
    x.setGoogleKubernetesComputeZone(pytest.globalData["googleKubernetesComputeZone"])
    x.setCurrentDirectory()
    x.setFileName(pytest.globalData["googleKubernetesEngineServiceAccountFile"])
    x.setGoogleServiceAccountEmail(pytest.globalData["googleKubernetesEngineServiceAccountEmail"])
    x.loadGoogleKubernetesServiceAccount() 
    x.setParentDomain(pytest.globalData["googleCloudDnsParentDomain"])
    x.setSubDomainPrefix(pytest.globalData["googleCloudDnsSubDomainPrefix"])
    x.setParentManagedZone(pytest.globalData["googleCloudDnsParentManagedZone"])
    x.setSubManagedZonePrefix(pytest.globalData["googleCloudDnsSubManagedZonePrefix"])
    assert x.deleteChildExternalDNSManagedZones() == True