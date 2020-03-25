import graphene
from app_models.models import Credential
from app_types.types import CredentialType

class CredentialInput(graphene.InputObjectType):
    ID = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateCredentialMutation(graphene.Mutation):
    credential = graphene.Field(CredentialType)
    class Arguments:
        credential_data = CredentialInput(required=True)
    def mutate(self, info, credential_data=None):
        credential = Credential(
            value=credential_data.value
        )
        credential.save()
        return CreateCredentialMutation(credential=credential)

class UpdateCredentialMutation(graphene.Mutation):
    credential = graphene.Field(CredentialType)
    class Arguments:
        credential_data = CredentialInput(required=True)
    @staticmethod
    def get_object(ID):
        return Credential.objects.get(pk=ID)
    def mutate(self, info, credential_data=None):
        credential = UpdateCredentialMutation.get_object(credential_data.ID)
        if credential_data.value:
            credential.value = credential_data.value
        credential.save()
        return UpdateCredentialMutation(credential=credential)

class DeleteCredentialMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Credential.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteCredentialMutation(success=success)