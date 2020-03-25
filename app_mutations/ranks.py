import graphene
from app_models.models import Rank
from app_types.types import RankType

class RankInput(graphene.InputObjectType):
    ID = graphene.ID()
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
    def get_object(ID):
        return Rank.objects.get(pk=ID)
    def mutate(self, info, rank_data=None):
        rank = UpdateRankMutation.get_object(rank_data.ID)
        if rank_data.value:
            rank.value = rank_data.value
        rank.save()
        return UpdateRankMutation(rank=rank)

class DeleteRankMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Rank.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteRankMutation(success=success)