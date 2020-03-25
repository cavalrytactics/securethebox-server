import graphene
from app_models.models import University
from app_types.types import UniversityType


class UniversityInput(graphene.InputObjectType):
    ID = graphene.ID()
    team = graphene.ID()
    domain = graphene.String()

class CreateUniversityMutation(graphene.Mutation):
    university = graphene.Field(UniversityType)

    class Arguments:
        university_data = UniversityInput(required=True)

    @staticmethod
    def check_exists(value):
        allObjects = University.objects.all()
        for item in allObjects:
            if item.domain == value:
                return True
        return False

    def mutate(self, info, university_data=None):
        exists = CreateUniversityMutation.check_exists(university_data.domain)
        university = University(domain=university_data.domain)
        if exists == False:
            university.save()
        return CreateUniversityMutation(university=university)


class UpdateUniversityMutation(graphene.Mutation):
    university = graphene.Field(UniversityType)

    class Arguments:
        university_data = UniversityInput(required=True)

    @staticmethod
    def get_object(ID):
        return University.objects.get(pk=ID)

    def mutate(self, info, university_data=None):
        university = UpdateUniversityMutation.get_object(university_data.ID)
        if university_data.domain:
            university.domain = university_data.domain
        university.save()
        return UpdateUniversityMutation(university=university)


class DeleteUniversityMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()

    def mutate(self, info, ID):
        try:
            University.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteUniversityMutation(success=success)
