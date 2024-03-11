from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User  # noqa
from products.models import Product


class ImportLog(models.Model):
    """
    Модель для записи лога импорта.

    Attributes:
        STATUS_CHOICES (list): Варианты статусов импорта.
        user (User): Пользователь, загрузивший файл для импорта.
        file_name (str): Имя файла импорта.
        status (str): Текущий статус импорта.
        timestamp (datetime): Время начала импорта.
        products (ManyToManyField): Связь с продуктами через модель ImportLogProduct.

    Methods:
        __str__(): Возвращает строковое представление объекта ImportLog.
    """

    STATUS_CHOICES = [
        ("in_progress", _("В процессе выполнения")),
        ("completed", _("Выполнен")),
        ("error", _("Завершён с ошибкой")),
    ]

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="imports", verbose_name="Пользователь"
    )
    file_name = models.CharField(max_length=255, verbose_name="Имя файла импорта")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, verbose_name="Статус")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время начала импорта")
    products = models.ManyToManyField(Product, through="ImportLogProduct", related_name="import_logs")

    class Meta:
        verbose_name = _("лог импорта")
        verbose_name_plural = _("логи импорта")

    def __str__(self):
        """
        Возвращает строковое представление объекта ImportLog.

        Returns:
            str: Строковое представление объекта ImportLog.
        """
        return f"Импорт: {self.file_name}, Статус: {self.status}"


class ImportLogProduct(models.Model):
    """
    Модель для связи продукта с логом импорта.

    Attributes:
        import_log (ImportLog): Ссылка на объект ImportLog.
        product (Product): Ссылка на объект Product.
    """

    import_log = models.ForeignKey(ImportLog, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("продукт в логе импорта")
        verbose_name_plural = _("продукты в логах импорта")