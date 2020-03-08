import subprocess
import json
import os
from subprocess import check_output
from os import path
import yaml
from kubernetes import client, config
import re
import shutil
import time

class CloudDnsController():
    def __init__(self):
        self.parentDomain = "securethebox.us"
        self.subDomainPrefix = "us-central1-a"
        self.parentManagedZone = "securethebox-us"
        self.subManagedZonePrefix = "us-central1-a"
        self.firebaseSiteName = "thebox-client"
        self.firebasePrimaryIP = "151.101.1.195"
        self.firebaseSecondaryIP = "151.101.65.195"
        self.fileName = ""
        self.currentDirectory = ""
        self.googleProjectId = ""
        self.googleCredentials = ""
        self.googleKubernetesComputeZone = ""
        self.googleKubernetesComputeCluster = ""
        self.googleKubernetesComputeRegion = ""
        self.googleKubernetesClusterOperationInfo = ""
        self.googleServiceAccountEmail = ""


    def setParentDomain(self,parentDomain):
        try:
            self.parentDomain = parentDomain
            return True
        except:
            return False

    def setSubDomainPrefix(self,subDomainPrefix):
        try:
            self.subDomainPrefix = subDomainPrefix
            return True
        except:
            return False
    
    def setParentManagedZone(self,parentManagedZone):
        try:
            self.parentManagedZone = parentManagedZone
            return True
        except:
            return False

    def setSubManagedZonePrefix(self,subManagedZonePrefix):
        try:
            self.subManagedZonePrefix = subManagedZonePrefix
            return True
        except:
            return False

    def setGoogleProjectId(self, googleProjectId):
        try:
            self.googleProjectId = googleProjectId
            return True
        except:
            return False

    def setGoogleKubernetesProject(self):
        try:
            subprocess.Popen(
                [f"gcloud config set project {self.googleProjectId} >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False

    def setFileName(self, fileName):
        try:
            self.fileName = fileName
            return True
        except:
            return False

    def setCurrentDirectory(self):
        try:
            self.currentDirectory = os.getcwd()
            return True
        except:
            return False

    def setClusterName(self, googleKubernetesComputeCluster):
        try:
            self.googleKubernetesComputeCluster = googleKubernetesComputeCluster
            return True
        except:
            return False

    def setEnvironmentVariable(self, environmentVariable):
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


    def setGoogleKubernetesComputeZone(self, googleKubernetesComputeZone):
        try:
            self.googleKubernetesComputeZone = googleKubernetesComputeZone
            return True
        except:
            return False

    def setGoogleKubernetesComputeCluster(self, googleKubernetesComputeCluster):
        try:
            self.googleKubernetesComputeCluster = googleKubernetesComputeCluster
            return True
        except:
            return False

    def setGoogleKubernetesComputeRegion(self, googleKubernetesComputeRegion):
        try:
            self.googleKubernetesComputeRegion = googleKubernetesComputeRegion
            return True
        except:
            return False

    def setGoogleServiceAccountEmail(self, googleServiceAccountEmail):
        try:
            self.googleServiceAccountEmail = googleServiceAccountEmail
            return True
        except:
            return False

    def loadGoogleKubernetesServiceAccount(self):
        try:
            subprocess.Popen(
                [f"gcloud auth activate-service-account --key-file {self.currentDirectory}/secrets/{self.fileName} >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen(
                [f"gcloud config set account {self.googleServiceAccountEmail} >> /dev/null 2>&1"], shell=True).wait()
            return True
        except:
            return False


    def getGoogleKubernetesClusterCredentials(self):
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

    # This is used for parent root domains only. ie. {self.parentDomain}.
    def createParentDNSManagedZone(self):
        try:
            subprocess.Popen([f"gcloud dns managed-zones create \"{self.parentManagedZone}\" --dns-name \"{self.parentDomain}.\" --description \"Managed by clouddns_controller.py\" >> /dev/null 2>&1"], shell=True).wait()
            command = ["gcloud","dns","record-sets","list","--zone",f"{self.parentManagedZone}","--name",f"{self.parentDomain}.","--type","NS"]
            whileLoop = True
            while whileLoop:                
                out = check_output(command)
                dnsRecord = out.decode("utf-8").splitlines()[1]
                if "ns-cloud-a1" in dnsRecord or "ns-cloud-d1" in dnsRecord:
                    print("FOUND:",dnsRecord)
                    whileLoop = False
                else:
                    print("FAILED:",dnsRecord)
                    subprocess.Popen([f"gcloud dns managed-zones delete {self.parentManagedZone}"], shell=True).wait()
                    subprocess.Popen([f"gcloud dns managed-zones create \"{self.parentManagedZone}\" --dns-name \"{self.parentDomain}.\" --description \"Managed by clouddns_controller.py\""], shell=True).wait()
            
            subprocess.Popen([f"gcloud dns record-sets transaction start --zone \"{self.parentManagedZone}\""], shell=True).wait()
            command2 = ["gcloud","dns","record-sets","list","--zone",f"{self.subManagedZonePrefix}-{self.parentManagedZone}","--name",f"{self.subManagedZonePrefix}.{self.parentDomain}.","--type","NS"]
            out2 = check_output(command2)
            dnsRecord2 = out2.decode("utf-8").splitlines()[1]
            options = ["ns-cloud-a", "ns-cloud-c", "ns-cloud-d", "ns-cloud-e", "ns-cloud-f"]
            for x in options:
                if x in dnsRecord2:
                    subprocess.Popen([f"gcloud dns record-sets transaction add {self.firebasePrimaryIP} {self.firebaseSecondaryIP} --name \"{self.parentDomain}.\" --ttl 300 --type A --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction add {self.firebasePrimaryIP} {self.firebaseSecondaryIP} --name \"www.{self.parentDomain}.\" --ttl 300 --type A --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction add \"v=spf1 include:_spf.firebasemail.com ~all\" \"firebase={self.firebaseSiteName}\" --name \"{self.parentDomain}.\" --ttl 300 --type TXT --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction add \"mail-{self.parentManagedZone}.dkim1._domainkey.firebasemail.com.\" --name \"firebase1._domainkey.{self.parentDomain}\" --ttl 300 --type CNAME --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction add \"mail-{self.parentManagedZone}.dkim2._domainkey.firebasemail.com.\" --name \"firebase2._domainkey.{self.parentDomain}\" --ttl 300 --type CNAME --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction add \"ghs.googlehosted.com.\" --name \"cloud-run.{self.parentDomain}\" --ttl 300 --type CNAME --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction execute --zone \"{self.parentManagedZone}\""], shell=True).wait()
            return True
        except:
            return False

    # This is used for parent root domains only. ie. {self.parentDomain}.
    def deleteParentDNSManagedZone(self):
        try:
            subprocess.Popen([f"gcloud dns record-sets transaction abort --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets transaction start --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets import --zone \"{self.parentManagedZone}\" --delete-all-existing /dev/null >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets transaction execute --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns managed-zones delete {self.parentManagedZone}"], shell=True).wait()
            return True
        except:
            return False

    def addAuthARecordInParentDNSManagedZone(self):
        try:
            command = ["kubectl","get","service/auth","-o","jsonpath='{.status.loadBalancer.ingress[0].ip}'"]
            whileLoop = True
            while whileLoop:     
                try:           
                    out = check_output(command)
                    ipAddress = out.decode("utf-8")
                    authIP = ipAddress.replace('\'','')
                    subprocess.Popen([f"gcloud dns record-sets transaction abort --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction start --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction add {authIP} --name \"auth.{self.parentDomain}.\" --ttl 300 --type A --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction execute --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    whileLoop = False
                    return True
                except:
                    print("Not available")
                    time.sleep(5)
        except:
            return False

    def addChildInParentDNSManagedZone(self):
        subprocess.Popen([f"gcloud dns record-sets transaction start --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
        command = ["gcloud","dns","record-sets","list","--zone",f"{self.subManagedZonePrefix}-{self.parentManagedZone}","--name",f"{self.subManagedZonePrefix}.{self.parentDomain}.","--type","NS"]
        out = check_output(command2)
        dnsRecord = out.decode("utf-8").splitlines()[1]
        options = ["ns-cloud-a", "ns-cloud-b", "ns-cloud-c", "ns-cloud-d", "ns-cloud-e", "ns-cloud-f"]
        for x in options:
            if x in dnsRecord:
                subprocess.Popen([f"gcloud dns record-sets transaction add {x}{{1..4}}.googledomains.com. --name \"{self.subManagedZonePrefix}.{self.parentDomain}.\" --ttl 300 --type NS --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()            
                subprocess.Popen([f"gcloud dns record-sets transaction execute --zone \"{self.parentManagedZone}\""], shell=True).wait()

    def removeChildInParentDNSManagedZone(self):
        subprocess.Popen([f"gcloud dns record-sets transaction start --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
        command = ["gcloud","dns","record-sets","list","--zone",f"{self.subManagedZonePrefix}-{self.parentManagedZone}","--name",f"{self.subManagedZonePrefix}.{self.parentDomain}.","--type","NS"]
        out = check_output(command2)
        dnsRecord = out.decode("utf-8").splitlines()[1]
        options = ["ns-cloud-a", "ns-cloud-b", "ns-cloud-c", "ns-cloud-d", "ns-cloud-e", "ns-cloud-f"]
        for x in options:
            if x in dnsRecord:
                subprocess.Popen([f"gcloud dns record-sets transaction remove {x}{{1..4}}.googledomains.com. --name \"{self.subManagedZonePrefix}.{self.parentDomain}.\" --ttl 300 --type NS --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()            
                subprocess.Popen([f"gcloud dns record-sets transaction execute --zone \"{self.parentManagedZone}\""], shell=True).wait()

    def createChildExternalDNSManagedZones(self):
        try:
            subprocess.Popen([f"gcloud dns managed-zones create \"{self.subManagedZonePrefix}-{self.parentManagedZone}\" --dns-name \"{self.subManagedZonePrefix}.{self.parentDomain}.\" --description \"Automatically managed zone by kubernetes.io/external-dns\""], shell=True).wait()
            return True
        except:
            return False

    def deleteChildExternalDNSManagedZones(self):
        try:
            subprocess.Popen([f"gcloud dns record-sets transaction abort --zone \"{self.subManagedZonePrefix}-{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets transaction start --zone \"{self.subManagedZonePrefix}-{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets import --zone \"{self.subManagedZonePrefix}-{self.parentManagedZone}\" --delete-all-existing /dev/null >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets transaction execute --zone \"{self.subManagedZonePrefix}-{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns managed-zones delete {self.subManagedZonePrefix}-{self.parentManagedZone}"], shell=True).wait()
            return True
        except:
            return False