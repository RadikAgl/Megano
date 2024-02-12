from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """модель пользователя"""
    username = models.CharField(
        unique=False,
        blank=True,

    )
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    class Meta:
        """имя таблицы"""
        app_label = "accounts"
