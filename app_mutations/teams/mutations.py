import graphene
from app_models.graphql.models import Team
from app_types.types import TeamType

class TeamInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateTeamMutation(graphene.Mutation):
    team = graphene.Field(TeamType)
    class Arguments:
        team_data = TeamInput(required=True)
    def mutate(self, info, team_data=None):
        team = Team(
            value=team_data.value
        )
        team.save()
        return CreateTeamMutation(team=team)

class UpdateTeamMutation(graphene.Mutation):
    team = graphene.Field(TeamType)
    class Arguments:
        team_data = TeamInput(required=True)
    @staticmethod
    def get_object(id):
        return Team.objects.get(pk=id)
    def mutate(self, info, team_data=None):
        team = UpdateTeamMutation.get_object(team_data.id)
        if team_data.value:
            team.value = team_data.value
        team.save()
        return UpdateTeamMutation(team=team)

class DeleteTeamMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Team.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteTeamMutation(success=success)