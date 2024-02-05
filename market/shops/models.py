from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Shop(models.Model):
    """Магазин"""

    name = models.CharField(max_length=512, verbose_name=_("название"))
    products = models.ManyToManyField(
        "products.Product",
        through="Offer",
        related_name="shops",
        verbose_name=_("товары в магазине"),
    )


class Seller(models.Model):
    """Модель django orm продавца"""

    name = models.CharField(max_length=512, verbose_name=_("Название продавца"))
    contact_info = models.CharField(max_length=512, verbose_name=_("Контактная информация"))
    description_of_seller = models.TextField(verbose_name=_("Описание"))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))

    class Meta:
        verbose_name_plural = _("Продавцы")

    def __str__(self):
        return f"{self.name}"


class Offer(models.Model):
    """Предложение магазина"""

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("цена"))
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name="Продавец")

    class Meta:
        constraints = [models.UniqueConstraint("shop", "product", name="unique_product_in_shop")]
