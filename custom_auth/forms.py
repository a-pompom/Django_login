from django import forms
from django.core.exceptions import ValidationError

from .validator import * 
from .models import User

class LoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField()


class SignUpForm(forms.Form):

    username = forms.CharField(
        error_messages = {
            'required': 'ユーザ名を入力してください。'
        }
    )

    password = forms.CharField(
        error_messages = {
            'required': 'パスワードを入力してください。'
        }
    )

    def clean_username(self) -> str:

        USERNAME_MIN_LENGTH = 5
        USERNAME_MAX_LENGTH = 32
        value: str = self.cleaned_data['username']

        if not value:
            return value

        if not is_valid_alpha_numeric(value):
            raise ValidationError('ユーザ名は半角英数または「-_」のみ使えます。')

        if not is_valid_min_length(value, USERNAME_MIN_LENGTH):
            raise ValidationError(f'ユーザ名は{USERNAME_MIN_LENGTH}文字以上で入力してください。')

        if not is_valid_max_length(value, USERNAME_MAX_LENGTH):
            raise ValidationError(f'ユーザ名は{USERNAME_MAX_LENGTH}文字以下で入力してください。')

        try:
            User.objects.get(username=value)

        except User.DoesNotExist:
            raise ValidationError(f'ユーザ名はすでに使用されています。')

        return value

    def clean_password(self) -> str:

        PASSWORD_MIN_LENGTH = 10
        PASSWORD_MAX_LENGTH = 64
        value: str = self.cleaned_data['password']

        if not value:
            return value

        if not is_valid_alpha_numeric(value):
            raise ValidationError('パスワードは半角英数または「-_」のみ使えます。')

        if not is_valid_min_length(value, PASSWORD_MIN_LENGTH):
            raise ValidationError(f'パスワードは{PASSWORD_MIN_LENGTH}文字以上で入力してください。')

        if not is_valid_max_length(value, PASSWORD_MAX_LENGTH):
            raise ValidationError(f'パスワードは{PASSWORD_MAX_LENGTH}文字以下で入力してください。')

