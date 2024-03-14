import os
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from settings_app.models import SiteSettings


class SiteSettingsTestCase(TestCase):
    """Модульные тесты для модели SiteSettings."""

    def setUp(self) -> None:
        # Сохранение исходных переменных среды
        self.original_email_host_user: str = os.environ.get("EMAIL_HOST_USER")
        self.original_email_host_password: str = os.environ.get("EMAIL_HOST_PASSWORD")
        # Установка переменных среды
        os.environ["EMAIL_HOST_USER"] = "joseph.fareez@yandex.ru"
        os.environ["EMAIL_HOST_PASSWORD"] = "ajhfieupshejurpz"

    def tearDown(self) -> None:
        # Восстановление исходных переменных среды
        os.environ["EMAIL_HOST_USER"] = (
            self.original_email_host_user if self.original_email_host_user is not None else ""
        )
        os.environ["EMAIL_HOST_PASSWORD"] = (
            self.original_email_host_password if (self.original_email_host_password is not None) else ""
        )

    def test_site_settings_creation(self) -> None:
        """Тест создания объекта SiteSettings."""
        site_settings: SiteSettings = SiteSettings.objects.create()
        self.assertIsNotNone(site_settings)
        self.assertIsInstance(site_settings, SiteSettings)

    def test_site_settings_absolute_url(self) -> None:
        """Тест метода get_absolute_url модели SiteSettings."""
        # Создание объекта SiteSettings без указания pk
        site_settings: SiteSettings = SiteSettings.objects.create()

        # Тестирование при уже существующем объекте
        expected_url: str = reverse("settings_app:sitesettings_change", kwargs={"pk": site_settings.pk})
        self.assertEqual(site_settings.get_absolute_url(), expected_url)

        # Тестирование при отсутствии объекта
        site_settings.pk = None  # Reset primary key to simulate an unsaved instance
        expected_url = reverse("settings_app:sitesettings_add")
        self.assertEqual(site_settings.get_absolute_url(), expected_url)

    def test_site_settings_save_method(self) -> None:
        """Тест метода save модели SiteSettings."""
        # Создание нового объекта SiteSettings
        site_settings: SiteSettings = SiteSettings.objects.create()
        # Вызов метода save
        site_settings.save()
        # Проверка, правильно ли заполнены email_credentials
        self.assertIsNotNone(site_settings.email_credentials)
        self.assertIn("username", site_settings.email_credentials)
        self.assertIn("password", site_settings.email_credentials)

    def test_site_settings_max_length(self) -> None:
        """Тест max_length для полей CharField в модели SiteSettings."""
        fields: list[str] = ["docs_dir", "successful_imports_dir", "failed_imports_dir"]
        for field_name in fields:
            with self.subTest(field_name=field_name):
                max_length: int = SiteSettings._meta.get_field(field_name).max_length
                self.assertEqual(max_length, 255)

    def test_site_settings_banners_expiration_time_positive_integer(self) -> None:
        """Тест, что banners_expiration_time является положительным целым числом."""
        site_settings: SiteSettings = SiteSettings.objects.create(banners_expiration_time=600)
        self.assertIsInstance(site_settings.banners_expiration_time, int)
        self.assertGreaterEqual(site_settings.banners_expiration_time, 0)

    @patch.dict(os.environ, {"EMAIL_HOST_USER": "test@example.com", "EMAIL_HOST_PASSWORD": "testpassword"})
    def test_site_settings_save_method_with_env_variables(self) -> None:
        """Тест метода save с переменными среды для учетных данных электронной почты."""
        site_settings: SiteSettings = SiteSettings.objects.create()
        site_settings.save()
        self.assertEqual(site_settings.email_credentials, {"username": "test@example.com", "password": "testpassword"})

    def test_site_settings_email_access_settings_and_credentials_empty_by_default(self) -> None:
        # Проверка, что email_access_settings и email_credentials пусты по умолчанию
        site_settings: SiteSettings = SiteSettings.objects.get_instance()

        # Получение настроек доступа к электронной почте по умолчанию
        default_email_access_settings: dict = {
            "EMAIL_HOST": os.getenv("EMAIL_HOST", ""),
            "EMAIL_PORT": os.getenv("EMAIL_PORT", ""),
            "EMAIL_USE_TLS": os.getenv("EMAIL_USE_TLS", ""),
            "EMAIL_USE_SSL": os.getenv("EMAIL_USE_SSL", ""),
        }

        # Сравнение с настройками доступа к электронной почте по умолчанию
        self.assertEqual(site_settings.email_access_settings, default_email_access_settings)

        # Проверка, что email_credentials пуст
        self.assertEqual(
            site_settings.email_credentials,
            {"username": os.getenv("EMAIL_HOST_USER", ""), "password": os.getenv("EMAIL_HOST_PASSWORD", "")},
        )

        # Проверка установки переменных среды
        self.assertEqual(os.environ.get("EMAIL_HOST_USER"), "joseph.fareez@yandex.ru")
        self.assertEqual(os.environ.get("EMAIL_HOST_PASSWORD"), "ajhfieupshejurpz")

    def test_site_settings_email_access_settings_and_credentials_with_env_variables(self) -> None:
        """Тест, что email_access_settings и email_credentials заполнены переменными среды."""
        # Установка переменных среды
        os.environ["EMAIL_HOST"] = "test.host"
        os.environ["EMAIL_PORT"] = "587"
        os.environ["EMAIL_USE_TLS"] = "1"
        os.environ["EMAIL_USE_SSL"] = "0"
        os.environ["EMAIL_HOST_USER"] = "test@example.com"
        os.environ["EMAIL_HOST_PASSWORD"] = "testpassword"

        site_settings: SiteSettings = SiteSettings.objects.get_instance()

        # Проверка, что email_access_settings и email_credentials заполнены корректно
        expected_email_access_settings: dict = {
            "EMAIL_HOST": "test.host",
            "EMAIL_PORT": "587",
            "EMAIL_USE_TLS": "1",
            "EMAIL_USE_SSL": "0",
        }
        expected_email_credentials: dict = {
            "username": "test@example.com",
            "password": "testpassword",
        }
        self.assertEqual(site_settings.email_access_settings, expected_email_access_settings)
        self.assertEqual(site_settings.email_credentials, expected_email_credentials)

        # Очистка: сброс переменных среды
        os.environ.pop("EMAIL_HOST")
        os.environ.pop("EMAIL_PORT")
        os.environ.pop("EMAIL_USE_TLS")
        os.environ.pop("EMAIL_USE_SSL")
        os.environ.pop("EMAIL_HOST_USER")
        os.environ.pop("EMAIL_HOST_PASSWORD")

        # Проверка сброса переменных среды
        self.assertIsNone(os.environ.get("EMAIL_HOST"))
        self.assertIsNone(os.environ.get("EMAIL_PORT"))
        self.assertIsNone(os.environ.get("EMAIL_USE_TLS"))
        self.assertIsNone(os.environ.get("EMAIL_USE_SSL"))
        self.assertIsNone(os.environ.get("EMAIL_HOST_USER"))
        self.assertIsNone(os.environ.get("EMAIL_HOST_PASSWORD"))
