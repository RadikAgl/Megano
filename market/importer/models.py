from django.contrib.auth import get_user_model
from django.db import models


class ImportLog(models.Model):
    """
    Модель для хранения логов импорта.
    """

    STATUS_CHOICES = [
        ("В процессе выполнения", "В процессе выполнения"),
        ("Выполнен", "Выполнен"),
        ("Завершён с ошибкой", "Завершён с ошибкой"),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="imports", verbose_name="user")
    file_name = models.CharField(max_length=255, verbose_name="Имя файла импорта")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, verbose_name="Статус")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время начала импорта")

    def __str__(self):
        return f"Импорт: {self.file_name}, Статус: {self.status}"
