import graphene
from app_models.graphql.models import Cluster
from app_types.types import ClusterType

class ClusterInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    status = graphene.String()

class CreateClusterMutation(graphene.Mutation):
    cluster = graphene.Field(ClusterType)
    class Arguments:
        cluster_data = ClusterInput(required=True)
    def mutate(self, info, cluster_data=None):
        cluster = Cluster(
            name=cluster_data.name,
            status=cluster_data.status
        )
        cluster.save()
        return CreateClusterMutation(cluster=cluster)

class UpdateClusterMutation(graphene.Mutation):
    cluster = graphene.Field(ClusterType)
    class Arguments:
        cluster_data = ClusterInput(required=True)
    @staticmethod
    def get_object(id):
        return Cluster.objects.get(pk=id)
    def mutate(self, info, cluster_data=None):
        cluster = UpdateClusterMutation.get_object(cluster_data.id)
        if cluster_data.name:
            cluster.name = cluster_data.name
        if cluster_data.status:
            cluster.status = cluster_data.status
        cluster.save()
        return UpdateClusterMutation(cluster=cluster)

class DeleteClusterMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Cluster.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteClusterMutation(success=success)