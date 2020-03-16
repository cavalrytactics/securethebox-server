import graphene
from app_models.models import Application, Vulnerability
from app_types.types import ApplicationType, VulnerabilityType
from app_mutations.vulnerabilities import VulnerabilityInput

class ApplicationInput(graphene.InputObjectType):
    id = graphene.ID()
    # _id = graphene.ID(primary_key=True)
    value = graphene.String()
    label = graphene.String()
    version = graphene.String()

class CreateApplicationMutation(graphene.Mutation):
    application = graphene.Field(ApplicationType)
    vulnerability = graphene.Field(VulnerabilityType)

    class Arguments:
        application_data = ApplicationInput(required=True)
        vulnerability_data = VulnerabilityInput(required=True)
    
    @staticmethod
    def get_vulnerability_object_by_value(value):
        return Vulnerability.objects.get(value=value)   

    def mutate(self, info, application_data=None, vulnerability_data=None):
        application = Application(
            value=application_data.value,
            label=application_data.label,
            version=application_data.version,
        )
        vulnerability = Vulnerability(
                        value=vulnerability_data.value,
                        label=vulnerability_data.label,
                        type=vulnerability_data.type,
                        exploitDbUrl=vulnerability_data.exploitDbUrl 
                    )
        try:
            application_object = Application.objects.get(value=application_data.value)
        except Application.DoesNotExist:
            application_object = None
        # Application exists, updating... update application
        if application_object:
            application = application_object
            if application_data.value:
                application.value = application_data.value
            if application_data.label:
                application.label = application_data.label
            if application_data.version:
                application.version = application_data.version
            # If vulnerability input exists...    
            if vulnerability_data:
                vulnerability_object = CreateApplicationMutation.get_vulnerability_object_by_value(vulnerability_data.value)
                if vulnerability_object not in application.vulnerability:
                    application.vulnerability.append(vulnerability_object)
            application.save()
            return UpdateApplicationMutation(application=application)
        else:
            # Application does not exist
            if vulnerability_data:
                vulnerability_object = CreateApplicationMutation.get_vulnerability_object_by_value(vulnerability_data.value)
                application.vulnerability.append(vulnerability_object)
            application.save()
            return CreateApplicationMutation(application=application)

class UpdateApplicationMutation(graphene.Mutation):
    application = graphene.Field(ApplicationType)
    vulnerability = graphene.Field(VulnerabilityType)

    class Arguments:
        application_data = ApplicationInput(required=True)
        vulnerability_data = VulnerabilityInput(required=True)

    @staticmethod
    def get_vulnerability_object_by_value(exploitDbUrl):
        return Vulnerability.objects.get(exploitDbUrl=exploitDbUrl)   
  
    @staticmethod
    def get_object(id):
        return Application.objects.get(pk=id)

    def mutate(self, info, application_data=None, vulnerability_data=None):
        application = UpdateApplicationMutation.get_object(application_data.id)
        try:
            application_object = Application.objects.get(pk=application_data.id)
        except Application.DoesNotExist:
            application_object = None
        if application_object:
            # Application exists
            application = application_object
            if application_data.value:
                application.value = application_data.value
            if application_data.label:
                application.label = application_data.label
            if application_data.version:
                application.version = application_data.version
            application.save()
        return UpdateApplicationMutation(application=application)

class DeleteApplicationMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Application.objects(_id=id).delete()
            success = True
        except:
            success = False
        return DeleteApplicationMutation(success=success)