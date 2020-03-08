import graphene
from app_models.graphql.models import Configuration
from app_types.types import ConfigurationType

class ConfigurationInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateConfigurationMutation(graphene.Mutation):
    configuration = graphene.Field(ConfigurationType)
    class Arguments:
        configuration_data = ConfigurationInput(required=True)
    def mutate(self, info, configuration_data=None):
        configuration = Configuration(
            value=configuration_data.value
        )
        configuration.save()
        return CreateConfigurationMutation(configuration=configuration)

class UpdateConfigurationMutation(graphene.Mutation):
    configuration = graphene.Field(ConfigurationType)
    class Arguments:
        configuration_data = ConfigurationInput(required=True)
    @staticmethod
    def get_object(id):
        return Configuration.objects.get(pk=id)
    def mutate(self, info, configuration_data=None):
        configuration = UpdateConfigurationMutation.get_object(configuration_data.id)
        if configuration_data.value:
            configuration.value = configuration_data.value
        configuration.save()
        return UpdateConfigurationMutation(configuration=configuration)

class DeleteConfigurationMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Configuration.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteConfigurationMutation(success=success)