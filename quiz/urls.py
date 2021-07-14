from django.urls import re_path
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include

from .views import *


router = DefaultRouter()
router.register(r"quiz", QuizView, basename="quiz")
router.register(r"questions", QuestionsView, basename="questions")
router.register(r"userResult", UserResultsView, basename="user_results")

urlpatterns = [
    url(r"^", include(router.urls)),
    re_path(r"^registration/?$", RegistrationAPIView.as_view(), name="user_registration"),
    re_path(r"^login/?$", LoginAPIView.as_view(), name="user_login"),
]
