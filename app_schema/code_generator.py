import json
import os
import pytest
from gql_query_builder import GqlQuery
from inspect import getmembers, isfunction, getmodule
import pprint
import subprocess
import shutil

"""

This code is not complete, but the target goal is to generate boilerplate code for mutations

"""

class CodeGenerator():
    def __init__(self):
        self.currentDirectory = ""
        self.queryType = ""   
        self.subject = ""
        self.operationName = ""
        self.fields = []
        self.inputClass = object
        self.subjectMutation = object
        self.selectionSet = {}
        self.inputDict = {}
        self.inputData = []
        self.variableDefinitions = {}
        self.query = ""
        
    def setCurrentDirectory(self):
        try:
            self.currentDirectory = os.getcwd()
            return True
        except:
            return False

    def setQueryType(self, queryType):
        try:
            self.queryType = queryType
            return True
        except:
            return False

    def setSubject(self, subject):
        try:
            self.subject = subject
            return True
        except:
            return False

    def setOperationName(self, operationName):
        try:
            self.operationName = operationName
            return True
        except:
            return False

    def setInputClass(self, inputClass):
        try:
            self.inputClass = inputClass
            return True
        except:
            return False
    
    def setSubjectMutation(self, subjectMutation):
        try:
            self.subjectMutation = subjectMutation
            return True
        except:
            return False

    def setFields(self):
        try:
            # self.fields = [attr for attr in dir(self.inputClass) if not callable(getattr(self.inputClass, attr)) and not attr.startswith("__")]
            for attr in dir(self.inputClass):
                if not attr.startswith("__") and "_" not in attr and "Field" not in attr and "Argument" not in attr:
                    self.fields.append(attr)
            return True
        except:
            return False

    def setSelectionSet(self):
        try:
            for x in self.fields:
                self.selectionSet[x] = "$"+str(x)
            return True
        except:
            return False

    def setInputDict(self):
        try:
            for x in self.fields:
                self.inputDict["$"+str(x)] = "String!"
            return True
        except:
            return False

    def setInputData(self):
        try:
            self.inputData = [attr for attr in dir(self.subjectMutation.Arguments) if not callable(getattr(self.subjectMutation.Arguments, attr)) and not attr.startswith("__")]
            for x in self.inputData:
                if x == "id":
                    pass
                else:
                    self.variableDefinitions[str(x).replace("_data","Data")] = str("$"+x).replace("_data","")
                    if str(x).replace("_data","") == self.subject:
                        self.variableDefinitions[str(x).replace("_data","Data")] = self.selectionSet
                    else:
                        del self.selectionSet[str(x).replace("_data","")]
                        # self.fields.remove(str(x).replace("_data",""))
                    try:
                        del self.variableDefinitions["id"]
                    except:
                        pass
            return True
        except:
            return False

    def setQuery(self):
        try:
            nestedFields = GqlQuery().fields(self.fields, name=self.subject).generate()
            self.query = GqlQuery().fields([nestedFields]).query(self.operationName, input=self.variableDefinitions).operation(self.queryType, name=self.operationName, input=self.inputDict).generate()
            return True
        except:
            return False
    
    def writeFile(self):
        try:
            with open(f"{self.currentDirectory}/app_schema/{self.operationName}.graphql", "w") as f:
                f.write(self.query.replace('\'','').replace("\"",""))
            return True
        except:
            return False

    def copyToFrontend(self, documentsPath):
        try:
            if shutil.which("travis") is None:
                return True
            else:
                subprocess.Popen([f"mv {self.currentDirectory}/app_schema/{self.operationName}.graphql {documentsPath}/{self.queryType}/{self.operationName}.graphql"],shell=True).wait()
            return True
        except:
            return False

    def resetClass(self):
        try: 
            self.subject = ""
            self.operationName = ""
            self.fields = []
            self.inputClass = object
            self.subjectMutation = object
            self.selectionSet = {}
            self.inputDict = {}
            self.inputData = []
            self.variableDefinitions = {}
            self.query = ""
            return True
        except:
            return False

