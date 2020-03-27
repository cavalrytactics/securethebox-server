import graphene
from app_models.models import Plan, Company
from app_types.types import PlanType, CompanyType
from app_mutations.companies import CompanyInput
from bson import ObjectId


class PlanInput(graphene.InputObjectType):
    ID = graphene.ID()
    name = graphene.String()
    description = graphene.String()
    duration = graphene.String()  # trial/monthly/yearly/free
    business = graphene.Boolean()
    education = graphene.Boolean()
    maxParticipants = graphene.Int()
    usageStartTime = graphene.String()  # time when purchased
    usageRelativeTime = graphene.String()  # time after purchase
    # reference: https://marketplace.zoom.us/docs/api-reference/other-references/plans

class CreatePlanMutation(graphene.Mutation):
    plan = graphene.Field(PlanType)

    class Arguments:
        plan_data = PlanInput(required=True)

    @staticmethod
    def get_plan_object_by_ID(ID):
        return Plan.objects.get(pk=ID)

    def mutate(self, info, plan_data=None):
        plan = Plan(
            name=plan_data.name,
            description=plan_data.description,
            duration=plan_data.duration,
            business=plan_data.business,
            education=plan_data.education,
            maxParticipant=plan_data.maxParticipant,
            usageStartTime=plan_data.usageStartTime,
            usageRelativeTime=plan_data.usageRelativeTime,
        )

        try:
            plan_object = Plan.objects.get(pk=plan_data.ID)
        except Plan.DoesNotExist:
            plan_object = None
        if plan_object:
            plan = plan_object
            if plan_data.name:
                plan.name = plan_data.name
            if plan_data.description:
                plan.description = plan_data.description
            if plan_data.duration:
                plan.duration = plan_data.duration
            if plan_data.business:
                plan.business = plan_data.business
            if plan_data.education:
                plan.education = plan_data.education
            if plan_data.maxParticipant:
                plan.maxParticipant = plan_data.maxParticipant
            if plan_data.usageStartTime:
                plan.usageStartTime = plan_data.usageStartTime
            if plan_data.usageRelativeTime:
                plan.usageRelativeTime = plan_data.usageRelativeTime
            plan.save()
            return CreatePlanMutation(plan=plan)
        else:
            plan.ID = ObjectId()
            plan.save()
            return CreatePlanMutation(plan=plan)

class UpdatePlanMutation(graphene.Mutation):
    plan = graphene.Field(PlanType)
    company = graphene.Field(CompanyType)

    class Arguments:
        plan_data = PlanInput(required=True)

    @staticmethod
    def get_plan_object_by_ID(ID):
        return Plan.objects.get(pk=ID)

    @staticmethod
    def get_company_object_by_ID(ID):
        return Company.objects.get(pk=ID)

    def mutate(self, info, plan_data=None):
        plan = UpdatePlanMutation.get_plan_object_by_ID(plan_data.ID)

        try:
            plan_object = Plan.objects.get(pk=plan_data.ID)
        except Plan.DoesNotExist:
            plan_object = None
        if plan_object:
            plan = plan_object
            if plan_data.name:
                plan.name = plan_data.name
            if plan_data.description:
                plan.description = plan_data.description
            if plan_data.duration:
                plan.duration = plan_data.duration
            if plan_data.business:
                plan.business = plan_data.business
            if plan_data.education:
                plan.education = plan_data.education
            if plan_data.maxParticipant:
                plan.maxParticipant = plan_data.maxParticipant
            if plan_data.usageStartTime:
                plan.usageStartTime = plan_data.usageStartTime
            if plan_data.usageRelativeTime:
                plan.usageRelativeTime = plan_data.usageRelativeTime
            plan.save()
        return UpdatePlanMutation(plan=plan)

class DeletePlanMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()

    def mutate(self, info, ID):
        try:
            Plan.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeletePlanMutation(success=success)
