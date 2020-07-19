import pytest # type: ignore
from typing import Dict
from django.core.exceptions import ValidationError

from ..forms import LoginForm, SignUpForm

from .fixture import *

class TestLoginForm:
    """ ログイン画面用Formのテスト 入力要素が存在するかのみを検証 """

    def test_初期状態にFieldとしてユーザ名_パスワードが存在すること(self):

        # GIVEN
        login_form = LoginForm()

        # THEN
        assert login_form['username'] is not None
        assert login_form['password'] is not None


@pytest.mark.django_db(transaction=False) # transaction=Falseでテストコード実行で利用したDBトランザクションをコミットしないよう設定
class TestSignUpForm:
    """ ユーザ登録画面用Formのテスト 入力要素の存在・バリデーション処理の妥当性を検証 """

    def test_Formの初期状態にFieldとしてユーザ名_パスワードが存在すること(self):

        # GIVEN
        signup_form = SignUpForm()

        
        # THEN
        assert signup_form['username'] is not None
        assert signup_form['password'] is not None


    @pytest.mark.parametrize(
        'cleaned_username',
        [
            pytest.param({'username': 'a-pompom105a'}, id='valid username'),
            pytest.param({'username': '12345'}, id='Equal to valid min length'),
            pytest.param({'username': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef'}, id='Equal to valid max length'),
        ]
    )
    def test_Formへ有効なユーザ名を渡すとcleaned_dataへユーザ名が格納されること(self, cleaned_username: Dict[str,str]):

        # GIVEN
        signup_form = SignUpForm()

        # WHEN
        signup_form.cleaned_data = cleaned_username
        signup_form.clean_username()

        # THEN
        assert signup_form.cleaned_data['username'] == cleaned_username['username']

    @pytest.mark.parametrize(
        'invalid_username',
        [
            pytest.param({'username': 'a-pompom 105a'}, id='Invalid username'),
            pytest.param({'username': '1234'}, id='Less than valid min length'),
            pytest.param({'username': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg'}, id='More than valid max length'),
            pytest.param({'username': 'a-pompom0107'}, id='Duplicate username'),
        ]
    )
    def test_SignUpFormへ無効なユーザ名を渡すとValidationErrorが送出されること(self, invalid_username: Dict[str,str], multiple_users):

        # GIVEN
        signup_form = SignUpForm()

        # THEN
        with pytest.raises(ValidationError):
            # WHEN
            signup_form.cleaned_data = invalid_username
            signup_form.clean_username()


    @pytest.mark.parametrize(
        'cleaned_password',
        [
            pytest.param({'password': 'invalid password'}, id='Invalid Character Type'),
            pytest.param({'password': 'min'}, id='Invalid min length'),
            pytest.param({'password': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-_________________'}, id='Invalid max length'),
        ]
    )
    def test_SignUpFormへ無効なパスワードを渡すとValidationErrorが送出されること(self, cleaned_password: Dict[str,str]):

        # GIVEN
        signup_form = SignUpForm({'username': 'mockUser', 'password': 'mockPassword'})
        
        # THEN
        with pytest.raises(ValidationError):
            # WHEN
            signup_form.cleaned_data = cleaned_password

            signup_form.clean_password()