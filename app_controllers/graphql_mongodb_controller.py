from mongoengine import connect
from bson import ObjectId
from app_schema.schema import schema
from app_models.graphql.models import Course, Category, Application, Service
import os
from gql import gql, Client
from graphene.test import Client as TestClient
from gql.transport.requests import RequestsHTTPTransport
import sys
import json 

class GraphqlMongodbController():
    def __init__(self):
        self.mongodbConnection = False
        self.graphqlConnection = False
        self.schema = object
        self.gqlclient = object
        self.mongodbclient = object

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

    def addCategory(self,payload):
        try:
            value = payload["value"]
            label = payload["label"]
            color = payload["color"]
            status, output = self.getCategoryByValue(value)
            if len(output) == 0:
                model = Category(value=value, label=label, color=color)
                model.save()
                modelId = model.id
            else:
                modelId = output[0]["node"]["id"]
            return True, modelId
        except:
            return False

    def addService(self,payload):
        try:
            value = payload["value"]
            status, output = self.getServiceByValue(value)
            if len(output) == 0:
                model = Service(value=value)
                model.save()
                modelId = model.id
                
            else:
                modelId = output[0]["node"]["id"]
            return True, modelId
        except:
            return False

    def getAllCategories(self):
        try:
            query = gql('''
            {
                allCategories{
                    edges {
                        node {
                            id,
                            value,
                            label,
                            color
                        }
                    }
                }
            }
            ''')
            output = self.gqlclient.execute(query)
            return True, output["data"]["allCategories"]["edges"]
        except:
            return False

    def getCategoryByValue(self,value):
        try:
            query = gql('''
            query ($value: String!) {
                allCategories (value: $value) {
                    edges {
                        node {
                            id,
                            value,
                            label
                        }
                    }
                }
            }
            ''')
            variables = {"value":value}
            if "pytest" in sys.modules:
                output = self.gqlclient.execute(query,variables=variables)
            else:
                output = self.gqlclient.execute(query,variable_values=json.dumps(variables))
            return True, output["data"]["allCategories"]["edges"]
        except:
            return False

    def getServiceByValue(self,value):
        try:
            query = gql('''
            query ($value: String!) {
                allServices (value: $value) {
                    edges {
                        node {
                            id,
                            value,
                            label
                        }
                    }
                }
            }
            ''')
            variables = {"value":value}
            if "pytest" in sys.modules:
                output = self.gqlclient.execute(query,variables=variables)
            else:
                output = self.gqlclient.execute(query,variable_values=json.dumps(variables))
            return True, output["data"]["allServices"]["edges"]
        except:
            return False

    def getApplicationByValue(self,value):
        try:
            query = gql('''
            query ($value: String!) {
                allApplications (value: $value) {
                    edges {
                        node {
                            id,
                            value,
                            label
                        }
                    }
                }
            }
            ''')
            variables = {"value":value}
            if "pytest" in sys.modules:
                output = self.gqlclient.execute(query,variables=variables)
            else:
                output = self.gqlclient.execute(query,variable_values=json.dumps(variables))
            return True, output["data"]["allApplications"]["edges"]
        except:
            return False

    def getCourseBySlug(self,slug):
        try:
            query = gql('''
            query ($slug: String!) {
                allCourses (slug: $slug) {
                    edges {
                        node {
                            id
                            activeStep
                            description
                            length
                            slug
                            title
                            totalSteps
                            category {
                                label
                                value
                            }
                        }
                    }
                }
            }
            ''')
            variables = {"slug":slug}
            if "pytest" in sys.modules:
                output = self.gqlclient.execute(query,variables=variables)
            else:
                output = self.gqlclient.execute(query,variable_values=json.dumps(variables))
            return True, output
        except:
            return False

    def getAllCourses(self):
        try:
            query = gql('''
            {
                allCourses{
                    edges {
                        node {
                            id
                            title
                            activeStep
                            description
                            length
                            slug
                            totalSteps
                        }
                    }
                }
            }
            ''')
            output = self.gqlclient.execute(query)
            print(output)
            return True, output 
        except:
            return False

    def mutate(self):
        try:
            query = gql('''
            mutation CreateCourse($title: String!, $activeStep: Int!, $description: String!, $length: Int!, $slug: String!, $totalSteps: Int!) {
                createCourse(title: $title, activeStep: $activeStep, description: $description, length: $length, slug: $slug, totalSteps: $totalSteps) {
                    course {
                        title
                        activeStep
                        description
                        length
                        slug
                        totalSteps
                    }
                }
            }
            ''')
            variables = {
                "title": "Blue Team - Security Engineer IC1",
                "activeStep": 0,
                "description": "This challenge is hard!",
                "length": 50,
                "slug": "this-is-slug",
                "totalSteps": 0
            }
        except:
            return False

    def addCourse(self, course_payload):
        title = course_payload["title"]
        activeStep = course_payload["activeStep"]
        description = course_payload["description"]
        length = course_payload["length"]
        slug = course_payload["slug"]
        totalSteps = course_payload["totalSteps"]
        category = course_payload["category"]
        try:
            status, output = self.getCourseBySlug(slug)
            if "pytest" in sys.modules:
                if len(output["data"]["allCourses"]["edges"]) == 0:
                    xcategory = Category(id=0, value="red_team", label="Red team", color="#2196f3")
                    category = xcategory.save()
                    print("CATEGORY:",category)
                    course = Course(title=title, activeStep=activeStep, description=description, length=length, slug=slug, totalSteps=totalSteps, category=category)
                    course.save()
            else:
                xcategory = Category(label="Red team",value="red_team")
                category = xcategory.save()
                print("CATEGORY:",category)
                course = Course(title=title, activeStep=activeStep, description=description, length=length, slug=slug, totalSteps=totalSteps, category=category)
                course.save()
            return True, "good" 
        except:
            return False