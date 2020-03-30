from rx import Observable
import random
import graphene
from graphene.relay import Node
from graphene_mongo.fields import MongoengineConnectionField
from app_models.models import (
    Application,
    Category,
    Cluster,
    Company,
    Competency,
    Configuration,
    Container,
    Course,
    Credential,
    Dummy,
    Job,
    Metric,
    Problem,
    Report,
    Rank,
    Scope,
    Service,
    Solution,
    Step,
    # Subscription,
    Submission,
    Team,
    Topic,
    University,
    User,
    Vulnerability
)
from app_types.types import (
    ApplicationType,
    CategoryType,
    ClusterType,
    CompanyType,
    CompetencyType,
    ConfigurationType,
    ContainerType,
    CourseType,
    CredentialType,
    DummyType,
    JobType,
    MetricType,
    ProblemType,
    RankType,
    ReportType,
    ScopeType,
    ServiceType,
    SolutionType,
    StepType,
    # SubscriptionType,
    SubmissionType,
    TeamType,
    TopicType,
    UniversityType,
    UserType,
    VulnerabilityType
)

from app_mutations.applications import (
    CreateApplicationMutation,
    UpdateApplicationMutation,
    DeleteApplicationMutation,
)
from app_mutations.categories import (
    CreateCategoryMutation,
    UpdateCategoryMutation,
    DeleteCategoryMutation,
)
from app_mutations.clusters import (
    CreateClusterMutation,
    UpdateClusterMutation,
    DeleteClusterMutation,
)
from app_mutations.companies import (
    CreateCompanyMutation,
    UpdateCompanyMutation,
    DeleteCompanyMutation,
)
from app_mutations.competencies import (
    CreateCompetencyMutation,
    UpdateCompetencyMutation,
    DeleteCompetencyMutation,
)
from app_mutations.containers import (
    CreateContainerMutation,
    UpdateContainerMutation,
    DeleteContainerMutation,
)
from app_mutations.configurations import (
    CreateConfigurationMutation,
    UpdateConfigurationMutation,
    DeleteConfigurationMutation,
)
from app_mutations.courses import (
    CreateCourseMutation,
    UpdateCourseMutation,
    DeleteCourseMutation,
)
from app_mutations.credentials import (
    CreateCredentialMutation,
    UpdateCredentialMutation,
    DeleteCredentialMutation,
)
from app_mutations.dummies import (
    CreateDummyMutation,
    UpdateDummyMutation,
    DeleteDummyMutation,
)
from app_mutations.jobs import (
    CreateJobMutation,
    UpdateJobMutation,
    DeleteJobMutation,
)
from app_mutations.metrics import (
    CreateMetricMutation,
    UpdateMetricMutation,
    DeleteMetricMutation,
)
from app_mutations.problems import (
    CreateProblemMutation,
    UpdateProblemMutation,
    DeleteProblemMutation,
)
from app_mutations.ranks import (
    CreateRankMutation,
    UpdateRankMutation,
    DeleteRankMutation,
)
from app_mutations.reports import (
    CreateReportMutation,
    UpdateReportMutation,
    DeleteReportMutation,
)
from app_mutations.scopes import (
    CreateScopeMutation,
    UpdateScopeMutation,
    DeleteScopeMutation,
)
from app_mutations.services import (
    CreateServiceMutation, 
    UpdateServiceMutation,
    DeleteServiceMutation,
    UpdateServiceAddApplicationMutation,
    UpdateServiceDeleteApplicationMutation
)
from app_mutations.solutions import (
    CreateSolutionMutation,
    UpdateSolutionMutation,
    DeleteSolutionMutation,
)
from app_mutations.steps import (
    CreateStepMutation,
    UpdateStepMutation,
    DeleteStepMutation,
)
# from app_mutations.subscriptions import (
#     CreateSubscriptionMutation,
#     UpdateSubscriptionMutation,
#     DeleteSubscriptionMutation,
# )
from app_mutations.submissions import (
    CreateSubmissionMutation,
    UpdateSubmissionMutation,
    DeleteSubmissionMutation,
)
from app_mutations.teams import (
    CreateTeamMutation,
    UpdateTeamMutation,
    DeleteTeamMutation,
)
from app_mutations.topics import (
    CreateTopicMutation,
    UpdateTopicMutation,
    DeleteTopicMutation,
)
from app_mutations.universities import (
    CreateUniversityMutation,
    UpdateUniversityMutation,
    DeleteUniversityMutation,
)
from app_mutations.users import (
    CreateUserMutation,
    UpdateUserMutation,
    DeleteUserMutation,
)
from app_mutations.vulnerabilities import (
    CreateVulnerabilityMutation,
    UpdateVulnerabilityMutation,
    DeleteVulnerabilityMutation,
)

