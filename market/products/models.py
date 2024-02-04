"""Django-модель, представляющая продукт."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Banner(models.Model):
    """Баннер"""

    name = models.CharField(max_length=512, verbose_name=_("название"))
    actual = models.BooleanField(default=True, verbose_name=_("актуальность"))
    preview = models.ImageField(verbose_name=_("превью"), upload_to="img/preview", null=True, blank=True)
    link = models.URLField(verbose_name=_("ссылка"), blank=True, unique=True, db_index=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    """Продукт"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    details = models.JSONField(verbose_name=_("характеристики"))


class Category(models.Model):
    """Модель django orm категорий товара"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"), unique=True)
    description = models.TextField(verbose_name=_("описание"), blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    sort_index = models.PositiveIntegerField(verbose_name=_("индекс сортировки"), null=True, unique=True)

    def is_active(self):
        return self.product_set.exists()

    class Meta:
        verbose_name_plural = _("Категорий")

    def __str__(self):
        return f"{self.name}"
