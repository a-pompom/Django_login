from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    """
    認証用ユーザ
    """

    class Meta:
        db_table = 'm_user'

    USERNAME_FIELD = 'username'

    username: str = models.CharField(
        name='username',
        max_length=255,
        unique=True
    )

    password: str = models.CharField(
        name='password',
        max_length=255,
    )

    is_admin: bool = models.BooleanField(
        name='is_admin'
    )

    def __str__(self):
        return f'username: {self.username}, password: {self.password}, is_admin: {self.is_admin}'