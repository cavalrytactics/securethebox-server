import graphene
from app_models.models import Topic
from app_types.types import TopicType

class TopicInput(graphene.InputObjectType):
    ID = graphene.ID()
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
    def get_object(ID):
        return Topic.objects.get(pk=ID)
    def mutate(self, info, topic_data=None):
        topic = UpdateTopicMutation.get_object(topic_data.ID)
        if topic_data.value:
            topic.value = topic_data.value
        topic.save()
        return UpdateTopicMutation(topic=topic)

class DeleteTopicMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Topic.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteTopicMutation(success=success)