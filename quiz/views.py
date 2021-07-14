from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Questions, Quiz
from .serializers import QuizSerializer, QuestionsSerializer
from datetime import datetime

permission = (permissions.AllowAny,)


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