class Mutations(graphene.ObjectType):
    create_application = CreateApplicationMutation.Field()
    create_category = CreateCategoryMutation.Field()
    create_cluster = CreateClusterMutation.Field()
    create_company = CreateCompanyMutation.Field()
    create_competency = CreateCompetencyMutation.Field()
    create_container = CreateContainerMutation.Field()
    create_configuration = CreateConfigurationMutation.Field()
    create_course = CreateCourseMutation.Field()
    create_credential = CreateCredentialMutation.Field()
    create_dummy = CreateDummyMutation.Field()
    create_job = CreateJobMutation.Field()
    create_metric = CreateMetricMutation.Field()
    create_problem = CreateProblemMutation.Field()
    create_rank = CreateRankMutation.Field()
    create_report = CreateReportMutation.Field()
    create_scope = CreateScopeMutation.Field()
    create_service = CreateServiceMutation.Field()
    create_solution = CreateSolutionMutation.Field()
    create_step = CreateStepMutation.Field()
    # create_subscription = CreateSubscriptionMutation.Field()
    create_submission = CreateSubmissionMutation.Field()
    create_team = CreateTeamMutation.Field()
    create_topic = CreateTopicMutation.Field()
    create_university = CreateUniversityMutation.Field()
    create_user = CreateUserMutation.Field()
    create_vulnerability = CreateVulnerabilityMutation.Field() 

    update_application = UpdateApplicationMutation.Field()
    update_cluster = UpdateClusterMutation.Field()
    update_company= UpdateCompanyMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    update_competency = UpdateCompetencyMutation.Field()
    update_configuration = UpdateConfigurationMutation.Field()
    update_container = UpdateContainerMutation.Field()
    update_course = UpdateCourseMutation.Field()
    update_credential = UpdateCredentialMutation.Field()
    update_dummy = UpdateDummyMutation.Field()
    update_job = UpdateJobMutation.Field()
    update_metric = UpdateMetricMutation.Field()
    update_problem = UpdateProblemMutation.Field()
    update_rank = UpdateRankMutation.Field()
    update_report = UpdateReportMutation.Field()
    update_scope = UpdateScopeMutation.Field()
    update_service = UpdateServiceMutation.Field()
    update_service_add_application = UpdateServiceAddApplicationMutation.Field()
    update_service_delete_application = UpdateServiceDeleteApplicationMutation.Field()
    update_solution = UpdateSolutionMutation.Field()
    update_step = UpdateStepMutation.Field()
    # update_subscription = UpdateSubscriptionMutation.Field()
    update_submission = UpdateSubmissionMutation.Field()
    update_team = UpdateTeamMutation.Field()
    update_topic = UpdateTopicMutation.Field()
    update_university = UpdateUniversityMutation.Field()
    update_user = UpdateUserMutation.Field()
    update_vulnerability = UpdateVulnerabilityMutation.Field()

    delete_application = DeleteApplicationMutation.Field()
    delete_category = DeleteCategoryMutation.Field()
    delete_cluster = DeleteClusterMutation.Field()
    delete_company = DeleteCompanyMutation.Field()
    delete_competency = DeleteCompetencyMutation.Field()
    delete_configuration = DeleteConfigurationMutation.Field()
    delete_container = DeleteContainerMutation.Field()
    delete_course = DeleteCourseMutation.Field()
    delete_credential = DeleteCredentialMutation.Field()
    delete_dummy = DeleteDummyMutation.Field()
    delete_job = DeleteJobMutation.Field()
    delete_metric = DeleteMetricMutation.Field()
    delete_problem = DeleteProblemMutation.Field()
    delete_rank = DeleteRankMutation.Field()
    delete_report = DeleteReportMutation.Field()
    delete_scope = DeleteScopeMutation.Field()
    delete_service = DeleteServiceMutation.Field()
    delete_solution = DeleteSolutionMutation.Field()
    delete_step = DeleteStepMutation.Field()
    # delete_subscription = DeleteSubscriptionMutation.Field()
    delete_submission = DeleteSubmissionMutation.Field()
    delete_team = DeleteTeamMutation.Field()
    delete_topic = DeleteTopicMutation.Field()
    delete_university = DeleteUniversityMutation.Field()
    delete_user = DeleteUserMutation.Field()
    delete_vulnerability = DeleteVulnerabilityMutation.Field()

