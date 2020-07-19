import pytest
from django.contrib.auth.hashers import make_password

from ..models import User

# テストユーザ情報
def get_user_info_fixture():

    user_info = [
        {'username': 'a-pompom0107', 'password': 'strong_password1234', 'is_admin': True},
        {'username': 'johnDoe__9807', 'password': 'mYPoWErfUl00PaSSwoRd', 'is_admin': False},
        {'username': 'pompomPurin0001', 'password': 'purinPompom0001', 'is_admin': False},
    ]
    return user_info

# テストユーザをfixtureで生成
@pytest.fixture()
def multiple_users():
    user_info = get_user_info_fixture()

    return tuple(
        User.objects.create(
            username=user_dict['username'],
            password=make_password(user_dict['password']),
            is_admin=user_dict['is_admin']
        ) for user_dict in user_info
    )