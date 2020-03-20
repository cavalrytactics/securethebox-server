import graphene
from app_models.models import Course, Report, Category, Cluster, Step
from app_types.types import CourseType,ReportType,CategoryType,ClusterType
from app_mutations.reports import ReportInput
from app_mutations.categories import CategoryInput
from app_mutations.clusters import ClusterInput
from bson import ObjectId 

class CourseInput(graphene.InputObjectType):
    ID = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    activeStep = graphene.Int()
    length = graphene.Int()
    totalSteps = graphene.Int()
    slug = graphene.String()
    cluster = graphene.String()
    category = graphene.String()

class CreateCourseMutation(graphene.Mutation):
    course = graphene.Field(CourseType)
    category = graphene.Field(CategoryType)
    cluster = graphene.Field(ClusterType)
    
    class Arguments:
        course_data = CourseInput(required=True)
        category_data = CategoryInput(required=False)
        cluster_data = ClusterInput(required=False)
        
    @staticmethod
    def get_category_object_by_value(value):
        return Category.objects.get(value=value)

    @staticmethod
    def get_cluster_object_by_value(value):
        return Cluster.objects.get(value=value)
    
    def mutate(self, info, course_data=None,  category_data=None, cluster_data=None):
        category = CreateCourseMutation.get_category_object_by_value(category_data.value)
        cluster = CreateCourseMutation.get_cluster_object_by_value(cluster_data.value)
        course = Course(
                title=course_data.title,
                description=course_data.description,
                category=category,
                cluster=cluster,
                activeStep=course_data.activeStep,
                length=course_data.length,
                totalSteps=course_data.totalSteps,
                slug=course_data.slug
            )

        try:
            course_object = Course.objects.get(title=course_data.title)
        except Course.DoesNotExist:
            course_object = None
        if course_object:
            # Course exists, update
            course = course_object
            if course_data.title:
                course.title = course_data.title
            if course_data.description:
                course.description = course_data.description
            if category_data.value:
                course.category = category
            if cluster_data.value:
                course.cluster = cluster   
            if course_data.activeStep:
                course.activeStep = course_data.activeStep
            if course_data.length:
                course.length = course_data.length
            if course_data.totalSteps:
                course.totalSteps = course_data.totalSteps
            if course_data.slug:
                course.slug = course_data.slug
            course.save()
            return UpdateCourseMutation(course=course)
        else:
            # Course does not exist
            course.ID = ObjectId()
            course.cluster = cluster
            course.category = category
            course.save()
            return CreateCourseMutation(course=course)

class UpdateCourseMutation(graphene.Mutation):
    course = graphene.Field(CourseType)
    category = graphene.Field(CategoryType)
    cluster = graphene.Field(ClusterType)
    
    class Arguments:
        course_data = CourseInput(required=True)
        category_data = CategoryInput(required=False)
        cluster_data = ClusterInput(required=False)
    
    @staticmethod
    def get_category_object_by_value(value):
        return Category.objects.get(value=value)
    
    @staticmethod
    def get_cluster_object_by_value(value):
        return Cluster.objects.get(value=value)
    
    @staticmethod
    def get_object(ID):
        return Course.objects.get(pk=ID)
    
    def mutate(self, info, course_data=None):
        course = UpdateCourseMutation.get_object(course_data.ID)
        category = UpdateCourseMutation.get_category_object_by_value(category_data.value)
        cluster = UpdateCourseMutation.get_cluster_object_by_value(cluster_data.value)

        try:
            course_object = Course.objects.get(pk=course_data.ID)
        except Course.DoesNotExist:
            course_object = None
        if course_object:
            # Course exists
            course = course_object
            if course_data.title:
                course.title = course_data.title
            if course_data.description:
                course.description = course_data.description
            if category_data.value:
                course.category = category
            if cluster_data.value:
                course.cluster = cluster   
            if course_data.activeStep:
                course.activeStep = course_data.activeStep
            if course_data.length:
                course.length = course_data.length
            if course_data.totalSteps:
                course.totalSteps = course_data.totalSteps
            if course_data.slug:
                course.slug = course_data.slug
            course.save()
        return UpdateCourseMutation(course=course)

class DeleteCourseMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID()
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Course.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteCourseMutation(success=success)