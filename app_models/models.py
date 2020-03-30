from mongoengine import Document
from mongoengine.fields import (
    FloatField,
    StringField,
    ListField,
    URLField,
    ObjectIdField,
    ReferenceField,
    BooleanField,
    EmailField,
    IntField,
    DateTimeField,
    FloatField,
)

class Vulnerability(Document):
    meta = {"collection": "vulnerabilities"}
    ID = ObjectIdField(primary_key=True)
    value = StringField()
    label = StringField()
    type = StringField()
    exploitDbUrl = URLField()

# class Subscription(Document):
#     meta = {"collection": "subscriptions"}
#     ID = ObjectIdField(primary_key=True)
#     stripeCustomerPlan = StringField()
#     stripeCustomerId = StringField()
#     stripeCustomerSubscriptionId = StringField()
#     active = BooleanField()

class Rank(Document):
    meta = {"collection": "ranks"}
    ID = ObjectIdField(primary_key=True)
    coursesComplete = IntField()
    flagsObtained = IntField()
    position = IntField()
    
class User(Document):
    meta = {"collection": "users"}
    ID = ObjectIdField(primary_key=True)
    manager = BooleanField()
    email = EmailField()
    level = IntField()
    rank = ReferenceField(Rank)
    # subscription = ReferenceField(Subscription)
    admin = BooleanField()
    recruiter = BooleanField()
    loggedIn = BooleanField()

class Team(Document):
    meta = {"collection": "teams"}
    ID = ObjectIdField(primary_key=True)
    members = ListField(ReferenceField(User))

class University(Document):
    meta = {"collection": "universities"}
    ID = ObjectIdField(primary_key=True)
    team = ReferenceField(Team)
    domain = StringField()

class Job(Document):
    meta = {"collection": "jobs"}
    ID = ObjectIdField(primary_key=True)
    description = StringField()
    minimumRank = IntField()
    responsibilities = StringField()
    qualifications = StringField()
    applyLink = URLField()
    applyEmail = EmailField()
    payRange = StringField()
    qualified = ListField(ReferenceField(User))

class Company(Document):
    meta = {"collection": "companies"}
    ID = ObjectIdField(primary_key=True)
    managers = ListField(ReferenceField(User))
    jobs = ListField(ReferenceField(Job))

class Credential(Document):
    meta = {"collection": "credentials"}
    ID = ObjectIdField(primary_key=True)
    username = StringField()
    password = StringField()
    publicKey = StringField()
    privateKey = StringField()

class Configuration(Document):
    meta = {"collection": "configurations"}
    ID = ObjectIdField(primary_key=True)
    port = IntField()
    url = URLField()
    credentals = ReferenceField(Credential)

class Competency(Document):
    meta = {"collection": "competencies"}
    ID = ObjectIdField(primary_key=True)
    label = StringField()
    value = StringField()

class Topic(Document):
    meta = {"collection": "topics"}
    ID = ObjectIdField(primary_key=True)
    competency = ReferenceField(Competency)
    label = StringField()
    value = StringField()

class Scope(Document):
    meta = {"collection": "scopes"}
    ID = ObjectIdField(primary_key=True)
    topic = ReferenceField(Topic)
    label = StringField()
    value = StringField()

class Solution(Document):
    meta = {"collection": "solutions"}
    ID = ObjectIdField(primary_key=True)    
    value = StringField()
    label = StringField()

class Submission(Document):
    meta = {"collection": "submissions"}
    ID = ObjectIdField(primary_key=True)
    author = StringField()
    verdict = StringField()
    creationTime = StringField() 
    relativeTime = StringField() 
    points = IntField()
    content = StringField()
    
class Problem(Document):
    meta = {"collection": "problems"}
    ID = ObjectIdField(primary_key=True)
    solutions = ReferenceField(Solution)
    submissions = ReferenceField(Submission)
    scope = ReferenceField(Scope)
    attempts = IntField()
    value = StringField()
    label = StringField()
    instructions = StringField() 
    points = IntField()
    number = IntField()
    startDate = StringField()
    dueDate = StringField()
    rejectDate = StringField()

class Dummy(Document):
    meta = {"collection": "dummies"}
    ID = ObjectIdField(primary_key=True)
    intent = StringField()
    purchases = IntField()
    active = BooleanField()

class Application(Document):
    meta = {"collection": "applications"}
    ID = ObjectIdField(primary_key=True) 
    value = StringField()
    label = StringField()
    version = StringField()
    configuration = ReferenceField(Configuration)
    vulnerability = ListField(ReferenceField(Vulnerability))
    problems = ListField(ReferenceField(Problem))
    dummies = ListField(ReferenceField(Dummy))

class Metric(Document):
    meta = {"collection": "metrics"}
    ID = ObjectIdField(primary_key=True)
    uptime = DateTimeField()
    downtime = DateTimeField()
    activeUsers = IntField()
    purchases = IntField()
    revenue = FloatField()

class Service(Document):
    meta = {"collection": "services"}
    ID = ObjectIdField(primary_key=True)
    value = StringField()
    label = StringField()
    type = StringField()
    applications = ListField(ReferenceField(Application))

class Report(Document):
    meta = {"collection": "reports"}
    ID = ObjectIdField(primary_key=True)
    score = IntField()

class Category(Document):
    meta = {"collection": "categories"}
    ID = ObjectIdField(primary_key=True)
    value = StringField()
    label = StringField()
    color = StringField()
    
class Container(Document):
    meta = {"collection": "containers"}
    ID = ObjectIdField(primary_key=True)
    services = ListField(ReferenceField(Service))
    status = StringField() 

class Cluster(Document):
    meta = {"collection": "clusters"}
    ID = ObjectIdField(primary_key=True)
    value = StringField()
    label = StringField()
    status = StringField()
    containers = ListField(ReferenceField(Container))
    
class Step(Document):
    meta = {"collection": "steps"}
    ID = ObjectIdField(primary_key=True)
    title = StringField()
    content = StringField()

class Course(Document):
    meta = {"collection": "courses"}
    ID = ObjectIdField(primary_key=True)
    title = StringField()
    description = StringField()
    startDate = StringField()
    dueDate = StringField()
    destroyDate = StringField()
    category = ReferenceField(Category)
    cluster = ReferenceField(Cluster)
    report = ReferenceField(Report)