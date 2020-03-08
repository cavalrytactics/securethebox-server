import graphene
from app_models.graphql.models import Service, Application
from app_types.types import ServiceType, ApplicationType
from app_mutations.applications.mutations import ApplicationInput

class ServiceInput(graphene.InputObjectType):
    id = graphene.ID()
    label = graphene.String()
    value = graphene.String()
    type = graphene.String()

class CreateServiceMutation(graphene.Mutation):
    service = graphene.Field(ServiceType)
    application = graphene.Field(ApplicationType)
    class Arguments:
        service_data = ServiceInput(required=True)
        application_data = ApplicationInput(required=False)

    @staticmethod
    def get_application_object_by_value(value):
        return Application.objects.get(value=value) 

    def mutate(self, info, service_data=None, application_data=None):
        # 1-1 service -> application
        # should it be application -> service? probably
        application = CreateServiceMutation.get_application_object_by_value(application_data.value)
        service = Service(
            label=service_data.label,
            value=service_data.value,
            type=service_data.type,
            applications=[application]
        )
        try:
            service_object = Service.objects.get(title=service_data.value)
        except Service.DoesNotExist:
            service_object = None
        if service_object:
            # Service exists
            service = service_object
            if service_data.label:
                service.label = service_data.label
            if service_data.value:
                service.value = service_data.value
            if service_data.serviceType:
                service.serviceType = service_data.serviceType
            if application_data.value:
                if application not in service.applications:
                    service.applications.append(application)
            service.save()
            return UpdateServiceMutation(service=service)
        else:
            # Service does not exist
            service.save()
            return CreateServiceMutation(service=service)
        

class UpdateServiceMutation(graphene.Mutation):
    service = graphene.Field(ServiceType)
    application = graphene.Field(ApplicationType)
    class Arguments:
        service_data = ServiceInput(required=True)
    @staticmethod
    def get_service_object(id):
        return Service.objects.get(pk=id)
    def mutate(self, info, service_data=None):
        service = UpdateServiceMutation.get_service_object(service_data.id)
        if service_data.value:
            service.value = service_data.value
        service.save()
        return UpdateServiceMutation(service=service)

class UpdateServiceAddApplicationMutation(graphene.Mutation):
    service = graphene.Field(ServiceType)
    application = graphene.Field(ApplicationType)
    class Arguments:
        service_data = ServiceInput(required=True)
        application_data = ApplicationInput(required=False)
    @staticmethod
    def get_service_object(id):
        return Service.objects.get(pk=id)
    def get_application_object(id):
        return Application.objects.get(pk=id)
    def mutate(self, info, service_data=None, application_data=None):
        service = UpdateServiceAddApplicationMutation.get_service_object(service_data.id)
        application = UpdateServiceAddApplicationMutation.get_application_object(application_data.id)
        if service_data.value:
            service.value = service_data.value
        if application_data.value:
            if application not in service.applications:
                service.applications.append(application)
        service.save()
        return UpdateServiceAddApplicationMutation(service=service)

class UpdateServiceDeleteApplicationMutation(graphene.Mutation):
    service = graphene.Field(ServiceType)
    application = graphene.Field(ApplicationType)
    class Arguments:
        service_data = ServiceInput(required=True)
        application_data = ApplicationInput(required=False)
    @staticmethod
    def get_service_object(id):
        return Service.objects.get(pk=id)
    def get_application_object(id):
        return Application.objects.get(pk=id)
    def mutate(self, info, service_data=None, application_data=None):
        service = UpdateServiceDeleteApplicationMutation.get_service_object(service_data.id)
        application = UpdateServiceDeleteApplicationMutation.get_application_object(application_data.id)
        if service_data.value:
            service.value = service_data.value
        if application_data.value:
            if application in service.applications:
                service.applications.remove(application)
        service.save()
        return UpdateServiceAddApplicationMutation(service=service)

class DeleteServiceMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Service.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteServiceMutation(success=success)