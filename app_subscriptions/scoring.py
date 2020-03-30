import graphene
from app_models.models import Scoring
from app_types.types import ScoringType
from bson import ObjectId 

class ScoringInput(graphene.InputObjectType):
    ID = graphene.ID()
    foo = graphene.Boolean()

