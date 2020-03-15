import subprocess
import json
import os
from subprocess import check_output
from os import path
import yaml
import re
import shutil
import time
from typing import li

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


    def setParentDomain(self, parentDomain: str) -> bool:
        try:
            self.parentDomain = parentDomain
            return True
        except:
            return False

    def setSubDomainPrefix(self,subDomainPrefix: str) -> bool:
        try:
            self.subDomainPrefix = subDomainPrefix
            return True
        except:
            return False
    
    def setParentManagedZone(self,parentManagedZone: str) -> bool:
        try:
            self.parentManagedZone = parentManagedZone
            return True
        except:
            return False

    def setSubManagedZonePrefix(self,subManagedZonePrefix: str) -> bool:
        try:
            self.subManagedZonePrefix = subManagedZonePrefix
            return True
        except:
            return False

    def setGoogleProjectId(self, googleProjectId: str) -> bool:
        try:
            self.googleProjectId = googleProjectId
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

    def setFileName(self, fileName: str) -> bool:
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

    def setClusterName(self, googleKubernetesComputeCluster: str) -> bool:
        try:
            self.googleKubernetesComputeCluster = googleKubernetesComputeCluster
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

    # This is used for parent root domains only. ie. {self.parentDomain}.
    def createParentDNSManagedZone(self) -> bool:
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
                    subprocess.Popen([f"gcloud dns record-sets transaction add \"v=spf1 include:_spf.firebasemail.com ~all\" \"firebase={self.firebaseSiteName}\" \"google-site-verification=WluXQlQdBJLd7lvro7D6deTbX3gSp5-EczxiFvKpfQk\" --name \"{self.parentDomain}.\" --ttl 300 --type TXT --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction add \"mail-{self.parentManagedZone}.dkim1._domainkey.firebasemail.com.\" --name \"firebase1._domainkey.{self.parentDomain}\" --ttl 300 --type CNAME --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction add \"mail-{self.parentManagedZone}.dkim2._domainkey.firebasemail.com.\" --name \"firebase2._domainkey.{self.parentDomain}\" --ttl 300 --type CNAME --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction add \"ghs.googlehosted.com.\" --name \"cloud-run.{self.parentDomain}\" --ttl 300 --type CNAME --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    subprocess.Popen([f"gcloud dns record-sets transaction execute --zone \"{self.parentManagedZone}\""], shell=True).wait()
            return True
        except:
            return False

    # This is used for parent root domains only. ie. {self.parentDomain}.
    def deleteParentDNSManagedZone(self) -> bool:
        try:
            subprocess.Popen([f"gcloud dns record-sets transaction abort --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets transaction start --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets import --zone \"{self.parentManagedZone}\" --delete-all-existing /dev/null >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets transaction execute --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns managed-zones delete {self.parentManagedZone}"], shell=True).wait()
            return True
        except:
            return False

    def addAuthARecordInParentDNSManagedZone(self) -> bool:
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

    def addChildInParentDNSManagedZone(self) -> bool:
        try:
            subprocess.Popen([f"gcloud dns record-sets transaction start --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            command = ["gcloud","dns","record-sets","list","--zone",f"{self.subManagedZonePrefix}-{self.parentManagedZone}","--name",f"{self.subManagedZonePrefix}.{self.parentDomain}.","--type","NS"]
            out = check_output(command2)
            dnsRecord = out.decode("utf-8").splitlines()[1]
            options = ["ns-cloud-a", "ns-cloud-b", "ns-cloud-c", "ns-cloud-d", "ns-cloud-e", "ns-cloud-f"]
            for x in options:
                if x in dnsRecord:
                    subprocess.Popen([f"gcloud dns record-sets transaction add {x}{{1..4}}.googledomains.com. --name \"{self.subManagedZonePrefix}.{self.parentDomain}.\" --ttl 300 --type NS --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()            
                    subprocess.Popen([f"gcloud dns record-sets transaction execute --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    return True
        except:
            return False

    def removeChildInParentDNSManagedZone(self) -> bool:
        try:
            subprocess.Popen([f"gcloud dns record-sets transaction start --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            command = ["gcloud","dns","record-sets","list","--zone",f"{self.subManagedZonePrefix}-{self.parentManagedZone}","--name",f"{self.subManagedZonePrefix}.{self.parentDomain}.","--type","NS"]
            out = check_output(command2)
            dnsRecord = out.decode("utf-8").splitlines()[1]
            options = ["ns-cloud-a", "ns-cloud-b", "ns-cloud-c", "ns-cloud-d", "ns-cloud-e", "ns-cloud-f"]
            for x in options:
                if x in dnsRecord:
                    subprocess.Popen([f"gcloud dns record-sets transaction remove {x}{{1..4}}.googledomains.com. --name \"{self.subManagedZonePrefix}.{self.parentDomain}.\" --ttl 300 --type NS --zone \"{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()            
                    subprocess.Popen([f"gcloud dns record-sets transaction execute --zone \"{self.parentManagedZone}\""], shell=True).wait()
                    return True
        except:
            return False

    def createChildExternalDNSManagedZones(self) -> bool:
        try:
            subprocess.Popen([f"gcloud dns managed-zones create \"{self.subManagedZonePrefix}-{self.parentManagedZone}\" --dns-name \"{self.subManagedZonePrefix}.{self.parentDomain}.\" --description \"Automatically managed zone by kubernetes.io/external-dns\""], shell=True).wait()
            return True
        except:
            return False

    def deleteChildExternalDNSManagedZones(self) -> bool:
        try:
            subprocess.Popen([f"gcloud dns record-sets transaction abort --zone \"{self.subManagedZonePrefix}-{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets transaction start --zone \"{self.subManagedZonePrefix}-{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets import --zone \"{self.subManagedZonePrefix}-{self.parentManagedZone}\" --delete-all-existing /dev/null >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns record-sets transaction execute --zone \"{self.subManagedZonePrefix}-{self.parentManagedZone}\" >> /dev/null 2>&1"], shell=True).wait()
            subprocess.Popen([f"gcloud dns managed-zones delete {self.subManagedZonePrefix}-{self.parentManagedZone}"], shell=True).wait()
            return True
        except:
            return False