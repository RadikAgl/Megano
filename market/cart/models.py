"""Модели приложения cart"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from shops.models import Offer


class Cart(models.Model):
    """Модель корзины"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts", verbose_name="Пользователь")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("корзина")
        verbose_name_plural = _("корзины")

    def __str__(self):
        return f"Cart {self.user}"


class ProductInCart(models.Model):
    """Модель товара в корзине"""

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="offers")
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("товар в корзине")
        verbose_name_plural = _("товары в корзине")
        ordering = ("-created_at",)

    def __str__(self):
        return f"Product {self.offer.product} in cart {self.cart}"