class Query(graphene.ObjectType):
    base = graphene.String()
    node = Node.Field()

    applications = MongoengineConnectionField(ApplicationType)
    categories = MongoengineConnectionField(CategoryType)
    clusters = MongoengineConnectionField(ClusterType)
    companies = MongoengineConnectionField(CompanyType)
    competencies = MongoengineConnectionField(CompetencyType)
    configurations = MongoengineConnectionField(ConfigurationType)
    containers = MongoengineConnectionField(ContainerType)
    courses = MongoengineConnectionField(CourseType)
    credentials = MongoengineConnectionField(CredentialType)
    dummies = MongoengineConnectionField(DummyType)
    jobs = MongoengineConnectionField(JobType)
    metrics = MongoengineConnectionField(MetricType)
    problems = MongoengineConnectionField(ProblemType)
    ranks = MongoengineConnectionField(RankType)
    reports = MongoengineConnectionField(ReportType)
    scopes = MongoengineConnectionField(ScopeType)
    services = MongoengineConnectionField(ServiceType)
    solutions = MongoengineConnectionField(SolutionType)
    steps = MongoengineConnectionField(StepType)
    # subscriptions = MongoengineConnectionField(SubscriptionType)
    submissions = MongoengineConnectionField(SubmissionType)
    teams = MongoengineConnectionField(TeamType)
    topics = MongoengineConnectionField(TopicType)
    universities = MongoengineConnectionField(UniversityType)
    users = MongoengineConnectionField(UserType)
    vulnerabilities = MongoengineConnectionField(VulnerabilityType)

    applications_list = graphene.List(ApplicationType)
    configurations_list = graphene.List(ConfigurationType)
    clusters_list = graphene.List(ClusterType)
    companies_list = graphene.List(CompanyType)
    containers_list = graphene.List(ContainerType)
    configurations_list = graphene.List(ConfigurationType)
    credentials_list = graphene.List(CredentialType)
    categories_list = graphene.List(CategoryType)
    competencies_list = graphene.List(CompetencyType)
    courses_list = graphene.List(CourseType)
    dummies_list = graphene.List(DummyType)
    jobs_list = graphene.List(JobType)
    metrics_list = graphene.List(MetricType)
    problems_list = graphene.List(ProblemType)
    ranks_list = graphene.List(RankType)
    reports_list = graphene.List(ReportType)
    scopes_list = graphene.List(ScopeType)
    services_list = graphene.List(ServiceType)
    solutions_list = graphene.List(SolutionType)
    steps_list = graphene.List(StepType)
    # subscriptions_list = graphene.List(SubscriptionType)
    submissions_list = graphene.List(SubmissionType)
    teams_list = graphene.List(TeamType)
    topics_list = graphene.List(TopicType)
    universities_list = graphene.List(UniversityType)
    users_list = graphene.List(UserType)
    vulnerabilities_list = graphene.List(VulnerabilityType)

    application = graphene.Field(ApplicationType, ID=graphene.ID(required=True))
    cluster = graphene.Field(ClusterType, ID=graphene.ID(required=True))
    company = graphene.Field(CompanyType, ID=graphene.ID(required=True))
    container = graphene.Field(ContainerType, ID=graphene.ID(required=True))
    configuration = graphene.Field(ConfigurationType, ID=graphene.ID(required=True))
    credential = graphene.Field(CredentialType, ID=graphene.ID(required=True))
    category = graphene.Field(CategoryType, ID=graphene.ID(required=True))
    competency = graphene.Field(CompetencyType, ID=graphene.ID(required=True))
    course = graphene.Field(CourseType, ID=graphene.ID(required=True))
    dummy = graphene.Field(DummyType, ID=graphene.ID(required=True))
    job = graphene.Field(JobType, ID=graphene.ID(required=True))
    metric = graphene.Field(MetricType, ID=graphene.ID(required=True))
    problem = graphene.Field(ProblemType, ID=graphene.ID(required=True))
    rank = graphene.Field(RankType, ID=graphene.ID(required=True))
    report = graphene.Field(ReportType, ID=graphene.ID(required=True))
    scope = graphene.Field(ScopeType, ID=graphene.ID(required=True))
    service = graphene.Field(ServiceType, ID=graphene.ID(required=True))
    solution = graphene.Field(SolutionType, ID=graphene.ID(required=True))
    step = graphene.Field(StepType, ID=graphene.ID(required=True))
    # subscription = graphene.Field(SubscriptionType, ID=graphene.ID(required=True))
    submission = graphene.Field(SubmissionType, ID=graphene.ID(required=True))
    team = graphene.Field(TeamType, ID=graphene.ID(required=True))
    topic = graphene.Field(TopicType, ID=graphene.ID(required=True))
    university = graphene.Field(UniversityType, ID=graphene.ID(required=True))
    user = graphene.Field(UserType, ID=graphene.ID(required=True))
    vulnerability = graphene.Field(VulnerabilityType, ID=graphene.ID(required=True))

    def resolve_application(root, info, ID):
        return Application.objects.get(pk=ID)
    def resolve_cluster(root, info, ID):
        return Cluster.objects.get(pk=ID)
    def resolve_company(root, info, ID):
        return Company.objects.get(pk=ID)
    def resolve_container(root, info, ID):
        return Container.objects.get(pk=ID)
    def resolve_configuration(root, info, ID):
        return Configuration.objects.get(pk=ID)
    def resolve_credential(root, info, ID):
        return Credential.objects.get(pk=ID)
    def resolve_category(root, info, ID):
        return Category.objects.get(pk=ID)
    def resolve_competency(root, info, ID):
        return Competency.objects.get(pk=ID)
    def resolve_course(root, info, ID):
        return Course.objects.get(pk=ID)
    def resolve_dummy(root, info, ID):
        return Dummy.objects.get(pk=ID)
    def resolve_job(root, info, ID):
        return Job.objects.get(pk=ID)
    def resolve_metric(root, info, ID):
        return Metric.objects.get(pk=ID)
    def resolve_problem(root, info, ID):
        return Problem.objects.get(pk=ID)
    def resolve_rank(root, info, ID):
        return Rank.objects.get(pk=ID)
    def resolve_report(root, info, ID):
        return Report.objects.get(pk=ID)
    def resolve_scope(root, info, ID):
        return Scope.objects.get(pk=ID)
    def resolve_service(root, info, ID):
        return Service.objects.get(pk=ID)
    def resolve_solution(root, info, ID):
        return Solution.objects.get(pk=ID)
    def resolve_step(root, info, ID):
        return Step.objects.get(pk=ID)
    # def resolve_subscription(root, info, ID):
    #     return Subscription.objects.get(pk=ID)
    def resolve_submission(root, info, ID):
        return Submission.objects.get(pk=ID)
    def resolve_team(root, info, ID):
        return Team.objects.get(pk=ID)
    def resolve_topic(root, info, ID):
        return Topic.objects.get(pk=ID)
    def resolve_university(root, info, ID):
        return University.objects.get(pk=ID)
    def resolve_user(root, info, ID):
        return User.objects.get(pk=ID)
    def resolve_vulnerability(root, info, ID):
        return Vulnerability.objects.get(pk=ID)

    def resolve_clusters_list(self, info):
        return Cluster.objects.all()
    def resolve_companies_list(self, info):
        return Company.objects.all()
    def resolve_configurations_list(self, info):
        return Configuration.objects.all()
    def resolve_credentials_list(self, info):
        return Credential.objects.all()
    def resolve_categories_list(self, info):
        return Category.objects.all()
    def resolve_competencies_list(self, info):
        return Competency.objects.all()
    def resolve_containers_list(self, info):
        return Container.objects.all()
    def resolve_courses_list(self, info):
        return Course.objects.all()
    def resolve_dummies_list(self, info):
        return Dummy.objects.all()
    def resolve_jobs_list(self, info):
        return Job.objects.all()
    def resolve_metrics_list(self, info):
        return Metric.objects.all()
    def resolve_problems_list(self, info):
        return Problem.objects.all()
    def resolve_ranks_list(self, info):
        return Rank.sobjects.all()
    def resolve_reports_list(self, info):
        return Report.objects.all()
    def resolve_scopes_list(self, info):
        return Scope.objects.all()
    def resolve_services_list(self, info):
        return Service.objects.all()
    def resolve_solutions_list(self, info):
        return Solution.objects.all()
    def resolve_steps_list(self, info):
        return Step.objects.all()
    # def resolve_subscriptions_list(self, info):
    #     return Subscription.objects.all()
    def resolve_submissions_list(self, info):
        return Submission.objects.all()
    def resolve_teams_list(self, info):
        return Team.objects.all()
    def resolve_topics_list(self, info):
        return Topic.objects.all()
    def resolve_universities_list(self, info):
        return University.objects.all()
    def resolve_users_list(self, info):
        return User.objects.all()
    def resolve_vulnerabilities_list(self, info):
        return Vulnerability.objects.all()

