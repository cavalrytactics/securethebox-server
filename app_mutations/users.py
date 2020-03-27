import graphene
from app_models.models import User, Company
from app_types.types import UserType, CompanyType
from app_mutations.companies import CompanyInput
from bson import ObjectId

class UserInput(graphene.InputObjectType):
    ID = graphene.ID()
    handle = graphene.String()
    email = graphene.String()
    subscriptionType = graphene.Int() # 0=basic/1=licensed
    accessControlRole = graphene.String() # use pycasbin
    status = graphene.String() # pending/active/inactive

class CreateUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)
    company = graphene.Field(CompanyType)

    class Arguments:
        user_data = UserInput(required=True)
        company_data = CompanyInput(required=True)

    @staticmethod
    def get_user_object_by_ID(ID):
        return User.objects.get(pk=ID)

    @staticmethod
    def get_company_object_by_ID(ID):
        return Company.objects.get(pk=ID)

    def mutate(self, info, user_data=None, company_data=None):
        company = CreateUserMutation.get_company_object_by_ID(company_data.ID)
        user = User(
            handle=user_data.handle,
            email=user_data.email,
            subscriptionType=user_data.subscriptionType,
            accessControlRole=user_data.accessControlRole,
            status=user_data.status
        )

        try:
            user_object = User.objects.get(pk=user_data.ID)
        except User.DoesNotExist:
            user_object = None
        if user_object:
            user = user_object
            if user_data.handle:
                user.handle = user_data.handle
            if user_data.email:
                user.email = user_data.email
            if user_data.subscriptionType:
                user.subscriptionType = user_data.subscriptionType
            if user_data.accessControlRole:
                user.accessControlRole = user_data.accessControlRole
            if user_data.status:
                user.status  = user_data.status
            if company_data.value:
                user.company = company
            user.save()
            return CreateUserMutation(user=user)
        else:
            user.ID = ObjectId()
            user.company = company
            user.save()
            return CreateUserMutation(user=user)

class UpdateUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)
    company = graphene.Field(CompanyType)

    class Arguments:
        user_data = UserInput(required=True)

    @staticmethod
    def get_user_object_by_ID(ID):
        return User.objects.get(pk=ID)

    @staticmethod
    def get_company_object_by_ID(ID):
        return Company.objects.get(pk=ID)

    def mutate(self, info, user_data=None, company_data=None):
        user = UpdateUserMutation.get_user_object_by_ID(user_data.ID)
        company = UpdateUserMutation.get_company_object_by_ID(company_data.ID)

        try:
            user_object = User.objects.get(pk=user_data.ID)
        except User.DoesNotExist:
            user_object = None
        if user_object:
            user = user_object
            if user_data.handle:
                user.handle = user_data.handle
            if user_data.email:
                user.email = user_data.email
            if user_data.subscriptionType:
                user.subscriptionType = user_data.subscriptionType
            if user_data.accessControlRole:
                user.accessControlRole = user_data.accessControlRole
            if company_data.value:
                user.company = company
            if user_data.status:
                user.status  = user_data.status
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