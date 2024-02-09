from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """модель пользователя"""
    email = models.EmailField(unique=True, blank=True)

    class Meta:
        """имя таблицы"""
        app_label = "accounts"
