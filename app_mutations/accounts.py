import graphene
from app_models.models import Account, Company
from app_types.types import AccountType, CompanyType
from app_mutations.companies import CompanyInput
from bson import ObjectId

class AccountInput(graphene.InputObjectType):
    ID = graphene.ID()
    name = graphene.String()
    ownerEmail = graphene.String()
    accountType = graphene.String() # master/sub
    seats = graphene.Int()
    subscriptionStartTime = graphene.String()
    subscriptionEndTime = graphene.String()

class CreateAccountMutation(graphene.Mutation):
    account = graphene.Field(AccountType)
    company = graphene.Field(CompanyType)

    class Arguments:
        account_data = AccountInput(required=True)
        company_data = CompanyInput(required=True)

    @staticmethod
    def get_account_object_by_ID(ID):
        return Account.objects.get(pk=ID)

    @staticmethod
    def get_company_object_by_ID(ID):
        return Company.objects.get(pk=ID)

    def mutate(self, info, account_data=None, company_data=None):
        company = CreateAccountMutation.get_company_object_by_ID(company_data.ID)
        account = Account(
            name=account_data.name,
            ownerEmail=account_data.ownerEmail,
            accountType=account_data.accountType,
            seats=account_data.seats,
            subscriptionStartTime=account_data.subscriptionStartTime,
            subscriptionEndTime=account_data.subscriptionEndTime
        )

        try:
            account_object = Account.objects.get(pk=account_data.ID)
        except Account.DoesNotExist:
            account_object = None
        if account_object:
            account = account_object
            if account_data.name:
                account.name = account_data.name
            if account_data.ownerEmail:
                account.ownerEmail = account_data.ownerEmail
            if account_data.accountType:
                account.accountType = account_data.accountType
            if account_data.seats:
                account.seats = account_data.seats
            if account_data.subscriptionStartTime:
                account.subscriptionStartTime  = account_data.subscriptionStartTime
            if company_data.subscriptionEndTime:
                account.subscriptionEndTime = account_data.subscriptionEndTime
            account.save()
            return CreateAccountMutation(account=account)
        else:
            account.ID = ObjectId()
            account.company = company
            account.save()
            return CreateAccountMutation(account=account)

class UpdateAccountMutation(graphene.Mutation):
    account = graphene.Field(AccountType)
    company = graphene.Field(CompanyType)

    class Arguments:
        account_data = AccountInput(required=True)

    @staticmethod
    def get_account_object_by_ID(ID):
        return Account.objects.get(pk=ID)

    @staticmethod
    def get_company_object_by_ID(ID):
        return Company.objects.get(pk=ID)

    def mutate(self, info, account_data=None, company_data=None):
        company = UpdateAccountMutation.get_company_object_by_ID(company_data.ID)
        account = UpdateAccountMutation.get_account_object_by_ID(account_data.ID)

        try:
            account_object = Account.objects.get(pk=account_data.ID)
        except Account.DoesNotExist:
            account_object = None
        if account_object:
            account = account_object
            if account_data.name:
                account.name = account_data.name
            if account_data.ownerEmail:
                account.ownerEmail = account_data.ownerEmail
            if account_data.accountType:
                account.accountType = account_data.accountType
            if account_data.seats:
                account.seats = account_data.seats
            if account_data.subscriptionStartTime:
                account.subscriptionStartTime  = account_data.subscriptionStartTime
            if company_data.subscriptionEndTime:
                account.subscriptionEndTime = account_data.subscriptionEndTime
            account.save()
            return UpdateAccountMutation(account=account)

class DeleteAccountMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Account.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteAccountMutation(success=success)