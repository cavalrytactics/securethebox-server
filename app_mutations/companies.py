import graphene
from app_models.models import Company
from app_types.types import CompanyType

class CompanyInput(graphene.InputObjectType):
    id = graphene.ID()
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
    def get_object(id):
        return Company.objects.get(pk=id)
    def mutate(self, info, company_data=None):
        company = UpdateCompanyMutation.get_object(company_data.id)
        if company_data.value:
            company.value = company_data.value
        company.save()
        return UpdateCompanyMutation(company=company)

class DeleteCompanyMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Company.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteCompanyMutation(success=success)