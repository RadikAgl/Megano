import os
from typing import Dict, Any

from django.db import models
from django.urls import reverse

from .singleton_model import (
    SingletonModel,
    BANNERS_EXPIRATION_TIME,
    FAILED_IMPORTS_DIR,
    SUCCESSFUL_IMPORTS_DIR,
    DOCS_DIR,
)


def get_default_email_access_settings() -> Dict[str, Any]:
    """
    Получает настройки доступа к почте по умолчанию из переменных окружения.
    """
    return {
        "EMAIL_HOST": os.getenv("EMAIL_HOST", ""),
        "EMAIL_USE_TLS": os.getenv("EMAIL_USE_TLS", ""),
        "EMAIL_USE_SSL": os.getenv("EMAIL_USE_SSL", ""),
        "EMAIL__HOST_PORT": os.getenv("EMAIL_HOST_PORT", ""),
        "EMAIL_HOST_USER": os.getenv("EMAIL_HOST_USER", ""),
        "EMAIL_HOST_PASSWORD": os.getenv("EMAIL_HOST_PASSWORD", ""),
    }


def get_default_email_credentials() -> Dict[str, str]:
    """
    Returns the default email credentials as an empty dictionary.
    """
    return {}


class ProjectSettingsManager(models.Manager):
    """
    Менеджер модели `SiteSettings`.

    Этот менеджер предоставляет дополнительные методы для работы с объектами `SiteSettings`.
    """

    def get_instance(self):
        """
        Получает или создает экземпляр настроек сайта.

        Если в базе данных уже существует экземпляр настроек сайта, возвращает его.
        В противном случае создает новый экземпляр и возвращает его.
        """
        if self.exists():
            return self.first()
        return self.create()


class SiteSettings(SingletonModel):
    """
    Модель настроек сайта.

    Эта модель содержит настройки сайта, такие как директории документов,
    настройки доступа к почте и другие параметры.
    """

    docs_dir = models.CharField(
        max_length=255, default=DOCS_DIR, verbose_name="Директория документов"
    )  # Директория для хранения документов
    successful_imports_dir = models.CharField(
        max_length=255, default=SUCCESSFUL_IMPORTS_DIR, verbose_name="Директория успешных импортов"
    )  # Директория для успешных импортов
    failed_imports_dir = models.CharField(
        max_length=255, default=FAILED_IMPORTS_DIR, verbose_name="Директория неудачных импортов"
    )  # Директория для неудачных импортов
    banners_expiration_time = models.PositiveIntegerField(
        default=BANNERS_EXPIRATION_TIME, verbose_name="Время истечения баннеров"
    )  # Время истечения баннеров (в секундах)
    email_access_settings = models.JSONField(
        default=get_default_email_access_settings,
        verbose_name="Настройки доступа к электронной почте",
        help_text="Настройки доступа к электронной почте из .env",
    )
    email_credentials = models.JSONField(
        default=get_default_email_credentials,
        verbose_name="Почтовые учетные данные",
        help_text="Почтовые учетные данные из .env",
    )  # Почтовые учетные данные
    objects = ProjectSettingsManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.DEFAULT_FROM_EMAIL = get_default_email_credentials()

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Переопределенный метод сохранения для модели SiteSettings.

        При сохранении настроек сайта обновляются учетные данные электронной почты из файла .env,
         если они не предоставлены.
        """

        # Обновление учетных данных электронной почты, если они предоставлены в переменных окружения
        username = os.getenv("EMAIL_HOST_USER", "")
        password = os.getenv("EMAIL_HOST_PASSWORD", "")
        if username and password:
            email_credentials = {
                "username": username,
                "password": password,
            }
            self.email_credentials = email_credentials
        else:
            # Проверка, установлены ли учетные данные электронной почты или являются ли они пустым словарем
            if not self.email_credentials or self.email_credentials == {}:
                # Установка пустого словаря, если учетные данные
                # электронной почты не предоставлены в переменных окружения
                self.email_credentials = {}

        super().save(*args, **kwargs)  # Вызов метода сохранения родителя для сохранения изменений

    def get_absolute_url(self) -> str:
        """
        Возвращает URL для просмотра или редактирования настроек сайта.

        Если объект уже существует в базе данных, возвращает URL для редактирования.
        В противном случае, возвращает URL для добавления новых настроек.
        """
        if self.pk:
            return reverse("settings_app:sitesettings_change", kwargs={"pk": self.pk})
        else:
            return reverse("settings_app:sitesettings_add")

    class Meta:
        verbose_name = "настройки сайта"
        verbose_name_plural = "настройки сайта"
