import graphene
from app_models.models import Application, Vulnerability
from app_types.types import ApplicationType, VulnerabilityType
from app_mutations.vulnerabilities import VulnerabilityInput
from bson import ObjectId 

class ApplicationInput(graphene.InputObjectType):
    ID = graphene.ID()
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
            app = application_object
            if application_data.value:
                app.value = application_data.value
            if application_data.label:
                app.label = application_data.label
            if application_data.version:
                app.version = application_data.version
            # If vulnerability input exists...    
            if vulnerability_data:
                vulnerability_object = CreateApplicationMutation.get_vulnerability_object_by_value(vulnerability_data.value)
                if vulnerability_object not in app.vulnerability:
                    app.vulnerability.append(vulnerability_object)
            app.save()
            return UpdateApplicationMutation(application=app)
        else:
            # Application does not exist
            application.ID = ObjectId()
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
    def get_object(ID):
        return Application.objects.get(pk=ID)

    def mutate(self, info, application_data=None, vulnerability_data=None):
        application = UpdateApplicationMutation.get_object(application_data.ID)
        try:
            application_object = Application.objects.get(pk=application_data.ID)
        except Application.DoesNotExist:
            application_object = application
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
        ID = graphene.ID()
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            app = Application.objects.all()
            success = False
            for a in app:
                if str(ID) == str(a.ID):
                    a.delete()
                    success = True
            return DeleteApplicationMutation(success=success)
        except:
            success = False
            return DeleteApplicationMutation(success=success)