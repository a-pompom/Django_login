from django import forms
from django.core.exceptions import ValidationError

from .validator import * 
from .models import User

USERNAME_MIN_LENGTH = 5
USERNAME_MAX_LENGTH = 32

PASSWORD_MIN_LENGTH = 10
PASSWORD_MAX_LENGTH = 64

class LoginForm(forms.Form):
    """ ログイン画面で利用するForm
    ログイン処理で入力項目をバリデーションするのは不自然なので、
    バリデーションはせず、認証処理のみを担う
    
    Attributes
    ----------
    username: CharField
        ユーザ名
    password: CharField
        パスワード
    """

    # ユーザ名
    username = forms.CharField()

    # パスワード
    password = forms.CharField()


class SignUpForm(forms.Form):
    """ ユーザ登録用Form

    Attributes
    ----------
    username: CharField
        ユーザ名 半角英数と-_で構成され、ユニーク
    password: CharField
        パスワード 半角英数と-_で構成される
    """

    # ユーザ名
    username = forms.CharField(
        validators=[
            get_validator(validate_min_length, USERNAME_MIN_LENGTH),
            get_validator(validate_max_length, USERNAME_MAX_LENGTH),
            get_validator(validate_alpha_numeric)
        ],
        error_messages = {
            'required': 'ユーザ名を入力してください。'
        }
    )

    # パスワード
    password = forms.CharField(
        validators=[
            get_validator(validate_min_length, PASSWORD_MIN_LENGTH),
            get_validator(validate_max_length, PASSWORD_MAX_LENGTH),
            get_validator(validate_alpha_numeric)
        ],
        error_messages = {
            'required': 'パスワードを入力してください。'
        }
    )

    def clean_username(self) -> str:
        """ ユーザ名バリデーション
        ユニークチェックを実行

        Returns
        -------
        value: str
            バリデーション後のユーザ名文字列

        Raise
        -----
        ValidationError
            ユニーク性を満たさなかったときに送出される
        """

        value: str = self.cleaned_data['username']

        if not value:
            return value

        # ユニーク
        if User.objects.filter(username=value).exists():
            raise ValidationError(f'ユーザ名はすでに使用されています。')

        return value