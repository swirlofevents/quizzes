from rest_framework.serializers import ModelSerializer
from .models import Quiz, Questions, Answers
from drf_writable_nested import WritableNestedModelSerializer


class AnswersSerializer(ModelSerializer):
    class Meta:
        model = Answers
        fields = ("id", "content")


class QuestionsSerializer(WritableNestedModelSerializer, ModelSerializer):
    """Список вопросов"""

    answers = AnswersSerializer(many=True)

    class Meta:
        model = Questions
        fields = ("id", "content", "question_type", "answers")


class QuizSerializer(WritableNestedModelSerializer, ModelSerializer):

    questions = QuestionsSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ("id", "name", "date_start", "date_finish", "description", "questions")
