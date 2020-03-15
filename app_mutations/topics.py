import graphene
from app_models.models import Topic
from app_types.types import TopicType

class TopicInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateTopicMutation(graphene.Mutation):
    topic = graphene.Field(TopicType)
    class Arguments:
        topic_data = TopicInput(required=True)
    def mutate(self, info, topic_data=None):
        topic = Topic(
            value=topic_data.value
        )
        topic.save()
        return CreateTopicMutation(topic=topic)

class UpdateTopicMutation(graphene.Mutation):
    topic = graphene.Field(TopicType)
    class Arguments:
        topic_data = TopicInput(required=True)
    @staticmethod
    def get_object(id):
        return Topic.objects.get(pk=id)
    def mutate(self, info, topic_data=None):
        topic = UpdateTopicMutation.get_object(topic_data.id)
        if topic_data.value:
            topic.value = topic_data.value
        topic.save()
        return UpdateTopicMutation(topic=topic)

class DeleteTopicMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Topic.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteTopicMutation(success=success)