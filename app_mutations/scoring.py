import graphene
from app_models.models import Scoring
from app_types.types import ScoringType

class ScoringInput(graphene.InputObjectType):
    ID = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateScoringMutation(graphene.Mutation):
    scoring = graphene.Field(ScoringType)
    class Arguments:
        scoring_data = ScoringInput(required=True)
    def mutate(self, info, scoring_data=None):
        scoring = Scoring(
            value=scoring_data.value
        )
        scoring.save()
        return CreateScoringMutation(scoring=scoring)

class UpdateScoringMutation(graphene.Mutation):
    scoring = graphene.Field(ScoringType)
    class Arguments:
        scoring_data = ScoringInput(required=True)
    @staticmethod
    def get_object(ID):
        return Scoring.objects.get(pk=ID)
    def mutate(self, info, scoring_data=None):
        scoring = UpdateScoringMutation.get_object(scoring_data.ID)
        if scoring_data.value:
            scoring.value = scoring_data.value
        scoring.save()
        return UpdateScoringMutation(scoring=scoring)

class DeleteScoringMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Scoring.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteScoringMutation(success=success)