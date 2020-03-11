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

class Subscription(Document):
    meta = {"collection": "subscriptions"}
    ID = ObjectIdField()
    stripeCustomerPlan = StringField()
    stripeCustomerId = StringField()
    stripeCustomerSubscriptionId = StringField()
    active = BooleanField()

class Rank(Document):
    meta = {"collection": "ranks"}
    ID = ObjectIdField()
    coursesComplete = IntField()
    flagsObtained = IntField()
    position = IntField()
    
class User(Document):
    meta = {"collection": "users"}
    ID = ObjectIdField()
    manager = BooleanField()
    email = EmailField()
    level = IntField()
    rank = ReferenceField(Rank)
    subscription = ReferenceField(Subscription)
    admin = BooleanField()
    recruiter = BooleanField()
    loggedIn = BooleanField()

class Team(Document):
    meta = {"collection": "teams"}
    ID = ObjectIdField()
    members = ListField(ReferenceField(User))

class University(Document):
    meta = {"collection": "universities"}
    ID = ObjectIdField()
    team = ReferenceField(Team)
    domain = StringField()

class Job(Document):
    meta = {"collection": "jobs"}
    ID = ObjectIdField()
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
    ID = ObjectIdField()
    managers = ListField(ReferenceField(User))
    jobs = ListField(ReferenceField(Job))

class Credential(Document):
    meta = {"collection": "credentials"}
    ID = ObjectIdField()
    username = StringField()
    password = StringField()
    publicKey = StringField()
    privateKey = StringField()

class Configuration(Document):
    meta = {"collection": "configurations"}
    ID = ObjectIdField()
    port = IntField()
    url = URLField()
    credentals = ReferenceField(Credential)

class Competency(Document):
    meta = {"collection": "competencies"}
    ID = ObjectIdField()
    label = StringField()
    value = StringField()

class Topic(Document):
    meta = {"collection": "topics"}
    ID = ObjectIdField()
    competency = ReferenceField(Competency)
    label = StringField()
    value = StringField()

class Scope(Document):
    meta = {"collection": "scopes"}
    ID = ObjectIdField()
    topic = ReferenceField(Topic)
    label = StringField()
    value = StringField()

class Solution(Document):
    meta = {"collection": "solutions"}
    ID = ObjectIdField()    
    value = StringField()

class Question(Document):
    meta = {"collection": "questions"}
    ID = ObjectIdField()
    solutions = ReferenceField(Solution)
    scope = ReferenceField(Scope)
    attempts = IntField()
    value = StringField()

class Dummy(Document):
    meta = {"collection": "dummies"}
    ID = ObjectIdField()
    intent = StringField()
    purchases = IntField()
    active = BooleanField()

class Application(Document):
    meta = {"collection": "applications"}
    ID = ObjectIdField()
    name = StringField()
    label = StringField()
    version = StringField()
    configuration = ReferenceField(Configuration)
    questions = ListField(ReferenceField(Question))
    dummies = ListField(ReferenceField(Dummy))

class Metric(Document):
    meta = {"collection": "metrics"}
    ID = ObjectIdField()
    uptime = DateTimeField()
    downtime = DateTimeField()
    activeUsers = IntField()
    purchases = IntField()
    revenue = FloatField()

class Service(Document):
    meta = {"collection": "services"}
    ID = ObjectIdField()
    value = StringField()
    label = StringField()
    type = StringField()
    applications = ListField(ReferenceField(Application))

class Report(Document):
    meta = {"collection": "reports"}
    ID = ObjectIdField()
    score = IntField()

class Category(Document):
    meta = {"collection": "categories"}
    ID = ObjectIdField()
    value = StringField()
    label = StringField()
    color = StringField()
    
class Container(Document):
    meta = {"collection": "containers"}
    ID = ObjectIdField()
    services = ListField(ReferenceField(Service))
    status = StringField() 

class Cluster(Document):
    meta = {"collection": "clusters"}
    ID = ObjectIdField()
    value = StringField()
    label = StringField()
    status = StringField()
    containers = ListField(ReferenceField(Container))

class Step(Document):
    meta = {"collection": "steps"}
    ID = ObjectIdField()
    title = StringField()
    content = StringField()

class Course(Document):
    meta = {"collection": "courses"}
    ID = ObjectIdField()
    activeStep = IntField()
    description = StringField()
    length = IntField()
    slug = StringField()
    title = StringField()
    totalSteps = IntField()
    category = ReferenceField(Category)
    report = ReferenceField(Report)
    cluster = ReferenceField(Cluster)
    status = StringField()
    steps = ListField(ReferenceField(Step))