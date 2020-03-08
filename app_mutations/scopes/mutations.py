import graphene
from app_models.graphql.models import Scope
from app_types.types import ScopeType

class ScopeInput(graphene.InputObjectType):
    id = graphene.ID()
    label = graphene.String()
    value = graphene.String()

class CreateScopeMutation(graphene.Mutation):
    scope = graphene.Field(ScopeType)

    class Arguments:
        scope_data = ScopeInput(required=True)

    @staticmethod
    def check_exists(value):
        allObjects = Scope.objects.all()
        for item in allObjects:
            if item.value == value:
                return True
        return False

    def mutate(self, info, scope_data=None):
        exists = CreateScopeMutation.check_exists(scope_data.value)
        scope = Scope(
            value=scope_data.value,
            label=scope_data.label
        )
        if exists == False:
            scope.save()
        return CreateScopeMutation(scope=scope)

class UpdateScopeMutation(graphene.Mutation):
    scope = graphene.Field(ScopeType)
    class Arguments:
        scope_data = ScopeInput(required=True)
    @staticmethod
    def get_object(id):
        return Scope.objects.get(pk=id)
    def mutate(self, info, scope_data=None):
        scope = UpdateScopeMutation.get_object(scope_data.id)
        if scope_data.value:
            scope.value = scope_data.value
        scope.save()
        return UpdateScopeMutation(scope=scope)

class DeleteScopeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Scope.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteScopeMutation(success=success)