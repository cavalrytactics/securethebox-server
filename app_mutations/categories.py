import graphene
from app_models.models import Category
from app_types.types import CategoryType

class CategoryInput(graphene.InputObjectType):
    ID = graphene.ID()
    label = graphene.String()
    value = graphene.String()
    color = graphene.String()

class CreateCategoryMutation(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        category_data = CategoryInput(required=True)
    
    @staticmethod
    def check_exists(value):
        allObjects = Category.objects.all()
        for item in allObjects:
            if item.value == value:
                return True
        return False

    def mutate(self, info, category_data=None):
        exists = CreateCategoryMutation.check_exists(category_data.value)
        category = Category(
            label=category_data.label,
            value=category_data.value,
            color=category_data.color,
        )
        if exists == False:
            category.save()
        return CreateCategoryMutation(category=category)

class UpdateCategoryMutation(graphene.Mutation):
    category = graphene.Field(CategoryType)
    class Arguments:
        category_data = CategoryInput(required=True)
    @staticmethod
    def get_object(ID):
        return Category.objects.get(pk=ID)
    def mutate(self, info, category_data=None):
        category = UpdateCategoryMutation.get_object(category_data.ID)
        if category_data.label:
            category.label = category_data.label
        if category_data.value:
            category.value = category_data.value
        if category_data.color:
            category.color = category_data.color
        category.save()
        return UpdateCategoryMutation(category=category)

class DeleteCategoryMutation(graphene.Mutation):
    class Arguments:
        ID = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, ID):
        try:
            Category.objects.get(pk=ID).delete()
            success = True
        except:
            success = False
        return DeleteCategoryMutation(success=success)