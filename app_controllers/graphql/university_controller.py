from mongoengine import connect
from bson import ObjectId
from app_schema.schema import schema
from app_models.graphql.models import (
    Application,
    Configuration,
    Credential,
    Category,
    Competency,
    Course,
    Question,
    Report,
    Scope,
    Service,
    Solution,
    Subscription,
    Topic,
    User,
)
import os
from gql import gql, Client
from graphene.test import Client as TestClient
from gql.transport.requests import RequestsHTTPTransport
import sys
import json 

class UniversityController():
    def __init__(self):
        self.mongodbConnection = False
        self.graphqlConnection = False
        self.schema = object
        self.gqlclient = object
        self.mongodbclient = object
        self.applicationId = ""

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

    def setMongodbClient(self):
        try:
            self.mongodbclient = connect("production_securethebox", host="mongodb+srv://"+os.environ["MONGODB_USER"]+":"+os.environ["MONGODB_PASSWORD"]+"@"+os.environ["MONGODB_CLUSTER"], alias="default")
            self.mongodbConnection = True
            return True
        except:
            return False

    def setSchema(self):
        try:
            self.schema = schema
            return True
        except:
            return False
    
    def setGraphqlClient(self):
        try:
            if "pytest" in sys.modules:
                self.gqlclient = TestClient(self.schema)
                self.graphqlConnection = True
                return True
            else:
                self.gqlclient = Client(transport=RequestsHTTPTransport(url='http://localhost:5000/graphql'), schema=self.schema)
                self.graphqlConnection = True
                return True
        except:
            return False

    def createUniversity(self, value):
        try:
            query = gql('''
            mutation createUniversity($domain: String!){
                createUniversity (universityData: {domain : $domain}){
                    university {
                    domain
                    }
                }
            }
            ''')
            expected = {
                "data": {
                    "createUniversity": {
                        "university": {
                            "domain": value
                        }
                    }
                }
            }
            variables = {"domain" : value}
            if "pytest" in sys.modules:
                result = self.gqlclient.execute(query,variables=variables)
                if result == expected:
                    return True
            else:
                result = self.gqlclient.execute(query,variable_values=json.dumps(variables))
                if result == expected:
                    return True
            return False
        except:
            return False

    