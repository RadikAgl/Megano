from typing import Any

from django.db import models


class SingletonModel(models.Model):
    """Базовая модель для реализации синглтона."""

    class Meta:
        abstract: bool = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Переопределенный метод сохранения.

        Удаляет все объекты класса, кроме текущего, перед сохранением.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls) -> "SingletonModel":
        """
        Загружает экземпляр класса.

        Если экземпляр не найден, создает новый.
        """
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()
