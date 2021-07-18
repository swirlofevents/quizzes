import jwt

from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class UserAuthenticate(authentication.BaseAuthentication):
    authentication_header_prefix = "Bearer"

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) > 2:
            """Неверный заголовок токена. Учетные данные не предоставлены"""
            return None

        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix.lower() != auth_header_prefix:
            """Неверный префикс заголвка"""
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm="HS256")
        except:
            raise exceptions.AuthenticationFailed("Неверный токен")

        try:
            user = User.objects.get(pk=payload["id"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Пользователь не найден")

        return (user, token)
