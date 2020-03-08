from app_models.rest.academy.categories import Categories
from app_models.rest.academy.category import Category
from app_models.rest.academy.courses import Courses
from app_models.rest.academy.course import Course
from app_models.rest.academy.steps import Steps
from app_models.rest.academy.step import Step
import uuid
import re

class Academy():
    def __init__(self):
        self.categories = Categories()
        self.category = Category()
        self.courses = Courses()
        self.course = Course()
        self.steps = Steps()
        self.step = Step()
        
    def getCourses(self):
        try:
            return True, self.courses.getCourses()
        except:
            return False
    
    def getCourse(self):
        try:
            return True, self.course.to_dict()
        except:
            return False

    def setCourse(self, title, description, categoryValue, courseLength):
        try:
            status, categoryId = self.getCategoryIdFromValue(categoryValue)
            self.course.setCourse(str(uuid.uuid4()),\
                title, \
                self.sanatizeString(title), \
                description, \
                categoryId, \
                courseLength, \
                len(self.steps.getSteps()),\
                0,\
                self.steps.getSteps())
            return True
        except:
            return False

    def addCourse(self):
        try:
            self.courses.addCourse(self.course.to_dict())
            return True
        except:
            return False
    
    def addCourseDict(self, courseDict):
        try:
            self.courses.addCourse(courseDict)
            return True
        except:
            return False
    
    def getCategories(self):
        try:
            return True, self.categories.getCategories()
        except:
            return False
        
    def addCategory(self, value, label, color):
        try:
            self.category.setCategory(len(self.categories.getCategories()), value, label, color)
            self.categories.addCategory(self.category.to_dict())
            return True
        except:
            return False

    def getCategoryIdFromValue(self,categoryValue):
        try:
            status, categories = self.getCategories()
            for index, category in enumerate(categories):
                if category["value"] == categoryValue:
                    return True, categories[index]["id"]
        except:
            return False

    def getSteps(self):
        try:
            return True, self.steps.getSteps()
        except:
            return False
    
    def addStep(self, title, content):
        try:
            self.step.setStep(len(self.steps.getSteps()), title, content)
            self.steps.addStep(self.step.to_dict())
            return True
        except:
            return False  
        
    def sanatizeString(self, someString):
        try:
            newString = " ".join(re.split("[^A-Za-z0-9]+",someString)).replace(" ","-").lower()
            return newString
        except:
            return False

    
category1 = Category()
category2 = Category()
category3 = Category()
category4 = Category()
category1.setCategory(0, "web", "Web", "#3f51b5")
category2.setCategory(1, "aws", "AWS", "#3f51b5")
category3.setCategory(2, "gcp", "GCP", "#3f51b5")
category4.setCategory(3, "cicd", "CI-CD", "#3f51b5")
categories = Categories()
categories.addCategory(category1.to_dict())
categories.addCategory(category2.to_dict())
categories.addCategory(category3.to_dict())
categories.addCategory(category4.to_dict())

course1 = Course()
steps = Steps()
steps.addStep({"id":"1", "title":"Overview", "content":"<h1>1</h1>"})
steps.addStep({"id":"1", "title":"Overview", "content":"<h1>2</h1>"})
course1.setCourse(
    "15459251a6d6b397565",
    "Challenge 1",
    "challenge-1",
    "Defense Scenario",
    "web",
    121,
    11,
    0,
    steps.getSteps())
courses = Courses()
courses.addCourse(course1.to_dict())

def addCourse(course_payload):
    course2 = Course()
    step1 = Steps()
    
    for x in course_payload["steps"]:
        step1.addStep(x)
    
    course2.setCourse(
        str(uuid.uuid4()),
        course_payload["title"],
        course_payload["title"].lower().replace(" ","-"),
        course_payload["description"],
        course_payload["category"],
        course_payload["length"],
        course_payload["totalSteps"],
        course_payload["activeStep"],
        step1.getSteps())
    courses.addCourse(course2.to_dict())


def main():

    return categories.getCategories(), courses.getCourses()
