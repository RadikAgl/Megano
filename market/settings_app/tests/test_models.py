from typing import Dict, Any
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from settings_app.models import SiteSettings


class SiteSettingsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Устанавливает начальные условия для тестов SiteSettings.
        """
        cls.site_settings: SiteSettings = SiteSettings.objects.create()

    def test_get_instance_existing(self) -> None:
        """
        Проверяет, возвращает ли get_instance() существующий экземпляр.
        """
        existing_instance: SiteSettings = SiteSettings.objects.get_instance()
        self.assertEqual(existing_instance, self.site_settings)

    def test_get_instance_new(self) -> None:
        """
        Проверяет, создает ли get_instance() новый экземпляр, если ни один не существует.
        """
        SiteSettings.objects.all().delete()  # Удаляет существующие экземпляры
        new_instance: SiteSettings = SiteSettings.objects.get_instance()
        self.assertIsNotNone(new_instance.pk)

    def test_get_absolute_url_with_pk(self) -> None:
        """
        Проверяет get_absolute_url() при наличии первичного ключа экземпляра.
        """
        url: str = self.site_settings.get_absolute_url()
        expected_url: str = reverse("settings_app:sitesettings_change", kwargs={"pk": self.site_settings.pk})
        self.assertEqual(url, expected_url)

    def test_get_absolute_url_without_pk(self) -> None:
        """
        Проверяет get_absolute_url() при отсутствии первичного ключа экземпляра.
        """
        self.site_settings.pk = None
        url: str = self.site_settings.get_absolute_url()
        expected_url: str = reverse("settings_app:sitesettings_add")
        self.assertEqual(url, expected_url)

    @patch("settings_app.models.get_default_email_settings")
    def test_default_email_settings(self, mock_get_default_email_settings) -> None:
        """
        Проверяет, корректно ли извлекаются настройки почты по умолчанию.
        """
        # Мокирует возвращаемое значение get_default_email_settings
        expected_settings: Dict[str, Any] = {
            "EMAIL_HOST": "example.com",
            "EMAIL_USE_TLS": True,
            "EMAIL_USE_SSL": False,
            "EMAIL__HOST_PORT": 587,
            "EMAIL_HOST_USER": "user@example.com",
            "EMAIL_HOST_PASSWORD": "password",
        }
        mock_get_default_email_settings.return_value = expected_settings

        # Получает настройки почты по умолчанию
        settings: SiteSettings = SiteSettings(email_access_settings=expected_settings)
        email_settings: Dict[str, Any] = settings.email_access_settings
        self.assertEqual(email_settings, expected_settings)
