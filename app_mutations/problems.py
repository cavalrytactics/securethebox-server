import graphene
from app_models.models import Problem
from app_types.types import ProblemType

class ProblemInput(graphene.InputObjectType):
    ID = graphene.ID()
    label = graphene.String()
    value = graphene.String()

class CreateProblemMutation(graphene.Mutation):
    problem = graphene.Field(ProblemType)

    class Arguments:
        problem_data = ProblemInput(required=True)

    def mutate(self, info, problem_data=None):
        problem = Problem(
            value=problem_data.value,
            label=problem_data.label
        )
        problem.save()
        return CreateProblemMutation(problem=problem)

class UpdateProblemMutation(graphene.Mutation):
    problem = graphene.Field(ProblemType)
    class Arguments:
        problem_data = ProblemInput(required=True)
    @staticmethod
    def get_object(ID):
        return Problem.objects.get(pk=ID)
    def mutate(self, info, problem_data=None):
        problem = UpdateProblemMutation.get_object(problem_data.ID)
        if problem_data.label:
            problem.label = problem_data.label
        if problem_data.value:
            problem.value = problem_data.value
        problem.save()
        return UpdateProblemMutation(problem=problem)

class DeleteProblemMutation(graphene.Mutation):
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