import subprocess
import json
import os
from subprocess import check_output
from os import path
import yaml
from kubernetes import client, config
import re
import shutil
from typing import Tuple, List

class KubernetesController():
    def __init__(self): 
        self.currentDirectory = ""
        self.serviceName = ""
        self.userName = ""
        self.kubectlAction = ""
        self.fileName = ""
        self.kubernetesDeploymentImage = ""
        self.kubernetesDeploymentName = ""
        self.googleProjectId = ""
        self.googleKubernetesComputeZone = ""
        self.googleKubernetesComputeCluster = ""
        self.googleKubernetesComputeRegion = ""
        self.googleKubernetesClusterOperationInfo = ""
        self.googleServiceAccountEmail = ""
        self.challengeId = "0000"
        self.challengeGroupId = "1234"
        self.kubernetesPodId = ""

    def setFileName(self, fileName) -> bool:
        try:
            self.fileName = fileName
            return True
        except:
            return False

    def setCurrentDirectory(self) -> bool:
        try:
            self.currentDirectory = os.getcwd()
            return True
        except:
            return False

    def setClusterName(self, clusterName: str) -> bool:
        try:
            self.googleKubernetesComputeCluster = clusterName
            return True
        except:
            return False

    def setServiceName(self, serviceName: str) -> bool:
        try:
            self.serviceName = serviceName
            return True
        except:
            return False

    def setUserName(self, userName: str) -> bool:
        try:
            self.userName = userName
            return True
        except:
            return False

    def setEmailAddress(self, emailAddress: str) -> bool:
        try:
            self.emailAddress = emailAddress
            return True
        except:
            return False

    def setEnvironmentVariable(self, environmentVariable: str) -> bool:
        try:
            if os.getenv(environmentVariable) is not None:
                setattr(self, environmentVariable,
                        os.getenv(environmentVariable))
            else:
                print(f"{environmentVariable} is not set")
                return False
            return True
        except:
            return False

    def setKubernetesDeploymentName(self, kubernetesDeploymentName: str) -> bool:
        self.kubernetesDeploymentName = kubernetesDeploymentName

    def setKubernetesDeploymentImage(self, kubernetesDeploymentImage: str) -> bool:
        self.kubernetesDeploymentImage = kubernetesDeploymentImage

    def setKubernetesPodId(self, kubernetesPodId: str) -> bool:
        try:
            self.kubernetesPodId = kubernetesPodId
            return True
        except:
            return False

    def setKubectlAction(self, kubectlAction: str) -> bool:
        try:
            self.kubectlAction = kubectlAction
            return True
        except:
            return False

    def generateIngressYamlFiles(self) -> bool:
        try:
            fileList = ["01_permissions","02_cluster-role",
                        "03_config", "04_deployment", "05_service", "06_ingress"]
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/{file}"
                subprocess.Popen(
                    [f"python3.7 {fullFilePath}.py {self.googleKubernetesComputeCluster} {self.serviceName} {self.emailAddress}"], shell=True).wait()
                fileCreated = path.exists(
                    f"{fullFilePath}-{self.googleKubernetesComputeCluster}-{self.serviceName}.yml")
                if fileCreated == False:
                    return False
            return True
        except:
            return False

    def generateServiceYamlFiles(self) -> bool:
        try:
            fileList = ["01_cluster-role","01_deployment", "02_service", "03_ingress"]
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/services/{self.serviceName}/{file}"
                subprocess.Popen(
                    [f"python3.7 {fullFilePath}.py {self.googleKubernetesComputeCluster} {self.serviceName} {self.userName}"], shell=True).wait()
                fileCreated = path.exists(
                    f"{fullFilePath}-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml")
                if fileCreated == False:
                    return False
            return True
        except:
            return False

    def generateAuthenticationYamlFiles(self) -> bool:
        try:
            fileList = ["01_deployment", "02_service", "03_ingress"]
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/authentication/{self.serviceName}/{file}"
                subprocess.Popen(
                    [f"python3.7 {fullFilePath}.py {self.googleKubernetesComputeCluster} {self.serviceName} {self.userName} {self.emailAddress} {self.GOOGLE_CLIENT_ID} {self.GOOGLE_CLIENT_SECRET}"], shell=True).wait()
                fileCreated = path.exists(
                    f"{fullFilePath}-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml")
                if fileCreated == False:
                    return False
            return True
        except:
            return False

    def generateStorageYamlFiles(self) -> bool:
        try:
            fileList = ["01_persistent-volume", "02_persistent-volume-claim"]
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/storage/challenges/{file}"
                subprocess.Popen(
                    [f"python3.7 {fullFilePath}.py {self.googleKubernetesComputeCluster} {self.userName} {self.challengeId} {self.challengeGroupId}"], shell=True).wait()
                fileCreated = path.exists(
                    f"{fullFilePath}-{self.userName}.yml")
                if fileCreated == False:
                    return False
            return True
        except:
            return False

    def generateDnsYamlFiles(self) -> bool:
        try:
            fileList = ["01_cluster-role", "02_deployment"]
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/dns/external-dns/{file}"
                subprocess.Popen(
                    [f"python3.7 {fullFilePath}.py {self.googleKubernetesComputeCluster} {self.userName}"], shell=True).wait()
                fileCreated = path.exists(
                    f"{fullFilePath}-external-dns-{self.userName}.yml")
                if fileCreated == False:
                    return False
            return True
        except:
            return False

    def deleteIngressYamlFiles(self) -> bool:
        try:
            fileList = ["01_permissions", "02_cluster-role",
                        "03_config", "04_deployment", "05_service", "06_ingress"]
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/{file}"
                try:
                    subprocess.Popen(
                        [f"rm -rf {fullFilePath}-{self.googleKubernetesComputeCluster}-{self.serviceName}.yml"], shell=True).wait()
                except:
                    continue
                fileCreated = path.exists(
                    f"{fullFilePath}-{self.googleKubernetesComputeCluster}-{self.serviceName}.yml")
                if fileCreated == True:
                    return False
            return True
        except:
            return False

    def deleteServiceYamlFiles(self) -> bool:
        try:
            fileList = ["01_deployment", "02_service", "03_ingress"]
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/services/{self.serviceName}/{file}"
                try:
                    subprocess.Popen(
                        [f"rm -rf {fullFilePath}-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml"], shell=True).wait()
                except:
                    continue
                fileCreated = path.exists(
                    f"{fullFilePath}-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml")
                if fileCreated == True:
                    return False
            return True
        except:
            return False

    def deleteAuthenticationYamlFiles(self) -> bool:
        try:
            fileList = ["01_deployment", "02_service", "03_ingress"]
            currentDirectory = self.currentDirectory
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/authentication/{self.serviceName}/{file}"
                try:
                    subprocess.Popen(
                        [f"rm -rf {fullFilePath}-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml"], shell=True).wait()
                except:
                    continue
                fileCreated = path.exists(
                    f"{fullFilePath}-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml")
                if fileCreated == True:
                    return False
            return True
        except:
            return False

    def deleteDnsYamlFiles(self) -> bool:
        try:
            fileList = ["01_cluster-role", "02_deployment"]
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/dns/external-dns/{file}"
                try:
                    subprocess.Popen(
                        [f"rm -rf {fullFilePath}-external-dns-{self.userName}.yml"], shell=True).wait()
                except:
                    continue
                fileCreated = path.exists(
                    f"{fullFilePath}-external-dns-{self.userName}.yml")
                if fileCreated == True:
                    return False
            return True
        except:
            return False

    def deleteStorageYamlFiles(self) -> bool:
        try:
            fileList = ["01_persistent-volume", "02_persistent-volume-claim"]
            for file in fileList:
                fullFilePath = f"{self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/storage/challenges/{file}"
                try:
                    subprocess.Popen(
                        [f"rm -rf {fullFilePath}-{self.userName}.yml"], shell=True).wait()
                except:
                    continue
                fileCreated = path.exists(
                    f"{fullFilePath}-{self.userName}.yml")
                if fileCreated == True:
                    return False
            return True
        except:
            return False

    def setGoogleProjectId(self, googleProjectId: str) -> bool:
        try:
            self.googleProjectId = googleProjectId
            return True
        except:
            return False

    def setGoogleKubernetesComputeZone(self, googleKubernetesComputeZone: str) -> bool:
        try:
            self.googleKubernetesComputeZone = googleKubernetesComputeZone
            return True
        except:
            return False

    def setGoogleKubernetesComputeCluster(self, googleKubernetesComputeCluster: str) -> bool:
        try:
            self.googleKubernetesComputeCluster = googleKubernetesComputeCluster
            return True
        except:
            return False

    def setGoogleKubernetesComputeRegion(self, googleKubernetesComputeRegion: str) -> bool:
        try:
            self.googleKubernetesComputeRegion = googleKubernetesComputeRegion
            return True
        except:
            return False

    def setGoogleServiceAccountEmail(self, googleServiceAccountEmail: str) -> bool:
        try:
            self.googleServiceAccountEmail = googleServiceAccountEmail
            return True
        except:
            return False

    def loadGoogleKubernetesServiceAccount(self) -> bool:
        try:
            subprocess.Popen(
                [f"gcloud auth activate-service-account --key-file {self.currentDirectory}/secrets/{self.fileName} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"gcloud config set account {self.googleServiceAccountEmail} >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False
    
    def setGoogleKubernetesProject(self) -> bool:
        try:
            subprocess.Popen(
                [f"gcloud config set project {self.googleProjectId} >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False

    def createGoogleKubernetesCluster(self) -> bool:
        try:
            subprocess.Popen(
                [f"gcloud auth activate-service-account --key-file {self.currentDirectory}/secrets/{self.fileName} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"gcloud config set account {self.googleServiceAccountEmail} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud container \
                --project \"{self.googleProjectId}\" clusters create \"{self.googleKubernetesComputeCluster}\" \
                --zone \"{self.googleKubernetesComputeZone}\" \
                --no-enable-basic-auth \
                --cluster-version \"1.14.10-gke.17\" \
                --machine-type \"n1-standard-1\" \
                --image-type \"COS\" \
                --disk-type \"pd-standard\" \
                --disk-size \"50\" \
                --scopes \"https://www.googleapis.com/auth/devstorage.read_only\",\"https://www.googleapis.com/auth/logging.write\",\"https://www.googleapis.com/auth/monitoring\",\"https://www.googleapis.com/auth/servicecontrol\",\"https://www.googleapis.com/auth/service.management.readonly\",\"https://www.googleapis.com/auth/ndev.clouddns.readwrite\",\"https://www.googleapis.com/auth/trace.append\" \
                --num-nodes \"4\" \
                --enable-ip-alias \
                --enable-stackdriver-kubernetes \
                --addons \"HorizontalPodAutoscaling\",\"HttpLoadBalancing\",\"CloudRun\" \
                --network \"projects/{self.googleProjectId}/global/networks/default\" \
                --subnetwork \"projects/{self.googleProjectId}/regions/{self.googleKubernetesComputeRegion}/subnetworks/default\" \
                --default-max-pods-per-node \"8\""], shell=True).wait()
            return True
        except:
            return False

    def getGoogleKubernetesClusterCredentials(self) -> bool:
        try:
            subprocess.Popen(
                [f"gcloud auth activate-service-account --key-file {self.currentDirectory}/secrets/{self.fileName} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"gcloud config set account {self.googleServiceAccountEmail} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"gcloud container clusters get-credentials {self.googleKubernetesComputeCluster} --project {self.googleProjectId} --zone {self.googleKubernetesComputeZone} >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False

    def createClusterRoleBinding(self) -> bool:
        try:
            subprocess.Popen([f"kubectl create clusterrolebinding external-dns --clusterrole=cluster-admin --user=cavalrytacticsinc@gmail.com >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False

    def deleteClusterRoleBinding(self) -> bool:
        try:
            subprocess.Popen([f"kubectl delete clusterrolebinding external-dns >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False

    def deleteGoogleKubernetesCluster(self) -> bool:
        try:
            subprocess.Popen(
                [f"gcloud auth activate-service-account --key-file {self.currentDirectory}/secrets/{self.fileName} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"gcloud config set account {self.googleServiceAccountEmail} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"echo \"y\" | gcloud container clusters delete {self.googleKubernetesComputeCluster} --project {self.googleProjectId} --zone {self.googleKubernetesComputeZone}"], stdout=subprocess.PIPE, shell=True).wait()
            return True
        except:
            return False

    def helper_deleteOrphanObject(self, objectId: str, objectType: str) -> bool:
        print("Deleting:", objectId, objectType)
        if objectType == "firewall-rules":
            subprocess.Popen([f"gcloud compute --project=\"{self.googleProjectId}\" -q firewall-rules delete {objectId}"],shell=True).wait()
        elif objectType == "target-pools":
            subprocess.Popen([f"gcloud compute --project=\"{self.googleProjectId}\" -q target-pools delete {objectId} --region={self.googleKubernetesComputeRegion}"],shell=True).wait()
        elif objectType == "backend-services":
            subprocess.Popen([f"gcloud compute --project=\"{self.googleProjectId}\" -q backend-services delete {objectId} --region={self.googleKubernetesComputeRegion}"],shell=True).wait()
        elif objectType == "forwarding-rules":
            subprocess.Popen([f"gcloud compute --project=\"{self.googleProjectId}\" -q forwarding-rules delete {objectId} --region={self.googleKubernetesComputeRegion}"],shell=True).wait()
        elif objectType == "health-checks":
            subprocess.Popen([f"gcloud compute --project=\"{self.googleProjectId}\" -q health-checks delete {objectId}"],shell=True).wait()
        elif objectType == "addresses":
            subprocess.Popen([f"echo 'y' | gcloud compute --project=\"{self.googleProjectId}\" addresses delete {objectId}"],shell=True).wait()
    
    def helper_checkValidFirewallRule(self, objectId: str) -> bool:
        command = ["gcloud",f"--project=\"{self.googleProjectId}\"","compute","firewall-rules","describe",f"\"{objectId}\"","--format=json"]
        out = check_output(command)
        fw_json=json.loads(out)
        description=fw_json["description"] # $(jq -r .description <<<"$fw_json")
        service_name=fw_json["kubernetes.io/service-name"] # $(jq -r '."kubernetes.io/service-name"' <<<"$description")
        ip=fw_json["kubernetes.io/service-ip"] # $(jq -r '."kubernetes.io/service-ip"' <<<"$description")
        print(f"=> {objectId}, IP: {ip}, Service: {service_name}")
        if ip not in self.activeIps:
            # IP not in use
            return False
        else:
            # IP is in use
            return True
        
    def deleteFirewallRules(self) -> bool:
        try:
            command = ["gcloud",f"--project={self.googleProjectId}","compute","firewall-rules","list","--format=value(name)",f"--filter=name ~ ^k8s"]
            out = check_output(command)
            object_list = out.decode('utf-8')
            object_split_list = object_list.splitlines()
            for objectId in object_split_list:
                self.helper_deleteOrphanObject(objectId, "firewall-rules")
            print(u"\n\n \u001b[48;5;196" + "m " +"IF YOU SEE ERRORS HERE, YOU NEED TO DELETE MANUALLY!\u001b[0m")
            print(f"\nhttps://console.cloud.google.com/networking/firewalls/list?project={self.googleProjectId}&authuser=2&addressesTablesize=50\n")
            return True
        except:
            return False

    def deleteFirewallRulesTest(self) -> bool:
        try:
            command = ["gcloud",f"--project={self.googleProjectId}","compute","firewall-rules","list","--format=value(name)",f"--filter=name ~ ^k8s"]
            out = check_output(command)
            object_list = out.decode('utf-8')
            object_split_list = object_list.splitlines()
            for objectId in object_split_list:
                print(objectId)
                self.helper_checkValidFirewallRule(objectId)
            return True
        except:
            return False

    def deleteStaticIPsStatusReserved(self) -> bool:
        try:
            command = ["gcloud",f"--project={self.googleProjectId}","compute","addresses","list","--format=value(name)","--filter=STATUS ~ ^RESERVED"]
            out = check_output(command)
            object_list = out.decode('utf-8')
            object_split_list = object_list.splitlines()
            for objectId in object_split_list:
                self.helper_deleteOrphanObject(objectId, "addresses")
            print(u"\n\n \u001b[48;5;196" + "m " +"IF YOU SEE ERRORS HERE, YOU NEED TO DELETE MANUALLY!\u001b[0m")
            print(f"\nhttps://console.cloud.google.com/networking/addresses/list?authuser=2&project={self.googleProjectId}&addressesTablesize=50\n")
            return True
        except:
            return False

    def deleteTargetPools(self) -> bool:
        try:
            command = ["gcloud",f"--project={self.googleProjectId}","compute","target-pools","list","--format=value(name)"]
            out = check_output(command)
            object_list = out.decode('utf-8')
            object_split_list = object_list.splitlines()
            for objectId in object_split_list:
                self.helper_deleteOrphanObject(objectId, "forwarding-rules")
                self.helper_deleteOrphanObject(objectId, "target-pools")
                self.helper_deleteOrphanObject(objectId, "health-checks")
            print(u"\n\n \u001b[48;5;21" + "m " +"IF YOU SEE ERRORS HERE, >>>>> FALSE POSITIVE <<<<<\u001b[0m")
            print(f"\nhttps://console.cloud.google.com/net-services/loadbalancing/loadBalancers/list?project={self.googleProjectId}\n")
            return True
        except:
            return False

    def selectGoogleKubernetesClusterContext(self) -> bool:
        try:
            contexts, active_context = config.list_kube_config_contexts()
            if not contexts:
                print("Cannot find any context in kube-config file.")
                return False
            else:
                context = f"gke_{self.googleProjectId}_{self.googleKubernetesComputeZone}_{self.googleKubernetesComputeCluster}"
                config.load_kube_config(context=context)
                subprocess.Popen([f"kubectl config use-context {context}"], stdout=subprocess.PIPE, shell=True).wait()
                return True
        except:
            return False

    def manageKubernetesIngressPod(self) -> bool:
        try:
            subprocess.Popen(
                [f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/01_permissions-{self.googleKubernetesComputeCluster}-{self.serviceName}.yml >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/02_cluster-role-{self.googleKubernetesComputeCluster}-{self.serviceName}.yml >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/03_config-{self.googleKubernetesComputeCluster}-{self.serviceName}.yml >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/04_deployment-{self.googleKubernetesComputeCluster}-{self.serviceName}.yml >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/05_service-{self.googleKubernetesComputeCluster}-{self.serviceName}.yml >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/ingress/{self.serviceName}/06_ingress-{self.googleKubernetesComputeCluster}-{self.serviceName}.yml >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False

    def manageKubernetesStoragePod(self) -> bool:
        try:
            if self.kubectlAction == "apply":
                subprocess.Popen(
                    [f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/storage/challenges/01_persistent-volume-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
                subprocess.Popen(
                    [f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/storage/challenges/02_persistent-volume-claim-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
                return True
            elif self.kubectlAction == "delete":
                subprocess.Popen(
                    [f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/storage/challenges/02_persistent-volume-claim-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
                subprocess.Popen(
                    [f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/storage/challenges/01_persistent-volume-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
                return True
        except:
            return False

    def manageKubernetesServicePod(self) -> bool:
        try:
            subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/services/{self.serviceName}/01_cluster-role-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/services/{self.serviceName}/01_deployment-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/services/{self.serviceName}/02_service-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/services/{self.serviceName}/03_ingress-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False
    
    def manageKubernetesAuthenticationPod(self) -> bool:
        try:
            subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/authentication/{self.serviceName}/01_deployment-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/authentication/{self.serviceName}/02_service-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/authentication/{self.serviceName}/03_ingress-{self.googleKubernetesComputeCluster}-{self.serviceName}-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False

    def manageKubernetesDnsPod(self) -> bool:
        try:
            subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/dns/external-dns/01_cluster-role-{self.serviceName}-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"kubectl {self.kubectlAction} -f {self.currentDirectory}/app_controllers/infrastructure/kubernetes-deployments/dns/external-dns/02_deployment-{self.serviceName}-{self.userName}.yml >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False

    def getKubernetesPodId(self) -> Tuple[bool, str]:
        command = ["kubectl", "get", "pods", "-o", "go-template", "--template",
                   "'{{range .items}}{{.metadata.name}}{{\"\\n\"}}{{end}}'"]
        out = check_output(command)
        pod_list = out.decode("utf-8").replace('\'', '').splitlines()
        pod_id = ''
        findPod = True
        while findPod:
            for i in pod_list:
                if f'{self.serviceName}' in str(i) and f'{self.userName}' in str(i):
                    pod_id = str(i)
                    findPod = False
                    self.kubernetesPodId = pod_id
                    return True, str(pod_id)
            return False, "0"

    def getkubernetesPodStatus(self) ->  Tuple[bool, str]:
        command = ["kubectl", "get", "pod", self.kubernetesPodId, "-o", "json"]
        command_output = check_output(command)
        parsedJSON = json.loads(command_output)
        currentState = parsedJSON["status"]["containerStatuses"][0]["state"]
        for i in currentState:
            if i == "running":
                return True, i
            else:
                return True, i
        return False, "unknown"