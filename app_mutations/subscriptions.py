import graphene
from app_models.models import Subscription
from app_types.types import SubscriptionType

class SubscriptionInput(graphene.InputObjectType):
    ID = graphene.ID()
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
    def get_object(ID):
        return Subscription.objects.get(pk=ID)
    def mutate(self, info, subscription_data=None):
        subscription = UpdateSubscriptionMutation.get_object(subscription_data.ID)
        if subscription_data.value:
            subscription.value = subscription_data.value
        subscription.save()
        return UpdateSubscriptionMutation(subscription=subscription)

class DeleteSubscriptionMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Subscription.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteSubscriptionMutation(success=success)