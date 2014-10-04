from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class NfcAuthBackend(ModelBackend):
    # Allows login without providing a password
    def authenticate(self, no_password=False, username=None, password=None, **kwargs):
        # make sure it was intentional
        if not no_password:
            return None
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None