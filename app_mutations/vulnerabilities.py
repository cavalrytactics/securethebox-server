import graphene
from app_models.models import Vulnerability
from app_types.types import VulnerabilityType

class VulnerabilityInput(graphene.InputObjectType):
    ID = graphene.ID()
    value = graphene.String()
    label = graphene.String() 
    type = graphene.String()
    exploitDbUrl = graphene.String()

class CreateVulnerabilityMutation(graphene.Mutation):
    vulnerability = graphene.Field(VulnerabilityType)

    class Arguments:
        vulnerability_data = VulnerabilityInput(required=True)
        
    def mutate(self, info, vulnerability_data=None):
        vulnerability = Vulnerability(
            value=vulnerability_data.value,
            label=vulnerability_data.label,
            type=vulnerability_data.type,
            exploitDbUrl=vulnerability_data.exploitDbUrl
        )
        try:
            vulnerability_object = Vulnerability.objects.get(type=vulnerability_data.type)
        except Vulnerability.DoesNotExist:
            vulnerability_object = None
        if vulnerability_object:
            # Vulnerability exists
            vulnerability = vulnerability_object
            if vulnerability_data.label:
                vulnerability_data.label = vulnerability_data.label
            if vulnerability_data.value:
                vulnerability_data.value = vulnerability_data.value
            if vulnerability_data.type:
                vulnerability_data.type = vulnerability_data.type
            if vulnerability_data.exploitDbUrl:
                vulnerability_data.exploitDbUrl = vulnerability_data.exploitDbUrl
            vulnerability.save()
            return CreateVulnerabilityMutation(vulnerability=vulnerability)
        else:
            vulnerability.save()
            return CreateVulnerabilityMutation(vulnerability=vulnerability)

class UpdateVulnerabilityMutation(graphene.Mutation):
    vulnerability = graphene.Field(VulnerabilityType)
    class Arguments:
        vulnerability_data = VulnerabilityInput(required=True)

    @staticmethod
    def get_object(ID):
        return Vulnerability.objects.get(pk=ID)
    def mutate(self, info, vulnerability_data=None):
        vulnerability = UpdateVulnerabilityMutation.get_object(vulnerability_data.ID)
        if vulnerability_data.label:
            vulnerability.label = vulnerability_data.label
        if vulnerability_data.value:
            vulnerability.value = vulnerability_data.value
        if vulnerability_data.type:
            vulnerability.type = vulnerability_data.type
        if vulnerability_data.exploitDbUrl:
            vulnerability_data.exploitDbUrl = vulnerability_data.exploitDbUrl
        vulnerability.save()
        return UpdateVulnerabilityMutation(vulnerability=vulnerability)

class DeleteVulnerabilityMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Vulnerability.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteVulnerabilityMutation(success=success)