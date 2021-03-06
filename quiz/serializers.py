from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    Serializer,
    ValidationError,
    IntegerField,
)
from .models import Quiz, Question, Answer, User, UserResult, UserAnswer
from drf_writable_nested import WritableNestedModelSerializer
from django.contrib.auth import authenticate


# Отдельный класс сериализации для результатов
class UserForResultsSerializer(ModelSerializer):

    id = IntegerField(label="ID")
    username = CharField(max_length=255)

    class Meta:
        model = User
        fields = ("id", "username")

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class AnswersSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "content")


class QuestionsSerializer(WritableNestedModelSerializer, ModelSerializer):
    """Список вопросов"""

    answers = AnswersSerializer(many=True)

    class Meta:
        model = Question
        fields = ("id", "content", "question_type", "answers")


class QuizSerializer(WritableNestedModelSerializer, ModelSerializer):

    questions = QuestionsSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ("id", "name", "date_start", "date_finish", "description", "questions")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # запрет на изменение
        if self.instance is not None:
            self.fields.get("date_start").read_only = True


class UserAnswerSerializer(ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = "__all__"


class UserResultSerializer(WritableNestedModelSerializer, ModelSerializer):

    user = UserForResultsSerializer()
    answers = UserAnswerSerializer(many=True)

    class Meta:
        model = UserResult
        fields = ("user", "quiz", "answers")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.filter(id=user_data.get("id")).first()
        quiz = validated_data.pop("quiz")
        # Проверка на пользователя, если его не существует, создается новый анонимный
        if not user:
            user = UserForResultsSerializer.create(UserForResultsSerializer(), user_data)
        # Проверка на опрос, его обязательно нужно передать
        if not quiz:
            raise ValidationError("Опрос не может быть пустым")
        user_result = UserResult.objects.create(user=user, quiz=quiz)
        answers = validated_data.pop("answers")
        for answer in answers:
            UserAnswer.objects.create(user_result=user_result, **answer)
        return user_result


# Auth/reg serializers


class RegistrationSerializer(ModelSerializer):

    username = CharField(max_length=255, min_length=3, write_only=True)
    password = CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    token = CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "token",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(Serializer):

    username = CharField(max_length=255, write_only=True)
    password = CharField(max_length=128, write_only=True)

    token = CharField(max_length=255, read_only=True)

    def validate(self, data):

        username = data.get("username", None)
        password = data.get("password", None)

        if username is None:
            raise ValidationError("Не введено имя пользователя.")

        if password is None:
            raise ValidationError("Не введен пароль.")

        user = authenticate(username=username, password=password)

        if user is None:
            raise ValidationError("Пользователь с таким именем и паролем не найден")

        return {
            "token": user.token,
        }
