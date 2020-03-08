import graphene
from app_models.graphql.models import Step
from app_types.types import StepType

class StepInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateStepMutation(graphene.Mutation):
    step = graphene.Field(StepType)
    class Arguments:
        step_data = StepInput(required=True)
    def mutate(self, info, step_data=None):
        step = Step(
            value=step_data.value
        )
        step.save()
        return CreateStepMutation(step=step)

class UpdateStepMutation(graphene.Mutation):
    step = graphene.Field(StepType)
    class Arguments:
        step_data = StepInput(required=True)
    @staticmethod
    def get_object(id):
        return Step.objects.get(pk=id)
    def mutate(self, info, step_data=None):
        step = UpdateStepMutation.get_object(step_data.id)
        if step_data.value:
            step.value = step_data.value
        step.save()
        return UpdateStepMutation(step=step)

class DeleteStepMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Step.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteStepMutation(success=success)