import graphene
from app_models.models import Solution, Vulnerability
from app_types.types import SolutionType, VulnerabilityType
from app_mutations.vulnerabilities import VulnerabilityInput
from bson import ObjectId 

class SolutionInput(graphene.InputObjectType):
    ID = graphene.ID()
    value = graphene.String()
    label = graphene.String()

class CreateSolutionMutation(graphene.Mutation):
    solution = graphene.Field(SolutionType)

    class Arguments:
        solution_data = SolutionInput(required=True)

    def mutate(self, info, solution_data=None, vulnerability_data=None):
        solution = Solution(
            value=solution_data.value,
            label=solution_data.label,
        )
        try:
            solution_object = Solution.objects.get(value=solution_data.value)
        except Solution.DoesNotExist:
            solution_object = None
        # Solution exists, update
        if solution_object:
            app = solution_object
            if solution_data.value:
                app.value = solution_data.value
            if solution_data.label:
                app.label = solution_data.label
            app.save()
            return UpdateSolutionMutation(solution=app)
        else:
            # Solution does not exist
            solution.ID = ObjectId()
            solution.save()
            return CreateSolutionMutation(solution=solution)

class UpdateSolutionMutation(graphene.Mutation):
    solution = graphene.Field(SolutionType)

    class Arguments:
        solution_data = SolutionInput(required=True)

    @staticmethod
    def get_object(ID):
        return Solution.objects.get(pk=ID)

    def mutate(self, info, solution_data=None):
        solution = UpdateSolutionMutation.get_object(solution_data.ID)
        try:
            solution_object = Solution.objects.get(pk=solution_data.ID)
        except Solution.DoesNotExist:
            solution_object = solution
        if solution_object:
            # Solution exists
            solution = solution_object
            if solution_data.value:
                solution.value = solution_data.value
            if solution_data.label:
                solution.label = solution_data.label
            solution.save()
        return UpdateSolutionMutation(solution=solution)

class DeleteSolutionMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID()
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Solution.objects.get(pk=ID).delete()
            success = True
            return DeleteSolutionMutation(success=success)
        except:
            success = False
            return DeleteSolutionMutation(success=success)