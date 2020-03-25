import graphene
from app_models.models import Step
from app_types.types import StepType

class StepInput(graphene.InputObjectType):
    ID = graphene.ID()
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
    def get_object(ID):
        return Step.objects.get(pk=ID)
    def mutate(self, info, step_data=None):
        step = UpdateStepMutation.get_object(step_data.ID)
        if step_data.value:
            step.value = step_data.value
        step.save()
        return UpdateStepMutation(step=step)

class DeleteStepMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Step.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteStepMutation(success=success)