import subprocess
import os
from os import path
"""

IAM Permissions:
Cloud Run Admin
Cloud Run Service Agent
Storage Admin
*Enable Domain Wide Delegation (Allows Service Account Requests)

"""

class CloudRunController():
    def __init__(self):
        self.currentDirectory = ""
        self.fileName = ""
        self.serviceAccountEmailAddress = ""
        self.projectId = ""
        self.imageName = ""
        self.region = ""
        self.platform = ""

    def setCurrentDirectory(self):
        try:
            self.currentDirectory = os.getcwd()
            return True
        except:
            return False

    def setFileName(self, fileName):
        try:
            self.fileName = fileName
            return True
        except:
            return False

    def setServiceAccountEmailAddress(self, serviceAccountEmailAddress):
        try:
            self.serviceAccountEmailAddress = serviceAccountEmailAddress
            return True
        except:
            return False

    def setProjectId(self, projectId):
        try:
            self.projectId = projectId
            return True
        except:
            return False

    def setImageName(self, imageName):
        try:
            self.imageName = imageName
            return True
        except:
            return False

    def setRegion(self, region):
        try:
            self.region = region
            subprocess.Popen([f"gcloud config set run/region {self.region}"],shell=True).wait()
            return True
        except:
            return False

    def setPlatform(self,platform):
        try:
            self.platform = platform
            subprocess.Popen([f"gcloud config set run/platform {self.platform}"],shell=True).wait()
            return True
        except:
            return False
        

    def setDockerSources(self):
        try:
            subprocess.Popen([f"echo 'y' | gcloud auth configure-docker"],shell=True).wait()
            subprocess.Popen([f"echo 'y' | gcloud components install docker-credential-gcr"],shell=True).wait()
            return True
        except:
            return False
        
    def setAccount(self):
        try:
            subprocess.Popen([f"gcloud auth activate-service-account --key-file {self.currentDirectory}/secrets/{self.fileName}"],shell=True).wait()
            subprocess.Popen([f"gcloud config set project {self.projectId}"],shell=True).wait()
            subprocess.Popen([f"gcloud config set account {self.serviceAccountEmailAddress}"],shell=True).wait()
            return True
        except:
            return False

    def buildImage(self):
        try:
            fileExists = path.exists(self.currentDirectory+"/secrets/travis-openssl-keys-values.txt")
            # For Local Deploy
            if fileExists == True:
                with open(self.currentDirectory+"/secrets/travis-openssl-keys-values.txt","r") as f:
                    env = str(f.readline()).replace("$","")
                    variables = env.split(",")
                    key = variables[0].split("=")[1]
                    iv = variables[1].split("=")[1]
                    subprocess.Popen([f"docker build . --build-arg key={key} --build-arg iv={iv} --tag gcr.io/{self.projectId}/{self.imageName}"],shell=True).wait()
            # For Travis Deploy
            else:
                with open(self.currentDirectory+"/secrets/travis-openssl-keys","r") as f:
                    envList = str(f.readline()).replace("$","")
                    slist = envList.split(",")
                    l = []
                    for line in slist:
                        l.append(line+"="+str(os.environ[str(line)]))
                    concatList = ",".join(l)
                    variables = concatList.split(",")
                    key = variables[0].split("=")[1]
                    iv = variables[1].split("=")[1]
                    subprocess.Popen([f"docker build . -build-arg key={key} --build-arg iv={iv} --tag gcr.io/{self.projectId}/{self.imageName}"],shell=True).wait()
            return True
            
            return True
        except:
            return False
        
    def pushImage(self):
        try:
            subprocess.Popen([f"docker push gcr.io/{self.projectId}/{self.imageName}"],shell=True).wait()
            return True
        except:
            return False
        

    def deployImage(self):
        try:
            fileExists = path.exists(self.currentDirectory+"/secrets/travis-openssl-keys-values.txt")
            # For Local Deploy
            if fileExists == True:
                with open(self.currentDirectory+"/secrets/travis-openssl-keys-values.txt","r") as f:
                    env = str(f.readline()).replace("$","")
                    subprocess.Popen([f"gcloud run deploy securethebox-server --image gcr.io/{self.projectId}/{self.imageName} --update-env-vars {env} --region {self.region}"],shell=True).wait()
            # For Travis Deploy
            else:
                with open(self.currentDirectory+"/secrets/travis-openssl-keys","r") as f:
                    envList = str(f.readline()).replace("$","")
                    slist = envList.split(",")
                    l = []
                    for line in slist:
                        l.append(line+"="+str(os.environ[str(line)]))
                    concatList = ",".join(l)
                    subprocess.Popen([f"gcloud run deploy securethebox-server --image gcr.io/{self.projectId}/{self.imageName} --update-env-vars {concatList} --region {self.region}"],shell=True).wait()
            return True
        except:
            return False