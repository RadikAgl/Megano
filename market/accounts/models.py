"""Django-модели, представляющие пользователей интернет-магазина."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from products.models import Product
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """модель пользователя"""

    username = models.CharField(
        unique=False,
        blank=True,
    )
    USERNAME_FIELD = "email"
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    class Meta:
        """имя таблицы"""

        app_label = "accounts"


class ViewHistory(models.Model):
    """Django-модель, представляющая историю просмотра товара пользователем."""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("покупатель"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("товар"))
    view_date = models.DateTimeField(auto_now_add=True, verbose_name=_("дата просмотра"))
    view_count = models.IntegerField(default=0, verbose_name=_("количество просмотров"))

    class Meta:
        verbose_name = "история просмотров"
        verbose_name_plural = "истории просмотров"

    def __str__(self):
        return f"{self.user} - {self.product} - {self.view_date}"
