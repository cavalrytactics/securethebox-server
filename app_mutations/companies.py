import graphene
from app_models.models import Company
from app_types.types import CompanyType

class CompanyInput(graphene.InputObjectType):
    ID = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateCompanyMutation(graphene.Mutation):
    company = graphene.Field(CompanyType)
    class Arguments:
        company_data = CompanyInput(required=True)
    def mutate(self, info, company_data=None):
        company = Company(
            value=company_data.value
        )
        company.save()
        return CreateCompanyMutation(company=company)

class UpdateCompanyMutation(graphene.Mutation):
    company = graphene.Field(CompanyType)
    class Arguments:
        company_data = CompanyInput(required=True)
    @staticmethod
    def get_object(ID):
        return Company.objects.get(pk=ID)
    def mutate(self, info, company_data=None):
        company = UpdateCompanyMutation.get_object(company_data.ID)
        if company_data.value:
            company.value = company_data.value
        company.save()
        return UpdateCompanyMutation(company=company)

class DeleteCompanyMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Company.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteCompanyMutation(success=success)