from typing import Any, Optional, Union
from custom_auth.exceptions import LoginFailureException
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest

from .models import User

class AuthBackend(BaseBackend):
    """ 認証処理用バックエンド
    """

    def get_user(self, user_id: int) -> Union[User, None]:
        """ セッションに格納されているユーザ識別用キーをもとにユーザモデルを取得

        Parameters
        ----------
        user_id: int
            一意識別子
        
        Returns
        -------
        user: User
            認証用ユーザ
        """

        try:
            user = User.objects.get(id=user_id)

        except (User.DoesNotExist, ValueError):
            return None
        
        return user

    def authenticate(self, request: HttpRequest, username: Optional[str]=None, password: Optional[str]=None, **kwargs: Any) -> User:
        """ 認証処理 ユーザ名・パスワードをもとに、該当するユーザがDBに存在するか検証

        Parameters
        ----------
        request: HttpRequest
            認証で利用されるリクエスト情報
        username: str
            ユーザをDBから取得するためのユーザ名
        password: str
            ユーザを認証するためのパスワード
        
        Returns
        -------
        user: User
            認証に成功した場合は、セッションへ格納するためのユーザモデルを返す

        Raises
        ------
        LoginFailureException
            ログインに失敗した場合に送出される
        """

        # ユーザ存在チェック
        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            raise LoginFailureException()

        # パスワード妥当性チェック
        is_valid_password = check_password(password, user.password)

        if not is_valid_password:
            raise LoginFailureException()
        
        return user