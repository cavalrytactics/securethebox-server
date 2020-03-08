import graphene
from app_models.graphql.models import User
from app_types.types import UserType

class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)
    class Arguments:
        user_data = UserInput(required=True)
    def mutate(self, info, user_data=None):
        user = User(
            value=user_data.value
        )
        user.save()
        return CreateUserMutation(user=user)

class UpdateUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)
    class Arguments:
        user_data = UserInput(required=True)
    @staticmethod
    def get_object(id):
        return User.objects.get(pk=id)
    def mutate(self, info, user_data=None):
        user = UpdateUserMutation.get_object(user_data.id)
        if user_data.value:
            user.value = user_data.value
        user.save()
        return UpdateUserMutation(user=user)

class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            User.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteUserMutation(success=success)