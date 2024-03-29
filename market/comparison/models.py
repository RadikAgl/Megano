from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from products.models import Product


class Comparison(models.Model):
    """
    Модель для хранения сравнения между товарами для конкретного пользователя.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="comparison", verbose_name=_("пользователь")
    )
    products = models.ManyToManyField(Product, verbose_name=_("товары"))
    created_at = models.DateTimeField(verbose_name=_("дата создания"), editable=False)

    class Meta:
        verbose_name = _("сравнения")
        verbose_name_plural = _("сравнение")

    def __str__(self):
        """
        Возвращает строковое представление объекта сравнения.
        """
        return f"Comparison #{self.pk}"

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения для установки даты создания при создании нового объекта.
        """
        if not self.pk:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)
