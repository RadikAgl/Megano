"""Django-модель, представляющая продукт."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Модель django orm категорий товара"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"), unique=True)
    description = models.TextField(verbose_name=_("описание"), blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    sort_index = models.PositiveIntegerField(verbose_name=_("индекс сортировки"), null=True, unique=True)

    def is_active(self):
        return self.product_set.exists()

    class Meta:
        verbose_name_plural = _("категория")

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    """Модель django orm товаров"""

    name = models.CharField(max_length=100, db_index=True, verbose_name=_("наименование"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=100, verbose_name=_("категория"))
    description = models.CharField(max_length=1000, verbose_name=_("описание"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("дата создания"))
    details = models.JSONField(default=dict, blank=True, verbose_name=_("детали"))

    class Meta:
        verbose_name_plural = _("продукт")

    def __str__(self):
        return f"{self.name}"
