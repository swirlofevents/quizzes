from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Questions, Quiz
from .serializers import QuizSerializer, QuestionsSerializer, RegistrationSerializer, LoginSerializer
from datetime import datetime

permission = (AllowAny,)


class GetQuizInfoView(ModelViewSet):

    permission_classes = permission
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def list(self, request):
        queryset = self.queryset.filter(date_start__lte=datetime.now(), date_finish__gte=datetime.now())
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class GetQuestionsInfoView(ModelViewSet):

    permission_classes = permission
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer


# Auth views


class RegistrationAPIView(APIView):

    permission_classes = permission
    serializer_class = RegistrationSerializer

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

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
