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
    cluster = graphene.String()
    category = graphene.String()
    startDate = graphene.String()
    dueDate = graphene.String()
    destroyDate = graphene.String()

class CreateCourseMutation(graphene.Mutation):
    course = graphene.Field(CourseType)
    category = graphene.Field(CategoryType)
    cluster = graphene.Field(ClusterType)
    
    class Arguments:
        course_data = CourseInput(required=True)
        category_data = CategoryInput(required=False)
        cluster_data = ClusterInput(required=False)
        
    @staticmethod
    def get_category_object_by_ID(ID):
        return Category.objects.get(pk=ID)

    @staticmethod
    def get_cluster_object_by_ID(ID):
        return Cluster.objects.get(ID=ID)
    
    def mutate(self, info, course_data=None,  category_data=None, cluster_data=None):
        category = CreateCourseMutation.get_category_object_by_ID(category_data.ID)
        cluster = CreateCourseMutation.get_cluster_object_by_ID(cluster_data.ID)
        course = Course(
                title=course_data.title,
                description=course_data.description,
                category=category,
                cluster=cluster,
                startDate=course_data.startDate,
                dueDate=course_data.dueDate,
                destroyDate=course_data.destroyDate,
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
            if course_data.startDate:
                course.startDate = course_data.startDate
            if course_data.dueDate:
                course.dueDate = course_data.dueDate
            if course_data.destroyDate:
                course.destroyDate = course_data.destroyDate
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
    def get_course_object_by_ID(ID):
        return Course.objects.get(pk=ID)
    
    @staticmethod
    def get_category_object_by_ID(ID):
        return Category.objects.get(pk=ID)

    @staticmethod
    def get_cluster_object_by_ID(ID):
        return Cluster.objects.get(ID=ID)
    
    def mutate(self, info, course_data=None, category_data=None, cluster_data=None):
        course = UpdateCourseMutation.get_course_object_by_ID(course_data.ID)
        category = UpdateCourseMutation.get_category_object_by_ID(category_data.ID)
        cluster = UpdateCourseMutation.get_cluster_object_by_ID(cluster_data.ID)

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
            if course_data.startDate:
                course.startDate = course_data.startDate
            if course_data.dueDate:
                course.dueDate = course_data.dueDate
            if course_data.destroyDate:
                course.destroyDate = course_data.destroyDate
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