class RandomType(graphene.ObjectType):
    seconds = graphene.Int()
    random_int = graphene.Int()

class Subscription(graphene.ObjectType):
    count_seconds = graphene.Int(up_to=graphene.Int())

    random_int = graphene.Field(RandomType)

    def resolve_count_seconds(root, info, up_to=5):
        print("callled")
        return Observable.interval(1000)\
                         .map(lambda i: "{0}".format(i))\
                         .take_while(lambda i: int(i) <= up_to)

    def resolve_random_int(root, info):
        return Observable.interval(1000).map(lambda i: RandomType(seconds=i, random_int=random.randint(0, 500)))

    # subscribe_to_foo = graphene.Boolean()
    
    # def resolve_subscribe_to_foo(self, args, **kwargs):
    #     return Observable.of(True)
        
schema = graphene.Schema(
    query=Query, 
    mutation=Mutations,
    subscription=Subscription,
    types=[
        ApplicationType,
        ClusterType,
        CategoryType,
        CompetencyType,
        ConfigurationType,
        ContainerType,
        CourseType,
        CredentialType,
        DummyType,
        JobType,
        MetricType,
        ProblemType,
        RankType,
        ReportType,
        ScopeType,
        SolutionType,
        StepType,
        ServiceType,
        # SubscriptionType,
        SubmissionType,
        TeamType,
        TopicType,
        UserType,
        UniversityType,
        VulnerabilityType
        ]
    )