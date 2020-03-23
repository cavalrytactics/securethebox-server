import graphene
from app_models.models import Problem
from app_types.types import ProblemType
from bson import ObjectId 

class ProblemInput(graphene.InputObjectType):
    ID = graphene.ID()
    label = graphene.String()
    value = graphene.String()
    number = graphene.Int()
    points = graphene.Int()
    instructions = graphene.String()
    startDate = graphene.String()
    dueDate = graphene.String()
    rejectDate = graphene.String()

class ProblemQuery(graphene.InputField):
    problem = graphene.Field(ProblemType)

    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Problem.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteProblemMutation(success=success)
