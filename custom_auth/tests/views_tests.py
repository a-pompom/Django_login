from django.http import HttpResponse, HttpResponseRedirect
from django.test import Client
from django.urls import reverse_lazy

import pytest # type: ignore
from typing import TypedDict

from .fixture import *

from ..views import *


class Props(TypedDict):
    """ テストで利用するプロパティ型 """
    client: Client
    login_path: str
    sign_up_path: str
    top_path: str
    logout_path: str

# テストで利用するプロパティ生成
@pytest.fixture()
def props() -> Props:

    return {
        'client': Client(),
        'login_path': reverse_lazy('login:login'),
        'sign_up_path': reverse_lazy('login:signup'),
        'top_path': reverse_lazy('login:top'),
        'logout_path': reverse_lazy('login:logout'),
    }
@pytest.mark.django_db(transaction=False)
class TestView:

    class TestLoginView:
        """ ログイン画面View """

        class TestGet:
            """ ログイン画面へのGETリクエスト """
            def test_ステータス200が返ること(self, props: Props):

                # WHEN
                response: HttpResponse = props['client'].get(props['login_path'])

                # THEN
                assert response.status_code == 200
            
            def test_ログイン画面のテンプレートが得られること(self, props: Props):

                # WHEN
                response: HttpResponse = props['client'].get(props['login_path'])

                # THEN
                assert '<title>ログイン</title>' in response.content.decode('utf-8')

        class TestPost:
            """ ログイン画面へのPOSTリクエスト """
            def test_ログイン成功するとTop画面へ遷移すること(self, props: Props, multiple_users):

                # GIVEN
                post_params = {
                    'username': 'a-pompom0107',
                    'password': 'strong_password1234',
                }

                # WHEN
                response: HttpResponseRedirect = props['client'].post(props['login_path'], post_params)

                # THEN
                assert props['top_path'] == response['Location']

            def test_日本語でユーザ名とパスワードを指定するとログイン画面へ遷移すること(self, props: Props, multiple_users):

                # GIVEN
                post_params = {
                    'username': 'ユーザ',
                    'password': 'パスワード',
                }

                # WHEN
                response: HttpResponse = props['client'].post(props['login_path'], post_params)

                # THEN
                assert '<title>ログイン</title>' in response.content.decode('utf-8')

            def test_存在しないユーザ名を指定するとログイン画面へ遷移すること(self, props: Props, multiple_users):

                # GIVEN
                post_params = {
                    'username': 'nobody',
                    'password': 'validPasswordString',
                }

                # WHEN
                response: HttpResponse = props['client'].post(props['login_path'], post_params)

                # THEN
                assert '<title>ログイン</title>' in response.content.decode('utf-8')

            def test_存在するユーザ名で間違ったパスワードを指定するとログイン画面へ遷移すること(self, props: Props, multiple_users):

                # GIVEN
                post_params = {
                    'username': 'a-pompom0107',
                    'password': 'validButIncorrectPassword',
                }

                # WHEN
                response: HttpResponse = props['client'].post(props['login_path'], post_params)

                # THEN
                assert '<title>ログイン</title>' in response.content.decode('utf-8')


    class TestSignUpView:
        """ ユーザ登録画面View """

        class TestGet:
            """ ユーザ登録画面へのGETリクエスト """
            def test_ステータス200が返ること(self, props: Props):

                # WHEN
                response: HttpResponse = props['client'].get(props['sign_up_path'])

                # THEN
                assert response.status_code == 200

            def test_ユーザ登録画面のテンプレートが得られること(self, props: Props):

                # WHEN
                response: HttpResponse = props['client'].get(props['sign_up_path'])

                # THEN
                assert '<title>ユーザ登録</title>' in response.content.decode('utf-8')

        class TestPost:
            """ ユーザ登録画面へのPOSTリクエスト """
            def test_ユーザ登録に成功するとログイン画面へリダイレクトすること(self, props: Props):

                # GIVEN
                post_params = {
                    'username': 'a-pompom_User',
                    'password': 'veryStrong-Password0001',
                }

                # WHEN
                response: HttpResponseRedirect = props['client'].post(props['sign_up_path'], post_params)

                # THEN
                assert props['login_path'] == response['Location']

            def test_ユーザ登録に成功するとDBへユーザが登録されること(self, props: Props):

                post_params = {
                    'username': 'a-pompom_User',
                    'password': 'veryStrong-Password0001',
                }

                # GIVEN
                props['client'].post(props['sign_up_path'], post_params)

                # WHEN
                created_user = User.objects.get(username=post_params['username'])

                # THEN
                assert created_user.username == post_params['username']

            def test_日本語でユーザ名とパスワードを指定するとユーザ登録画面へ遷移すること(self, props: Props):

                # GIVEN
                post_params = {
                    'username': 'ユーザ',
                    'password': 'パスワード',
                }

                # WHEN
                response: HttpResponse = props['client'].post(props['sign_up_path'], post_params)

                # THEN
                assert '<title>ユーザ登録</title>' in response.content.decode('utf-8')

            def test_存在するユーザ名で登録するとユーザ登録画面へ遷移すること(self, props: Props, multiple_users):

                # GIVEN
                post_params = {
                    'username': 'a-pompom0107',
                    'password': 'strongMockPassword_1234'
                }

                # WHEN
                response: HttpResponse = props['client'].post(props['sign_up_path'], post_params)

                # THEN
                assert '<title>ユーザ登録</title>' in response.content.decode('utf-8')


    class TestTopView:
        """ TOP画面View """

        class TestGet:
            """ TOP画面へのGETリクエスト """

            def test_AdminユーザでTOP画面へアクセスすると管理者用トップ画面へ遷移すること(self, props: Props, multiple_users):

                # GIVEN
                props['client'].login(username='a-pompom0107', password='strong_password1234')

                # WHEN
                response: HttpResponse = props['client'].get(props['top_path'])

                # THEN
                assert '<title>管理者TOP</title>' in response.content.decode('utf-8')

            def test_Admin以外のユーザでTOP画面へアクセスするとユーザTOP画面へ遷移すること(self, props: Props, multiple_users):

                # GIVEN
                props['client'].login(username='johnDoe__9807', password='mYPoWErfUl00PaSSwoRd')

                # WHEN
                response: HttpResponse = props['client'].get(props['top_path'])

                # THEN
                assert '<title>ユーザTOP</title>' in response.content.decode('utf-8')

            def test_未ログインユーザでTOP画面へアクセスするとログイン画面へ遷移すること(self, props: Props):

                # WHEN
                response: HttpResponseRedirect = props['client'].get(props['top_path'])

                # THEN
                assert props['login_path'] == response['Location']


    class TestLogoutView:
        """ ログアウトView """

        class TestGet:
            """ ログアウトViewへのGETリクエスト """

            def test_ログイン済みユーザがログアウトするとログイン画面へ遷移すること(self, props: Props, multiple_users):

                # GIVEN
                props['client'].login(username='a-pompom0107', password='strong_password1234')
                # WHEN
                response: HttpResponseRedirect = props['client'].get(props['logout_path'])

                # THEN
                assert props['login_path'] == response['Location']
                

            def test_ログイン済みユーザがログアウト後にTOP画面へアクセスするとログイン画面へ遷移すること(self, props: Props, multiple_users):

                # GIVEN
                props['client'].login(username='a-pompom0107', password='strong_password1234')
                # WHEN
                props['client'].get(props['logout_path'])
                response: HttpResponseRedirect = props['client'].get(props['top_path'])

                # THEN
                assert props['login_path'] == response['Location']

            def test_未ログインユーザがログアウト画面へアクセスするとログイン画面へ遷移すること(self, props: Props, multiple_users):

                # WHEN
                response: HttpResponseRedirect = props['client'].get(props['logout_path'])

                # THEN
                assert props['login_path'] == response['Location']

    class Test404View:
        """ 404エラーView """

        class TestGet:
            """ 存在しないパスへのGETリクエスト """

            def test_存在しないURLへリクエストするとステータス404が返ること(self, props: Props):

                # WHEN
                response: HttpResponse = props['client'].get('/login/nothing/urll')

                # THEN
                assert response.status_code == 404

            def test_存在しないURLへリクエストすると404エラー画面へ遷移すること(self, props: Props):

                # WHEN
                response: HttpResponse = props['client'].get('/login/nothing/urll')

                # THEN
                assert '404' in response.content.decode('utf-8')