from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from imports.models import ImportLog, ImportLogProduct
from products.models import Product, Category


class ImportLogModelTest(TestCase):
    """
    Класс тестирования модели ImportLog.

    Methods:
        setUp(): Подготовка данных перед выполнением тестов.
        test_import_log_str(): Тестирование метода __str__ модели ImportLog.
        test_verbose_name(): Тестирование verbose_name и verbose_name_plural модели ImportLog.
    """

    def setUp(self):
        """
        Подготовка данных перед выполнением тестов.
        """
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.import_log = ImportLog.objects.create(
            user=self.user, file_name="test_file.txt", status="Выполнен", timestamp=timezone.now()
        )

    def test_import_log_str(self):
        """
        Тестирование метода __str__ модели ImportLog.

        Ожидается, что строковое представление объекта ImportLog корректно формируется.
        """
        self.assertEqual(
            str(self.import_log), f"Импорт: {self.import_log.file_name}," f" Статус: {self.import_log.status}"
        )

    def test_verbose_name(self):
        """
        Тестирование verbose_name и verbose_name_plural модели ImportLog.

        Ожидается, что verbose_name и verbose_name_plural установлены корректно.
        """
        self.assertEqual(ImportLog._meta.verbose_name, "лог импорта")
        self.assertEqual(ImportLog._meta.verbose_name_plural, "логи импорта")


class ImportLogProductModelTest(TestCase):
    """
    Класс тестирования модели ImportLogProduct.

    Methods:
        setUp(): Подготовка данных перед выполнением тестов.
        test_import_log_product_relationships(): Тестирование отношений модели ImportLogProduct.
        test_verbose_name(): Тестирование verbose_name и verbose_name_plural модели ImportLogProduct.
    """

    def setUp(self):
        """
        Подготовка данных перед выполнением тестов.
        """
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.import_log = ImportLog.objects.create(
            user=self.user, file_name="test_file.txt", status="Выполнен", timestamp=timezone.now()
        )
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(name="Test Product", category=self.category)

        self.import_log_product = ImportLogProduct.objects.create(import_log=self.import_log, product=self.product)

    def test_import_log_product_relationships(self):
        """
        Тестирование отношений модели ImportLogProduct.

        Ожидается, что отношения между ImportLogProduct, ImportLog и Product установлены корректно.
        """
        self.assertEqual(self.import_log_product.import_log, self.import_log)
        self.assertEqual(self.import_log_product.product, self.product)

    def test_verbose_name(self):
        """
        Тестирование verbose_name и verbose_name_plural модели ImportLogProduct.

        Ожидается, что verbose_name и verbose_name_plural установлены корректно.
        """
        self.assertEqual(ImportLogProduct._meta.verbose_name, "продукт в логе импорта")
        self.assertEqual(ImportLogProduct._meta.verbose_name_plural, "продукты в логах импорта")
