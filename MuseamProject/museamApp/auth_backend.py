from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.contrib.auth.hashers import check_password

from museamApp.models import User


class CustomBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        login = username  # использует поле login вместо username
        try:
            user = User.objects.get(login=login)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None