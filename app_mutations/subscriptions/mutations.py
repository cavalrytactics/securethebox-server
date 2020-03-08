import graphene
from app_models.graphql.models import Subscription
from app_types.types import SubscriptionType

class SubscriptionInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateSubscriptionMutation(graphene.Mutation):
    subscription = graphene.Field(SubscriptionType)
    class Arguments:
        subscription_data = SubscriptionInput(required=True)
    def mutate(self, info, subscription_data=None):
        subscription = Subscription(
            value=subscription_data.value
        )
        subscription.save()
        return CreateSubscriptionMutation(subscription=subscription)

class UpdateSubscriptionMutation(graphene.Mutation):
    subscription = graphene.Field(SubscriptionType)
    class Arguments:
        subscription_data = SubscriptionInput(required=True)
    @staticmethod
    def get_object(id):
        return Subscription.objects.get(pk=id)
    def mutate(self, info, subscription_data=None):
        subscription = UpdateSubscriptionMutation.get_object(subscription_data.id)
        if subscription_data.value:
            subscription.value = subscription_data.value
        subscription.save()
        return UpdateSubscriptionMutation(subscription=subscription)

class DeleteSubscriptionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Subscription.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteSubscriptionMutation(success=success)