"""Django-модель, представляющая продукт."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Banner(models.Model):
    """Баннер"""

    name = models.CharField(max_length=512, verbose_name=_("название"))
    actual = models.BooleanField(default=True, verbose_name=_("актуальность"))
    preview = models.ImageField(verbose_name=_("превью"), upload_to="banners")
    link = models.URLField(verbose_name=_("ссылка"), unique=True, db_index=True)

    class Meta:
        verbose_name = _("Баннер")
        verbose_name_plural = _("Баннеры")

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    """Модель django orm категорий товара"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"), unique=True)
    description = models.TextField(verbose_name=_("описание"), blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    sort_index = models.PositiveIntegerField(verbose_name=_("индекс сортировки"), null=True, unique=True)

    def is_active(self):
        """Проверяет, активна ли категория, имея ли хотя бы один продукт."""
        return self.product_set.exists()

    class Meta:
        verbose_name_plural = _("категория")

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    """Модель django orm тегов"""

    name = models.CharField(max_length=100, verbose_name=_("тег"), unique=True)

    class Meta:
        verbose_name_plural = _("тег")

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    """Модель django orm товаров"""

    name = models.CharField(max_length=100, db_index=True, verbose_name=_("наименование"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=100, verbose_name=_("категория"))
    description = models.CharField(max_length=1000, verbose_name=_("описание"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("дата создания"))
    details = models.JSONField(default=dict, blank=True, verbose_name=_("детали"))
    tags = models.ManyToManyField(Tag, related_name="product")

    class Meta:
        verbose_name_plural = _("продукт")

    def __str__(self):
        return f"{self.name}"


class ProductImage(models.Model):
    """Модель фотографии товара"""

    image = models.ImageField(upload_to="products/%Y/%m/%d/", verbose_name=_("изображение"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name=_("продукт"))

    class Meta:
        verbose_name = _("изображение")
        verbose_name_plural = _("изображения")

    def __str__(self):
        return f"{self.product.name}"
