import graphene
from app_models.models import Metric
from app_types.types import MetricType

class MetricInput(graphene.InputObjectType):
    ID = graphene.ID()
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
    def get_object(ID):
        return Metric.objects.get(pk=ID)
    def mutate(self, info, metric_data=None):
        metric = UpdateMetricMutation.get_object(metric_data.ID)
        if metric_data.value:
            metric.value = metric_data.value
        metric.save()
        return UpdateMetricMutation(metric=metric)

class DeleteMetricMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Metric.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteMetricMutation(success=success)