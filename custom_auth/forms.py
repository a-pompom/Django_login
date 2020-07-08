from django import forms
from django.core.exceptions import ValidationError

from .validator import * 
from .models import User

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
        error_messages = {
            'required': 'ユーザ名を入力してください。'
        }
    )

    # パスワード
    password = forms.CharField(
        error_messages = {
            'required': 'パスワードを入力してください。'
        }
    )

    def clean_username(self) -> str:
        """ ユーザ名バリデーション
        文字種別・ユニークチェックを実行

        Returns
        -------
        value: str
            バリデーション後のユーザ名文字列

        Raise
        -----
        ValidationError
            文字種別・ユニーク性を満たさなかったときに送出される
        """

        USERNAME_MIN_LENGTH = 5
        USERNAME_MAX_LENGTH = 32
        value: str = self.cleaned_data['username']

        if not value:
            return value

        # 文字種別
        if not is_valid_alpha_numeric(value):
            raise ValidationError('ユーザ名は半角英数または「-_」のみ使えます。')

        # 文字長
        if not is_valid_min_length(value, USERNAME_MIN_LENGTH):
            raise ValidationError(f'ユーザ名は{USERNAME_MIN_LENGTH}文字以上で入力してください。')
        if not is_valid_max_length(value, USERNAME_MAX_LENGTH):
            raise ValidationError(f'ユーザ名は{USERNAME_MAX_LENGTH}文字以下で入力してください。')

        # ユニーク
        if User.objects.filter(username=value).exists():
            raise ValidationError(f'ユーザ名はすでに使用されています。')

        return value

    def clean_password(self) -> str:
        """ パスワードバリデーション
        文字種別チェックを実行

        Returns
        -------
        value: str
            バリデーション後のパスワード文字列

        Raise
        -----
        ValidationError
            文字種別を満たさなかったときに送出される
        """

        PASSWORD_MIN_LENGTH = 10
        PASSWORD_MAX_LENGTH = 64
        value: str = self.cleaned_data['password']

        if not value:
            return value

        # 文字種別
        if not is_valid_alpha_numeric(value):
            raise ValidationError('パスワードは半角英数または「-_」のみ使えます。')

        # 文字長
        if not is_valid_min_length(value, PASSWORD_MIN_LENGTH):
            raise ValidationError(f'パスワードは{PASSWORD_MIN_LENGTH}文字以上で入力してください。')
        if not is_valid_max_length(value, PASSWORD_MAX_LENGTH):
            raise ValidationError(f'パスワードは{PASSWORD_MAX_LENGTH}文字以下で入力してください。')

        return value