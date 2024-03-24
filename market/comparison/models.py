from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from products.models import Product


class Comparison(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="comparison", verbose_name=_("пользователь")
    )
    products = models.ManyToManyField(Product, verbose_name=_("товары"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("дата создания"))

    class Meta:
        verbose_name_plural = _("сравнение")

    def __str__(self):
        return f"Comparison #{self.pk}"
