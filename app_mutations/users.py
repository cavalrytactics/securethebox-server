import graphene
from app_models.models import User
from app_types.types import UserType

class UserInput(graphene.InputObjectType):
    ID = graphene.ID()
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
    def get_object(ID):
        return User.objects.get(pk=ID)
    def mutate(self, info, user_data=None):
        user = UpdateUserMutation.get_object(user_data.ID)
        if user_data.value:
            user.value = user_data.value
        user.save()
        return UpdateUserMutation(user=user)

class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            User.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteUserMutation(success=success)