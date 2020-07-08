from custom_auth.exceptions import LoginFailureException
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.http import HttpRequest, HttpResponse

from typing import cast

from .forms import LoginForm, SignUpForm
from .backend import AuthBackend
from .models import User


class LoginView(View):
    """ ログイン画面用View
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """ ログイン画面表示処理

        Parameters
        ----------
        request: HttpRequest
            GETリクエスト情報

        Returns
        -------
        response: HttpResponse
            ログイン画面表示用レスポンス
        """

        context = {
            'form': LoginForm()
        }

        return render(request, 'login/login.html', context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """ ログイン処理

        Parameters
        ----------
        request : HttpRequest
            POSTリクエスト情報

        Returns
        -------
        HttpResponse
            ログイン失敗 -> ログイン画面
            ログイン成功 -> トップ画面

        Raises
        ------
        LoginFailureException
            ユーザ名・パスワードがDBに存在するものと合致しなかった場合に送出 ログイン画面へ再遷移
        """

        form = LoginForm(request.POST)
        
        # ユーザ認証
        try:
            if not form.is_valid():
                raise LoginFailureException()
            
            user = AuthBackend().authenticate(
                request, 
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )
        
        # ログイン失敗
        except LoginFailureException:

            form.add_error(None, 'ユーザ名またはパスワードが間違っています。')
            context = {'form': form}
            return render(request, 'login/login.html', context)

        login(request, user, 'custom_auth.backend.AuthBackend')

        return redirect(settings.LOGIN_SUCCESS_URL)


class SignUpView(View):
    """ ユーザ登録処理用View
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """ ユーザ登録画面表示

        Parameters
        ----------
        request : HttpRequest
            GETリクエスト情報

        Returns
        -------
        HttpResponse
            ユーザ登録画面
        """        

        context = {
            'form': SignUpForm()
        }

        return render(request, 'signup/signup.html', context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """ ユーザ登録処理

        Parameters
        ----------
        request : HttpRequest
            POSTリクエスト情報

        Returns
        -------
        HttpResponse
            ユーザ登録失敗 -> ユーザ登録画面
            ユーザ登録成功 -> ログイン画面
        """        

        form = SignUpForm(request.POST)

        # 登録失敗
        if not form.is_valid():

            context = {
                'form': form
            }
            return render(request, 'signup/signup.html', context)

        # ユーザ登録
        user = User(
            username=form.cleaned_data['username'],
            password=make_password(form.cleaned_data['password']),
            is_admin=False,
        )
        user.save()

        return redirect('login:login')

class TopView(View):
    """ トップ画面用View
    """    

    def get(self, request: HttpRequest) -> HttpResponse:
        """ トップ画面表示

        Parameters
        ----------
        request : HttpRequest
            GETリクエスト

        Returns
        -------
        HttpResponse
            未ログイン -> ログイン画面
            ログイン済み -> トップ画面 権限に応じて出しわけ
        """        

        user = cast(User, request.user)

        # 認証済みか
        if not user.is_authenticated:
            return redirect('login:login')
        
        # 管理者か
        if user.is_admin:
            return render(request, 'top/top_admin.html')

        return render(request, 'top/top.html')

class LogoutView(View):
    """ ログアウト処理用View
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """ ログアウト処理

        Parameters
        ----------
        request : HttpRequest
            GETリクエスト

        Returns
        -------
        HttpResponse
            ログイン画面
        """        

        logout(request)

        return redirect('login:login')


def handler404(request: HttpRequest, exception: Exception) -> HttpResponse:
    """ 404ページを表示

    Parameters
    ----------
    request : HttpRequest
        存在しない画面へのリクエスト
    exception : Exception
        遷移元の例外

    Returns
    -------
    HttpResponse
        404ページ
    """    

    return render(request, 'widget_404.html', status=404)
