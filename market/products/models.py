"""Django-модель, представляющая продукт."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """Продукт"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    details = models.JSONField(verbose_name=_("характеристики"))


class Category(models.Model):
    """Модель категорий товара"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"), unique=True)
    description = models.TextField(verbose_name=_("описание"), blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sort_index = models.CharField(verbose_name=_("индекс сортировки"), blank=True)

    class Meta:
        db_table = "category"
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return f"{self.name}"
