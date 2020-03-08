import graphene
from app_models.graphql.models import Rank
from app_types.types import RankType

class RankInput(graphene.InputObjectType):
    id = graphene.ID()
    coursesComplete = graphene.Int()
    flagsObtained = graphene.Int()
    position = graphene.Int()

class CreateRankMutation(graphene.Mutation):
    rank = graphene.Field(RankType)
    class Arguments:
        rank_data = RankInput(required=True)
    def mutate(self, info, rank_data=None):
        rank = Rank(
            value=rank_data.value
        )
        rank.save()
        return CreateRankMutation(rank=rank)

class UpdateRankMutation(graphene.Mutation):
    rank = graphene.Field(RankType)
    class Arguments:
        rank_data = RankInput(required=True)
    @staticmethod
    def get_object(id):
        return Rank.objects.get(pk=id)
    def mutate(self, info, rank_data=None):
        rank = UpdateRankMutation.get_object(rank_data.id)
        if rank_data.value:
            rank.value = rank_data.value
        rank.save()
        return UpdateRankMutation(rank=rank)

class DeleteRankMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Rank.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteRankMutation(success=success)