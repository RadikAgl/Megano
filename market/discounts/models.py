"""Модели приложения discounts"""

from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from discounts.mixins import DiscountBase
from products.models import Product, Category, Tag


class DiscountProduct(DiscountBase):
    """Модель для хранения скидок на товары"""

    products = models.ManyToManyField(Product, related_name="discount_products")

    class Meta:
        verbose_name = _("скидка на товар")
        verbose_name_plural = _("скидки на товары")


class DiscountCategory(DiscountBase):
    """Модель для хранения скидок на категории товаров"""

    categories = models.ManyToManyField(Category, related_name="discount_categories")

    class Meta:
        verbose_name = _("скидка на категорию товаров")
        verbose_name_plural = _("скидки на категории товаров")


class DiscountTag(DiscountBase):
    """Модель для хранения скидок на теги товаров"""

    tags = models.ManyToManyField(Tag, related_name="discount_tags")

    class Meta:
        verbose_name = _("скидка на теги товаров")
        verbose_name_plural = _("скидки на теги товаров")


class DiscountBonus(DiscountBase):
    """Модель для хранения скидок на стоимость корзины"""

    cart_threshold_cost = models.DecimalField(
        default=Decimal("Infinity"), max_digits=10, decimal_places=2, verbose_name=_("пороговая цена")
    )

    class Meta:
        verbose_name = _("скидка на стоимость корзины")
        verbose_name_plural = _("скидки на стоимость корзины")


class DiscountUser(DiscountBase):
    """Модель для хранения скидок для пользователя"""

    user = models.ManyToManyField(User, related_name="discount_users")

    class Meta:
        verbose_name = _("скидка для пользователя")
        verbose_name_plural = _("скидки для пользователей")
