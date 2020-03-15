import graphene
from app_models.models import Question
from app_types.types import QuestionType

class QuestionInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    value = graphene.String()

class CreateQuestionMutation(graphene.Mutation):
    question = graphene.Field(QuestionType)
    class Arguments:
        question_data = QuestionInput(required=True)
    def mutate(self, info, question_data=None):
        question = Question(
            value=question_data.value
        )
        question.save()
        return CreateQuestionMutation(question=question)

class UpdateQuestionMutation(graphene.Mutation):
    question = graphene.Field(QuestionType)
    class Arguments:
        question_data = QuestionInput(required=True)
    @staticmethod
    def get_object(id):
        return Question.objects.get(pk=id)
    def mutate(self, info, question_data=None):
        question = UpdateQuestionMutation.get_object(question_data.id)
        if question_data.value:
            question.value = question_data.value
        question.save()
        return UpdateQuestionMutation(question=question)

class DeleteQuestionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id):
        try:
            Question.objects.get(pk=id).delete()
            success = True
        except:
            success = False
        return DeleteQuestionMutation(success=success)