""" Базовые модели приложения discounts """

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class DiscountBase(models.Model):
    """Базовая модель скидок"""

    title = models.CharField(max_length=100, verbose_name=_("название акции"))
    percentage = models.PositiveIntegerField(default=0, verbose_name=_("процент скидки"))
    start_date = models.DateField(verbose_name=_("начало акции"))
    end_date = models.DateField(verbose_name=_("окончание акции"))

    class Meta:
        abstract = True

    def is_active(self):
        now = timezone.now().date()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"percentage={self.percentage}, event={self.title}"
