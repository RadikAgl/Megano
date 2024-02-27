"""Модели приложения cart"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class Cart(models.Model):
    """Модель корзины"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("корзина")
        verbose_name_plural = _("корзины")

    def __str__(self):
        return f"Cart {self.user}"
