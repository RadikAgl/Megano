from django.db import models

from accounts.models import User


class ImportLog(models.Model):
    """
    Модель для хранения логов импорта.
    """

    STATUS_CHOICES = [
        ("В процессе выполнения", "В процессе выполнения"),
        ("Выполнен", "Выполнен"),
        ("Завершён с ошибкой", "Завершён с ошибкой"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255, verbose_name="Имя файла импорта")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, verbose_name="Статус")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время начала импорта")

    def __str__(self):
        return f"Импорт: {self.file_name}, Статус: {self.status}"
