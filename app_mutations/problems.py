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

class CreateProblemMutation(graphene.Mutation):
    problem = graphene.Field(ProblemType)

    class Arguments:
        problem_data = ProblemInput(required=True)

    def mutate(self, info, problem_data=None):
        problem = Problem(
            value=problem_data.value,
            label=problem_data.label,
            number=problem_data.number,
            startDate=problem_data.startDate,
            dueDate=problem_data.dueDate,
            rejectDate=problem_data.rejectDate,
            points=problem_data.points,
            instructions=problem_data.instructions
        )

        try:
            problem_object = Problem.objects.get(value=problem_data.value)
        except Problem.DoesNotExist:
            problem_object = None

        if problem_object:
            if problem_data.label:
                problem.label = problem_data.label
            if problem_data.value:
                problem.value = problem_data.value
            if problem_data.number:
                problem.number = problem_data.number
            if problem_data.startDate:
                problem.startDate = problem_data.startDate
            if problem_data.dueDate:
                problem.dueDate = problem_data.dueDate
            if problem_data.rejectDate:
                problem.rejectDate = problem_data.rejectDate
            if problem_data.points:
                problem.points = problem_data.points
            if problem_data.instructions:
                problem.instructions = problem_data.instructions
            problem.save()
            return UpdateProblemMutation(problem=problem)
        else:
            problem.ID = ObjectId()
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

        try:
            problem_object = Problem.objects.get(pk=problem_data.ID)
        except Problem.DoesNotExist:
            problem_object = problem
        if problem_object:
            if problem_data.label:
                problem.label = problem_data.label
            if problem_data.value:
                problem.value = problem_data.value
            if problem_data.number:
                problem.number = problem_data.number
            if problem_data.startDate:
                problem.startDate = problem_data.startDate
            if problem_data.dueDate:
                problem.dueDate = problem_data.dueDate
            if problem_data.rejectDate:
                problem.rejectDate = problem_data.rejectDate
            if problem_data.points:
                problem.points = problem_data.points
            if problem_data.instructions:
                problem.instructions = problem_data.instructions
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