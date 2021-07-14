from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include

from .views import *


router = DefaultRouter()
router.register(r"quiz", GetQuizInfoView, basename="quiz")

router.register(r"questions", GetQuestionsInfoView, basename="questions")

urlpatterns = [
    url(r"^", include(router.urls)),
]
