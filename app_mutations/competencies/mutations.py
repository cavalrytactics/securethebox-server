import graphene
from app_models.graphql.models import Competency
from app_types.types import CompetencyType

class CompetencyInput(graphene.InputObjectType):
    id = graphene.ID()
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
    def get_object(id):
        return Competency.objects.get(pk=id)
    def mutate(self, info, competency_data=None):
        competency = UpdateCompetencyMutation.get_object(competency_data.id)
        if competency_data.value:
            competency.value = competency_data.value
        competency.save()
        return UpdateCompetencyMutation(competency=competency)

class DeleteCompetencyMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Competency.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteCompetencyMutation(success=success)