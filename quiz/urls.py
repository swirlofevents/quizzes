from django.urls import re_path
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include

from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r"quiz", QuizView, basename="quiz")
router.register(r"questions", QuestionsView, basename="questions")
router.register(r"userResult", UserResultsView, basename="user_results")
schema_view = get_schema_view(
    openapi.Info(
        title="Quiz api",
        default_version="v1",
        description="Сваггер для апи опросов",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    url(r"^", include(router.urls)),
    re_path(r"^registration/?$", RegistrationAPIView.as_view(), name="user_registration"),
    re_path(r"^login/?$", LoginAPIView.as_view(), name="user_login"),
    url(r"^doc(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    url(r"^doc/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    url(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
