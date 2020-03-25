import graphene
from app_models.models import Job
from app_types.types import JobType

class JobInput(graphene.InputObjectType):
    ID = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateJobMutation(graphene.Mutation):
    job = graphene.Field(JobType)
    class Arguments:
        job_data = JobInput(required=True)
    def mutate(self, info, job_data=None):
        job = Job(
            value=job_data.value
        )
        job.save()
        return CreateJobMutation(job=job)

class UpdateJobMutation(graphene.Mutation):
    job = graphene.Field(JobType)
    class Arguments:
        job_data = JobInput(required=True)
    @staticmethod
    def get_object(ID):
        return Job.objects.get(pk=ID)
    def mutate(self, info, job_data=None):
        job = UpdateJobMutation.get_object(job_data.ID)
        if job_data.value:
            job.value = job_data.value
        job.save()
        return UpdateJobMutation(job=job)

class DeleteJobMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Job.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteJobMutation(success=success)