import graphene
from app_models.models import Competency
from app_types.types import CompetencyType

class CompetencyInput(graphene.InputObjectType):
    ID = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateCompetencyMutation(graphene.Mutation):
    competency = graphene.Field(CompetencyType)
    class Arguments:
        competency_data = CompetencyInput(required=True)
    def mutate(self, info, competency_data=None):
        competency = Competency(
            value=competency_data.value
        )
        competency.save()
        return CreateCompetencyMutation(competency=competency)

class UpdateCompetencyMutation(graphene.Mutation):
    competency = graphene.Field(CompetencyType)
    class Arguments:
        competency_data = CompetencyInput(required=True)
    @staticmethod
    def get_object(ID):
        return Competency.objects.get(pk=ID)
    def mutate(self, info, competency_data=None):
        competency = UpdateCompetencyMutation.get_object(competency_data.ID)
        if competency_data.value:
            competency.value = competency_data.value
        competency.save()
        return UpdateCompetencyMutation(competency=competency)

class DeleteCompetencyMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Competency.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteCompetencyMutation(success=success)