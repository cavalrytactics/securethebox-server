import graphene
from app_models.graphql.models import Solution
from app_types.types import SolutionType

class SolutionInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateSolutionMutation(graphene.Mutation):
    solution = graphene.Field(SolutionType)
    class Arguments:
        solution_data = SolutionInput(required=True)
    def mutate(self, info, solution_data=None):
        solution = Solution(
            value=solution_data.value
        )
        solution.save()
        return CreateSolutionMutation(solution=solution)

class UpdateSolutionMutation(graphene.Mutation):
    solution = graphene.Field(SolutionType)
    class Arguments:
        solution_data = SolutionInput(required=True)
    @staticmethod
    def get_object(id):
        return Solution.objects.get(pk=id)
    def mutate(self, info, solution_data=None):
        solution = UpdateSolutionMutation.get_object(solution_data.id)
        if solution_data.value:
            solution.value = solution_data.value
        solution.save()
        return UpdateSolutionMutation(solution=solution)

class DeleteSolutionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Solution.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteSolutionMutation(success=success)