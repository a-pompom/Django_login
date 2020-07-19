from custom_auth.tests.fixture import multiple_users
import pytest # type: ignore

from .fixture import *

from ..backend import AuthBackend
from ..exceptions import LoginFailureException
from ..models import User

@pytest.mark.django_db(transaction=False)
class TestAuthBackend:
    """ 認証バックエンドテストコード
    """

    # PKによるユーザ取得
    class TestGetUser:
        """ get_userメソッドの検証 """
        
        def test_存在するユーザIDでUserが得られること(self, multiple_users):

            # GIVEN
            sut = AuthBackend()
            length = len(multiple_users)

            for i in range(length):

                # WHEN
                actual = sut.get_user(i+1)
                expected = User.objects.get(id=i+1)

                # THEN
                assert actual == expected

        def test_存在しないユーザIDでNoneが返ること(self, multiple_users):

            # GIVEN
            sut = AuthBackend()
            invalid_user_id_list = ['invalid userid', -999, 1.5]

            for invalid_user_id in invalid_user_id_list:

                # WHEN
                actual = sut.get_user(invalid_user_id)

                # THEN
                assert actual is None
        
    # 認証処理
    class TestAuthenticate:
        """ authenticateメソッドの検証 """
        def test_妥当なユーザ名とパスワードでUserが得られること(self, multiple_users):

            # GIVEN
            sut = AuthBackend()
            length = len(multiple_users)

            user_info = get_user_info_fixture()

            for i in range(length):

                # WHEN
                actual: User = sut.authenticate(None, username=user_info[i]['username'], password=user_info[i]['password'])
                expected_user = User.objects.get(username=user_info[i]['username'])

                # THEN
                assert actual == expected_user

        def test_存在しないユーザ名でLoginFailureExceptionが送出されること(self, multiple_users):

            # GIVEN
            sut = AuthBackend()

            # THEN
            with pytest.raises(LoginFailureException):
                # WHEN
                sut.authenticate(None, username='Nobody', password='mockPassword')

        def test_存在するユーザ名と誤ったパスワードでLoginFailureExceptionが送出されること(self, multiple_users):

            # GIVEN
            sut = AuthBackend()
            user_info = get_user_info_fixture()

            # THEN
            with pytest.raises(LoginFailureException):
                # WHEN
                sut.authenticate(None, username=user_info[0]['username'], password='invalidPassword')