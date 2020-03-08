import graphene
from app_models.graphql.models import Metric
from app_types.types import MetricType

class MetricInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateMetricMutation(graphene.Mutation):
    metric = graphene.Field(MetricType)
    class Arguments:
        metric_data = MetricInput(required=True)
    def mutate(self, info, metric_data=None):
        metric = Metric(
            value=metric_data.value
        )
        metric.save()
        return CreateMetricMutation(metric=metric)

class UpdateMetricMutation(graphene.Mutation):
    metric = graphene.Field(MetricType)
    class Arguments:
        metric_data = MetricInput(required=True)
    @staticmethod
    def get_object(id):
        return Metric.objects.get(pk=id)
    def mutate(self, info, metric_data=None):
        metric = UpdateMetricMutation.get_object(metric_data.id)
        if metric_data.value:
            metric.value = metric_data.value
        metric.save()
        return UpdateMetricMutation(metric=metric)

class DeleteMetricMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Metric.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteMetricMutation(success=success)