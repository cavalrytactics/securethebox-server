from graphene import relay
from graphene_mongo import MongoengineObjectType
from app_models.models import (
    Application, 
    Category, 
	Cluster,
	Company,
    Competency, 
	Container,
    Configuration, 
	Course, 
	Credential, 
	Dummy,
	Job,
	Metric,
    Problem,
	Rank,
    Report, 
    Scope, 
    Service, 
    Solution, 
	Step,
    Subscription, 
	Team,
    Topic, 
	University,
    User,
	Vulnerability)

class ApplicationType(MongoengineObjectType):
	class Meta:
		model = Application
		interfaces = (relay.Node,)
class CategoryType(MongoengineObjectType):
	class Meta:
		model = Category
		interfaces = (relay.Node,)
class ClusterType(MongoengineObjectType):
	class Meta:
		model = Cluster
		interfaces = (relay.Node,)
class CompanyType(MongoengineObjectType):
	class Meta:
		model = Company
		interfaces = (relay.Node,)
class ConfigurationType(MongoengineObjectType):
	class Meta:
		model = Configuration
		interfaces = (relay.Node,)
class CredentialType(MongoengineObjectType):
	class Meta:
		model = Credential
		interfaces = (relay.Node,)
class CompetencyType(MongoengineObjectType):
	class Meta:
		model = Competency
		interfaces = (relay.Node,)
class ContainerType(MongoengineObjectType):
	class Meta:
		model = Container
		interfaces = (relay.Node,)
class CourseType(MongoengineObjectType):
	class Meta:
		model = Course
		interfaces = (relay.Node,)
class DummyType(MongoengineObjectType):
	class Meta:
		model = Dummy
		interfaces = (relay.Node,)
class JobType(MongoengineObjectType):
	class Meta:
		model = Job
		interfaces = (relay.Node,)
class MetricType(MongoengineObjectType):
	class Meta:
		model = Metric
		interfaces = (relay.Node,)
class ProblemType(MongoengineObjectType):
	class Meta:
		model = Problem
		interfaces = (relay.Node,)
class RankType(MongoengineObjectType):
	class Meta:
		model = Rank
		interfaces = (relay.Node,)
class ReportType(MongoengineObjectType):
	class Meta:
		model = Report
		interfaces = (relay.Node,)
class ScopeType(MongoengineObjectType):
	class Meta:
		model = Scope
		interfaces = (relay.Node,)
class ServiceType(MongoengineObjectType):
	class Meta:
		model = Service
		interfaces = (relay.Node,)
class SolutionType(MongoengineObjectType):
	class Meta:
		model = Solution
		interfaces = (relay.Node,)
class StepType(MongoengineObjectType):
	class Meta:
		model = Step
		interfaces = (relay.Node,)
class SubscriptionType(MongoengineObjectType):
	class Meta:
		model = Subscription
		interfaces = (relay.Node,)
class TeamType(MongoengineObjectType):
	class Meta:
		model = Team
		interfaces = (relay.Node,)
class TopicType(MongoengineObjectType):
	class Meta:
		model = Topic
		interfaces = (relay.Node,)
class UniversityType(MongoengineObjectType):
	class Meta:
		model = University
		interfaces = (relay.Node,)
class UserType(MongoengineObjectType):
	class Meta:
		model = User
		interfaces = (relay.Node,)
class VulnerabilityType(MongoengineObjectType):
	class Meta:
		model = Vulnerability
		interfaces = (relay.Node,)