from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Question, Quiz, UserResult
from .serializers import (
    QuizSerializer,
    QuestionsSerializer,
    RegistrationSerializer,
    LoginSerializer,
    UserResultSerializer,
)
from datetime import datetime

permission_all = (AllowAny,)
permission_read = (IsAuthenticatedOrReadOnly,)
permission_admin = (IsAdminUser,)

schema_view = get_schema_view(
    openapi.Info(
        title="Quiz api",
        default_version="v1",
        description="Сваггер для апи опросов",
    ),
    public=True,
    permission_classes=permission_all,
)


class QuizView(ModelViewSet):

    permission_classes = permission_all
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def list(self, request):
        queryset = self.queryset.filter(date_start__lte=datetime.now(), date_finish__gte=datetime.now())
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class QuestionsView(ModelViewSet):

    permission_classes = permission_admin
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer


class UserResultsView(ModelViewSet):

    permission_classes = permission_all
    queryset = UserResult.objects.all()
    serializer_class = UserResultSerializer

    def retrieve(self, request, pk):
        print(request.META["REMOTE_ADDR"])
        user_results = self.queryset.filter(user=pk)
        result = self.serializer_class(user_results, many=True)
        return Response(result.data)


# Auth views


class RegistrationAPIView(APIView):

    permission_classes = permission_all
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        request_body=RegistrationSerializer,
        responses={"200": "OK", "400": "Bad Request"},
        security=[],
        operation_id="Register",
        operation_description="Создание нового пользователя, возвращает токен",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "token": serializer.data.get("token", None),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):

    permission_classes = permission_all
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={"200": "OK", "400": "Bad Request"},
        security=[],
        operation_id="Login",
        operation_description="Авторизация, возвращает токен",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
