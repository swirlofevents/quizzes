import jwt
from django.db.models import (
    Model,
    IntegerField,
    CharField,
    TextField,
    BooleanField,
    ForeignKey,
    DateTimeField,
    CASCADE,
)
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

from datetime import datetime, timedelta


class User(AbstractBaseUser, PermissionsMixin):

    username = CharField(db_index=True, max_length=255, unique=True)

    is_staff = BooleanField(default=False)

    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username

    def _generate_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.strftime("%S"))}, settings.SECRET_KEY, algorithm="HS256"
        )

        return token

    @property
    def token(self):
        """Определяем метод генерации токена как аттрибут
        для удобной работы
        """
        return self._generate_token()


class Quiz(Model):
    name = CharField(max_length=255)
    date_start = DateTimeField()
    date_finish = DateTimeField()
    description = TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"


class Questions(Model):

    TEXT = "TEXT"
    SINGLETONE = "SINGLETONE"
    MULTITONE = "MULTITONE"
    QUESTION_TYPE = (
        (TEXT, "TEXT"),
        (SINGLETONE, "SINGLETONE"),
        (MULTITONE, "MULTITONE"),
    )

    test = ForeignKey(Quiz, on_delete=CASCADE, related_name="questions")
    content = TextField()
    question_type = CharField(max_length=20, choices=QUESTION_TYPE, default=SINGLETONE)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answers(Model):
    content = TextField()
    question = ForeignKey(Questions, on_delete=CASCADE, related_name="answers")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


# class userResults(Model):
#     user = ForeignKey(User, on_delete=CASCADE)
#     test = ForeignKey(Quiz, on_delete=CASCADE)

#     class Meta:
#         verbose_name = "Результат опроса"
#         verbose_name_plural = "Результаты опросов"


# class User_Answers(Model):
#     answer = ForeignKey(Answers, on_delete=CASCADE)
#     question = ForeignKey(Questions, on_delete=CASCADE)
#     user = ForeignKey(User, on_delete=CASCADE)
#     userResult = ForeignKey(userResults, on_delete=CASCADE, related_name='userAnswers', blank=True)

#     class Meta:
#         verbose_name = "Ответ пользователя"
#         verbose_name_plural = "Ответы пользователей"
