from app_controllers.kubernetes_controller import KubernetesController
import os
import time
kc = KubernetesController()

globalData = {
    "googleProjectId": "securethebox-server",
    "googleKubernetesComputeZone": "us-central1-a",
    "googleKubernetesComputeCluster": "us-central1-a",
    "googleKubernetesComputeRegion": "us-central1",
    "googleKubernetesEngineNamespace": "",
    "googleKubernetesEngineServiceAccountEmail": "stb-kubernetes-engine-sa@securethebox-server.iam.gserviceaccount.com",
    "googleKubernetesEngineServiceAccountFile": "securethebox-server-stb-kubernetes-engine-sa.json",
    "googleCloudRunServiceAccountEmail": "stb-cloud-run-sa@securethebox-client.iam.gserviceaccount.com",
    "googleCloudRunServiceAccountFile": "securethebox-client-stb-cloud-run-sa.json",
    "googleCloudRunProjectId": "securethebox-client",
    "googleCloudRunImageName": "securethebox-server",
    "googleCloudRunRegion": "us-central1",
    "googleCloudRunPlatform": "managed",
    "googleCloudDnsParentDomain": "securethebox.us",
    "googleCloudDnsParentManagedZone": "securethebox-us",
    "googleCloudDnsSubDomainPrefix": "us-central1-a",
    "googleCloudDnsSubManagedZonePrefix": "us-central1-a",
}

class KubernetesManager():
    def __init__(self):
        self.clusterName = ""
        self.userName = ""
        self.action = ""
        self.emailAddress = ""
        self.encryptedEnvironmentVariables = {}
        self.kubernetesDeploymentImage = ""
        self.kubernetesDeploymentName = ""
        self.kubernetesHost = ""
        self.googleProjectId = ""
        self.googleCredentials = ""
        self.googleKubernetesComputeZone = ""
        self.googleKubernetesComputeCluster = ""
        self.googleKubernetesComputeRegion = ""
        self.googleKubernetesClusterOperationInfo = ""
        self.googleServiceAccountEmail = ""
        self.challengeId = "0000"
        self.challengeGroupId = "1234"
        self.kubernetesPodId = ""
    
    def setVariables(self, clusterName: str, userName: str, action: str, emailAddress: str) -> bool:
        try:
            self.clusterName = clusterName
            self.userName = userName
            self.action = action
            self.emailAddress = emailAddress
            return True
        except:
            return False

    def manageKubernetesCluster(self) -> bool:
        try:
            for var in globalData["environmentVariablesList"]:
                kc.setEnvironmentVariable(var)
            kc.setCurrentDirectory()
            kc.setFileName(globalData["googleServiceAccountFile"])
            kc.setGoogleKubernetesComputeRegion(globalData["googleKubernetesComputeRegion"])
            kc.setGoogleKubernetesComputeZone(globalData["googleKubernetesComputeZone"])
            kc.setGoogleProjectId(globalData["googleProjectId"])
            kc.setGoogleServiceAccountEmail(globalData["googleServiceAccountEmail"])
            if self.action == 'apply':
                kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
                kc.selectGoogleKubernetesClusterContext()
                kc.createGoogleKubernetesCluster()
            elif self.action == 'delete':
                kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
                kc.selectGoogleKubernetesClusterContext()
                kc.deleteGoogleKubernetesCluster()
            return True
        except:
            return False

    def manageKubernetesIngress(self) -> bool:
        try:
            for var in globalData["environmentVariablesList"]:
                kc.setEnvironmentVariable(var)
            servicesList = ["traefik"]
            kc.setCurrentDirectory()
            kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
            kc.selectGoogleKubernetesClusterContext()
            kc.setServiceName(servicesList[0])
            kc.setUserName(self.userName)
            kc.setEmailAddress(self.emailAddress)
            kc.setKubectlAction(self.action)
            if self.action == 'apply':
                for service in servicesList:
                    kc.generateIngressYamlFiles()
                    kc.manageKubernetesIngressPod()
            elif self.action == 'delete':
                for service in servicesList:
                    kc.manageKubernetesIngressPod()
                    kc.deleteIngressYamlFiles()
            return True
        except:
            return False

    def manageKubernetesAuthentication(self) -> bool:
        try:
            for var in globalData["environmentVariablesList"]:
                kc.setEnvironmentVariable(var)
            servicesList = ["auth"]
            kc.setCurrentDirectory()
            kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
            kc.selectGoogleKubernetesClusterContext()
            kc.setServiceName(servicesList[0])
            kc.setUserName(self.userName)
            kc.setEmailAddress(self.emailAddress)
            kc.setKubectlAction(self.action)
            if self.action == 'apply':
                for service in servicesList:
                    kc.generateAuthenticationYamlFiles()
                    kc.manageKubernetesAuthenticationPod()
            elif self.action == 'delete':
                for service in servicesList:
                    kc.manageKubernetesAuthenticationPod()
                    kc.deleteAuthenticationYamlFiles()
            return True
        except:
            return False

    def manageKubernetesDns(self) -> bool:
        try:
            for var in globalData["environmentVariablesList"]:
                kc.setEnvironmentVariable(var)
            servicesList = ["external-dns"]
            kc.setCurrentDirectory()
            kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
            kc.selectGoogleKubernetesClusterContext()
            kc.setServiceName(servicesList[0])
            kc.setUserName(self.userName)
            kc.setEmailAddress(self.emailAddress)
            kc.setKubectlAction(self.action)
            if self.action == 'apply':
                for service in servicesList:
                    kc.generateDnsYamlFiles()
                    kc.manageKubernetesDnsPod()
            elif self.action == 'delete':
                for service in servicesList:
                    kc.manageKubernetesDnsPod()
                    kc.deleteDnsYamlFiles()
            return True
        except:
            return False

    def manageKubernetesServices(self) -> bool:
        try:
            for var in globalData["environmentVariablesList"]:
                kc.setEnvironmentVariable(var)
            servicesList = ["securethebox-server","gitlab","jenkins","juice-shop","nginx-modsecurity","splunk","splunk-universal-forwarder"]
            kc.setCurrentDirectory()
            kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
            kc.selectGoogleKubernetesClusterContext()
            kc.setUserName(self.userName)
            kc.setEmailAddress(self.emailAddress)
            kc.setKubectlAction(self.action)
            if self.action == 'apply':
                for service in servicesList:
                    try:
                        kc.setServiceName(service)
                        kc.generateServiceYamlFiles()
                        kc.manageKubernetesServicePod()
                    except:
                        pass
            elif self.action == 'delete':
                for service in servicesList:
                    try:
                        kc.setServiceName(service)
                        kc.manageKubernetesServicePod()
                        kc.deleteServiceYamlFiles()
                    except:
                        pass
            return True
        except:
            return False

    def manageKubernetesStorage(self) -> bool:
        try:
            for var in globalData["environmentVariablesList"]:
                kc.setEnvironmentVariable(var)
            kc.setCurrentDirectory()
            kc.setGoogleKubernetesComputeCluster(globalData["googleKubernetesComputeCluster"])
            kc.selectGoogleKubernetesClusterContext()
            kc.setUserName(self.userName)
            kc.setEmailAddress(self.emailAddress)
            kc.setKubectlAction(self.action)
            if self.action == 'apply':
                try:
                    kc.generateStorageYamlFiles()
                    kc.manageKubernetesStoragePod()
                except:
                    pass
            elif self.action == 'delete':
                try:
                    kc.manageKubernetesStoragePod()
                    kc.deleteStorageYamlFiles()
                except:
                    pass
            return True
        except:
            return False
