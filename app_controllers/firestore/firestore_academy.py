import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from app_models.rest.academy.categories import Categories
from app_models.rest.academy.category import Category
from app_models.rest.academy.course import Course
from app_models.rest.academy.courses import Courses
from app_models.rest.academy.step import Step
from app_models.rest.academy.steps import Steps
import sys
import uuid
import os
import subprocess

# Use a service account
# Use a service account
try:
    cred = credentials.Certificate(os.getcwd()+'/secrets/firebase-adminsdk.json')
except:
    currentDirectory = os.getcwd()
    with open(os.getcwd()+"/secrets/travis-openssl-keys","r") as f:
        envList = str(f.readline()).replace("$","").split(",")
        os.chdir(os.getcwd()+"/secrets")
        print(f"openssl aes-256-cbc -K {os.environ[str(envList[0])]} -iv {os.environ[str(envList[1])]} -in secrets.tar.enc -out secrets.tar -d && tar xvf secrets.tar")
        subprocess.Popen([f"openssl aes-256-cbc -K {os.environ[str(envList[0])]} -iv {os.environ[str(envList[1])]} -in secrets.tar.enc -out secrets.tar -d && tar xvf secrets.tar"],shell=True).wait()
        os.chdir(currentDirectory)
        print("SUCCESS",envList)
        cred = credentials.Certificate(os.getcwd()+'/secrets/firebase-adminsdk.json')

firebase_admin.initialize_app(cred)

db = firestore.client()

class FirestoreAcademy():
    def __init__(self):
        self.courses = []
    
    def getCourses(self):
        docs = db.collection(u'academy').stream()
        courses = []
        for doc in docs:
            courses.append(doc.to_dict())
        self.courses = courses
        return self.courses

    def addCourse(self, course_payload):
        _course = Course()
        _steps = Steps()
        
        for x in course_payload["steps"]:
            _steps.addStep(x)
        
        _course.setCourse(
            str(uuid.uuid4()),
            course_payload["title"],
            course_payload["title"].lower().replace(" ","-"),
            course_payload["description"],
            course_payload["category"],
            course_payload["length"],
            course_payload["totalSteps"],
            course_payload["activeStep"],
            _steps.getSteps())
        self.courses.append(_course.to_dict())
        db.collection(u'academy').add(_course.to_dict())