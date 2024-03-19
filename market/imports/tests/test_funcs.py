from unittest.mock import patch, MagicMock

from django.test import TestCase

from accounts.models import User
from imports.common_utils import notify_admin_about_import_success


class TestNotifyAdminAboutImportSuccess(TestCase):
    @patch("imports.common_utils.send_mail")
    @patch("settings_app.models.SiteSettings.load")
    @patch("accounts.models.User.objects.get")
    def test_notify_admin_about_import_success(self, mock_user_get, mock_site_settings_load, mock_send_mail):
        # Mock User object
        user_id = 1
        user_email = "user@example.com"
        user_username = "testuser"
        user = MagicMock(spec=User)
        user.email = user_email
        user.username = user_username
        mock_user_get.return_value = user

        # Mock SiteSettings object
        site_settings = MagicMock()
        site_settings.email_access_settings = {"EMAIL_HOST_USER": "admin@example.com"}  # Mock email settings
        mock_site_settings_load.return_value = site_settings

        # Call the function
        file_name = "test.csv"
        total_products = 10
        successful_imports = 8
        failed_imports = 2
        notify_admin_about_import_success(user_id, file_name, total_products, successful_imports, failed_imports)

        # Assertions
        mock_user_get.assert_called_once_with(id=user_id)
        mock_site_settings_load.assert_called_once()
        mock_send_mail.assert_called_once_with(
            "Импорт успешно завершен",
            f"Импорт файла {file_name} успешно завершен.\n"
            f"Загружено пользователем: {user_username} ({user_email}).\n"
            f"Всего товаров: {total_products}\n"
            f"Успешных импортов: {successful_imports}\n"
            f"Неудачных импортов: {failed_imports}",
            user_email,  # Sender
            ["admin@example.com"],  # Recipient
            fail_silently=False,
        )
