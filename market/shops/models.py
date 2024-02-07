from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def shop_logo_directory_path(instance: "Shop", filename: str) -> str:
    """Функция, гененрирующая путь, по которому будет храниться логотип компании-продавца"""
    return "shops/shop_{name}/{filename}".format(
        name=instance.name,
        filename=filename,
    )


class Shop(models.Model):
    """Модель django orm магазина, который является продавцом на маркетплейсе Megano"""

    name = models.CharField(max_length=512, verbose_name=_("Название"))
    contact_info = models.CharField(max_length=512, verbose_name=_("Контактная информация"))
    description_of_seller = models.TextField(verbose_name=_("Описание"))
    products = models.ManyToManyField(
        "products.Product",
        through="Offer",
        related_name="shops",
        verbose_name=_("Товары в магазине"),
    )
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    logo = models.ImageField(
        upload_to=shop_logo_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        verbose_name=_("Логотип компании"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = _("Продавцы")

    def __str__(self):
        return f"{self.name}"


class Offer(models.Model):
    """Предложение магазина"""

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("цена"))

    class Meta:
        constraints = [models.UniqueConstraint("shop", "product", name="unique_product_in_shop")]
