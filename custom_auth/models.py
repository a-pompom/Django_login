from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    認証用ユーザ
    """

    class Meta:
        db_table = 'm_user'

    username = models.CharField(
        name='username',
        max_length=255,
        unique=True
    )

    password = models.CharField(
        name='password',
        max_length=255,
    )

    is_admin = models.BooleanField(
        name='is_admin'
    )