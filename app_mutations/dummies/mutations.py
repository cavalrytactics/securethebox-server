import graphene
from app_models.graphql.models import Dummy
from app_types.types import DummyType

class DummyInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateDummyMutation(graphene.Mutation):
    dummy = graphene.Field(DummyType)
    class Arguments:
        dummy_data = DummyInput(required=True)
    def mutate(self, info, dummy_data=None):
        dummy = Dummy(
            value=dummy_data.value
        )
        dummy.save()
        return CreateDummyMutation(dummy=dummy)

class UpdateDummyMutation(graphene.Mutation):
    dummy = graphene.Field(DummyType)
    class Arguments:
        dummy_data = DummyInput(required=True)
    @staticmethod
    def get_object(id):
        return Dummy.objects.get(pk=id)
    def mutate(self, info, dummy_data=None):
        dummy = UpdateDummyMutation.get_object(dummy_data.id)
        if dummy_data.value:
            dummy.value = dummy_data.value
        dummy.save()
        return UpdateDummyMutation(dummy=dummy)

class DeleteDummyMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Dummy.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteDummyMutation(success=success)