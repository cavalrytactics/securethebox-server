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
    Subscription,
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
    SubscriptionType,
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
from app_mutations.subscriptions import (
    CreateSubscriptionMutation,
    UpdateSubscriptionMutation,
    DeleteSubscriptionMutation,
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
    create_subscription = CreateSubscriptionMutation.Field()
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
    update_subscription = UpdateSubscriptionMutation.Field()
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
    delete_subscription = DeleteSubscriptionMutation.Field()
    delete_team = DeleteTeamMutation.Field()
    delete_topic = DeleteTopicMutation.Field()
    delete_university = DeleteUniversityMutation.Field()
    delete_user = DeleteUserMutation.Field()
    delete_vulnerability = DeleteVulnerabilityMutation.Field()

class Query(graphene.ObjectType):
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
    subscriptions = MongoengineConnectionField(SubscriptionType)
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
    subscriptions_list = graphene.List(SubscriptionType)
    teams_list = graphene.List(TeamType)
    topics_list = graphene.List(TopicType)
    universities_list = graphene.List(UniversityType)
    users_list = graphene.List(UserType)
    vulnerabilities_list = graphene.List(VulnerabilityType)
    
    def resolve_applications_list(self, info):
        return Application.objects.all()
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
        return Contianer.objects.all()
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
    def resolve_subscriptions_list(self, info):
        return Subscription.objects.all()
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

schema = graphene.Schema(
    query=Query, 
    mutation=Mutations,
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
        SubscriptionType,
        TeamType,
        TopicType,
        UserType,
        UniversityType,
        VulnerabilityType
        ]
    )