import graphene
from app_models.models import Submission
from app_types.types import SubmissionType
from bson import ObjectId 

class SubmissionInput(graphene.InputObjectType):
    ID = graphene.ID()
    author = graphene.String()
    verdict = graphene.String()
    creationTime = graphene.String() 
    relativeTime = graphene.String() 
    points = graphene.Int()
    content = graphene.String()

class CreateSubmissionMutation(graphene.Mutation):
    submission = graphene.Field(SubmissionType)

    class Arguments:
        submission_data = SubmissionInput(required=True)

    def mutate(self, info, submission_data=None):
        submission = Submission(
            author=submission_data.author,
            verdict=submission_data.verdict,
            creationTime=submission_data.creationTime,
            relativeTime=submission_data.relativeTime,
            points=submission_data.points,
            content=submission_data.content
        )

        try:
            submission_object = Submission.objects.get(value=submission_data.value) 
        except Submission.DoesNotExist:
            submission_object = None

        if submission_object:
            if submission_data.author:
                submission.author = submission_data.author
            if submission_data.verdict:
                submission.verdict = submission_data.verdict
            if submission_data.creationTime:
                submission.creationTime = submission_data.creationTime
            if submission_data.relativeTime:
                submission.relativeTime = submission_data.relativeTime
            if submission_data.points:
                submission.points = submission_data.points
            if submission_data.content:
                submission.content = submission_data.content
            submission.save()
            return UpdateSubmissionMutation(submission=submission)
        else:
            submission.ID = ObjectId()
            submission.save()
            return CreateSubmissionMutation(submission=submission)

class UpdateSubmissionMutation(graphene.Mutation):
    submission = graphene.Field(SubmissionType)

    class Arguments:
        submission_data = SubmissionInput(required=True)
    @staticmethod
    def get_object(ID):
        return Submission.objects.get(pk=ID)

    def mutate(self, info, submission_data=None):
        submission = UpdateSubmissionMutation.get_object(submission_data.ID)

        try:
            submission_object = Submission.objects.get(pk=submission_data.ID)
        except Submission.DoesNotExist:
            submission_object = submission
        if submission_object:
            if submission_data.author:
                submission.author = submission_data.author
            if submission_data.verdict:
                submission.verdict = submission_data.verdict
            if submission_data.creationTime:
                submission.creationTime = submission_data.creationTime
            if submission_data.relativeTime:
                submission.relativeTime = submission_data.relativeTime
            if submission_data.points:
                submission.points = submission_data.points
            if submission_data.content:
                submission.content = submission_data.content
            submission.save()
        return UpdateSubmissionMutation(submission=submission)

class DeleteSubmissionMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Submission.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteSubmissionMutation(success=success)