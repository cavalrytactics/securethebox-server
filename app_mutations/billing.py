import graphene
from app_models.models import Billing, Company
from app_types.types import BillingType, CompanyType
from app_mutations.companies import CompanyInput 
from bson import ObjectId

class BillingInput(graphene.InputObjectType):
    ID = graphene.ID()
    email = graphene.String()

class CreateBillingMutation(graphene.Mutation):
    billing = graphene.Field(BillingType)
    company = graphene.Field(CompanyType)

    class Arguments:
        billing_data = BillingInput(required=True)
        company_data = CompanyInput(required=True)

    @staticmethod
    def get_billing_object_by_ID(ID):
        return Billing.objects.get(pk=ID)

    @staticmethod
    def get_company_object_by_ID(ID):
        return Company.objects.get(pk=ID)

    def mutate(self, info, billing_data=None, company_data=None):
        company = CreateBillingMutation.get_company_object_by_ID(company_data.ID)
        billing = Billing(
            handle=billing_data.handle,
            email=billing_data.email,
            subscriptionType=billing_data.subscriptionType,
            accessControlRole=billing_data.accessControlRole,
            status=billing_data.status
        )

        try:
            billing_object = Billing.objects.get(pk=billing_data.ID)
        except Billing.DoesNotExist:
            billing_object = None
        if billing_object:
            billing = billing_object
            if billing_data.handle:
                billing.handle = billing_data.handle
            if billing_data.email:
                billing.email = billing_data.email
            if billing_data.subscriptionType:
                billing.subscriptionType = billing_data.subscriptionType
            if billing_data.accessControlRole:
                billing.accessControlRole = billing_data.accessControlRole
            if billing_data.status:
                billing.status  = billing_data.status
            if company_data.value:
                billing.company = company
            billing.save()
            return CreateBillingMutation(billing=billing)
        else:
            billing.ID = ObjectId()
            billing.company = company
            billing.save()
            return CreateBillingMutation(billing=billing)

class UpdateBillingMutation(graphene.Mutation):
    billing = graphene.Field(BillingType)
    company = graphene.Field(CompanyType)

    class Arguments:
        billing_data = BillingInput(required=True)

    @staticmethod
    def get_billing_object_by_ID(ID):
        return Billing.objects.get(pk=ID)

    @staticmethod
    def get_company_object_by_ID(ID):
        return Company.objects.get(pk=ID)

    def mutate(self, info, billing_data=None, company_data=None):
        billing = UpdateBillingMutation.get_billing_object_by_ID(billing_data.ID)
        company = UpdateBillingMutation.get_company_object_by_ID(company_data.ID)

        try:
            billing_object = Billing.objects.get(pk=billing_data.ID)
        except Billing.DoesNotExist:
            billing_object = None
        if billing_object:
            billing = billing_object
            if billing_data.handle:
                billing.handle = billing_data.handle
            if billing_data.email:
                billing.email = billing_data.email
            if billing_data.subscriptionType:
                billing.subscriptionType = billing_data.subscriptionType
            if billing_data.accessControlRole:
                billing.accessControlRole = billing_data.accessControlRole
            if company_data.value:
                billing.company = company
            if billing_data.status:
                billing.status  = billing_data.status
            billing.save()
        return UpdateBillingMutation(billing=billing)

class DeleteBillingMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Billing.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteBillingMutation(success=success)