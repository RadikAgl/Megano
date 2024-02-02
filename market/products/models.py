from django.db import models
from django.utils.translation import gettext_lazy as _


class Banner(models.Model):
    """Баннер"""

    name = models.CharField(max_length=512, verbose_name=_("название"))
    actual = models.BooleanField(default=True, verbose_name=_("актуальность"))
    preview = models.ImageField(verbose_name=_("превью"), upload_to="img/preview", null=True, blank=True)


class Product(models.Model):
    """Продукт"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    details = models.JSONField(verbose_name=_("характеристики"))
