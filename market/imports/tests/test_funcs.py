import unittest
from unittest.mock import patch, MagicMock

from accounts.models import User
from imports.common_utils import notify_admin_about_import_success
from settings_app.models import SiteSettings


class TestNotifyAdminAboutImportSuccess(unittest.TestCase):
    @patch("imports.common_utils.send_mail")
    @patch("settings_app.models.SiteSettings.objects.get")
    @patch("accounts.models.User.objects.get")
    def test_notify_admin_about_import_success(self, mock_user_get, mock_site_settings_get_instance, mock_send_mail):
        # Mocking the User object
        user_id = 1
        user_email = "user@example.com"
        user_username = "testuser"
        user = MagicMock(spec=User)
        user.email = user_email
        user.username = user_username
        mock_user_get.return_value = user

        # Mocking the SiteSettings object
        site_settings = MagicMock(spec=SiteSettings)
        site_settings.email_access_settings = {
            "EMAIL_HOST": "smtp.yandex.ru",
            "DEFAULT_ADMIN_EMAIL": "joseph.fareez@yandex.ru",
        }
        mock_site_settings_get_instance.return_value = site_settings

        # Call the function
        file_name = "test.csv"
        total_products = 10
        successful_imports = 8
        failed_imports = 2
        notify_admin_about_import_success(user_id, file_name, total_products, successful_imports, failed_imports)

        # Assertions
        mock_user_get.assert_called_once_with(id=user_id)
        mock_site_settings_get_instance.assert_called_once()
        mock_send_mail.assert_called_once_with(
            "Импорт успешно завершен",
            f"Импорт файла {file_name} успешно завершен.\n"
            f"Загружено пользователем: {user_username} ({user_email}).\n"
            f"Всего товаров: {total_products}\n"
            f"Успешных импортов: {successful_imports}\n"
            f"Неудачных импортов: {failed_imports}",
            user_email,
            ["joseph.fareez@yandex.ru"],
            fail_silently=False,
        )
