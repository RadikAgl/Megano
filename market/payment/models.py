from django.db import models


class Order(models.Model):
    """модель заказа"""

    name = models.CharField(null=False, blank=False, max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    pay_setting = models.CharField(null=False, blank=True)
    city = models.CharField(null=False, blank=False)
    address = models.CharField(null=False, blank=False)