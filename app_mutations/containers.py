import graphene
from app_models.models import Container
from app_types.types import ContainerType

class ContainerInput(graphene.InputObjectType):
    ID = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateContainerMutation(graphene.Mutation):
    container = graphene.Field(ContainerType)
    class Arguments:
        container_data = ContainerInput(required=True)
    def mutate(self, info, container_data=None):
        container = Container(
            value=container_data.value
        )
        container.save()
        return CreateContainerMutation(container=container)

class UpdateContainerMutation(graphene.Mutation):
    container = graphene.Field(ContainerType)
    class Arguments:
        container_data = ContainerInput(required=True)
    @staticmethod
    def get_object(ID):
        return Container.objects.get(pk=ID)
    def mutate(self, info, container_data=None):
        container = UpdateContainerMutation.get_object(container_data.ID)
        if container_data.value:
            container.value = container_data.value
        container.save()
        return UpdateContainerMutation(container=container)

class DeleteContainerMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Container.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteContainerMutation(success=success)