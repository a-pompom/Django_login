from django import forms

class LoginForm(forms.Form):

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