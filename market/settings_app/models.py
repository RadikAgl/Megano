import os
from django.db import models
from .singleton_model import SingletonModel


class ProjectSettingsManager(models.Manager):
    def get_instance(self):
        if self.exists():
            return self.first()
        return self.create()


class SiteSettings(SingletonModel):
    """Модель настроек сайта"""

    DOCS_DIR = models.CharField(max_length=255, default="docs", verbose_name="Docs Directory")
    SUCCESSFUL_IMPORTS_DIR = models.CharField(
        max_length=255, default="successful_imports", verbose_name="Successful Imports Directory"
    )
    FAILED_IMPORTS_DIR = models.CharField(
        max_length=255, default="failed_imports", verbose_name="Failed Imports Directory"
    )

    BANNERS_EXPIRATION_TIME = models.PositiveIntegerField(default=600, verbose_name="Banners Expiration Time")
    email_access_settings = models.JSONField(default=dict, verbose_name="Email Access Settings")

    EMAIL_HOST_USER = models.CharField(
        max_length=255, default=os.getenv("EMAIL_HOST_USER"), verbose_name="Email Host User"
    )

    objects = ProjectSettingsManager()

    def save(self, *args, **kwargs):
        email_settings = {
            "EMAIL_PORT": getattr(self, "EMAIL_PORT", None),
            "EMAIL_HOST_USER": getattr(self, "EMAIL_HOST_USER", None),
            "EMAIL_HOST_PASSWORD": getattr(self, "EMAIL_HOST_PASSWORD", None),
            "DEFAULT_FROM_EMAIL": getattr(self, "DEFAULT_FROM_EMAIL", None),
        }

        self.email_access_settings.update(email_settings)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "настройки сайта"
        verbose_name_plural = "настройки сайта"
