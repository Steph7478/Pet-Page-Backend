from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username
        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        return getattr(user, 'is_active', True)
