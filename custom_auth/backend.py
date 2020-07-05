from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

from .models import User

class AuthBackend(BaseBackend):

    def get_user(self, user_id):
        print('get_user called')
        print(user_id)

        user = User.objects.get(id=user_id)
        
        return user

    def authenticate(self, request, username=None, password=None):
        print('authenticate called')

        try:

            user = User.objects.get(username=username)
            print('user')
            print(user)

        except User.DoesNotExist:
            print('user does not exist')
            return None

        is_valid_password = check_password(password, user.password)

        if not is_valid_password:
            return None
        
        return user