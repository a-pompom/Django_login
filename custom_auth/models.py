from __future__ import annotations

from django.db import models
from django.db.models import CharField, BooleanField
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    """ 認証用ユーザ
    """

    class Meta:
        db_table = 'm_user'

    USERNAME_FIELD = 'username'

    # ユーザ名 ユニーク
    username: CharField[str, str] = models.CharField(
        name='username',
        max_length=255,
        unique=True,
    )

    # パスワード
    password: CharField[str, str] = models.CharField(
        name='password',
        max_length=255,
    )

    # 管理者か
    is_admin: BooleanField[bool, bool] = models.BooleanField(
        name='is_admin',
    )

    def __str__(self):
        return f'username: {self.username}, password: {self.password}, is_admin: {self.is_admin}'