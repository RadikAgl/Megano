from django.test import TestCase
from accounts.models import User
from importer.models import ImportLog


class ImportLogModelTest(TestCase):
    def setUp(self):
        """
        Метод настройки для создания пользователя для тестирования.
        """
        self.user = User.objects.create(username="testuser", email="testuser@example.com")

    def test_import_log_creation(self):
        """
        Тест создания объекта ImportLog.
        """
        import_log = ImportLog.objects.create(user=self.user, file_name="example.csv", status="Выполнен")
        saved_import_log = ImportLog.objects.get(id=import_log.id)
        self.assertEqual(saved_import_log.user, self.user)
        self.assertEqual(saved_import_log.file_name, "example.csv")
        self.assertEqual(saved_import_log.status, "Выполнен")
        self.assertIsNotNone(saved_import_log.timestamp)

    def test_import_log_str_method(self):
        """
        Тест метода __str__ объекта ImportLog.
        """
        import_log = ImportLog.objects.create(user=self.user, file_name="example.csv", status="В процессе выполнения")
        expected_str = f"Импорт: {import_log.file_name}, Статус: {import_log.status}"
        self.assertEqual(str(import_log), expected_str)
