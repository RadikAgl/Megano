from django.core.management import call_command
from django.test import TestCase
from django.utils.translation import gettext as _
from products.models import Product, Category


class ProductModelTest(TestCase):
    """Класс тестов модели товара"""

    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "05-categories.json", "07-products.json")

    def setUp(self):
        self.product = Product.objects.get(pk=1)
        self.category = Category.objects.get(pk=1)

    def test_fixture_loading(self):
        products_count = Product.objects.count()
        self.assertGreater(products_count, 0)

    def test_verbose_name(self):
        field_verboses = {
            "name": _("наименование"),
            "category": _("категория"),
            "description": _("описание"),
            "created_at": _("дата создания"),
            "details": _("детали"),
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(self.product._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        max_length = self.product._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)


class CategoryModelTest(TestCase):
    """Класс тестов модели Категорий"""

    fixtures = ["05-categories.json"]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        call_command("loaddata", "05-categories.json")

    def setUp(self):
        self.category = Category.objects.get(pk=1)

    def test_fixture_loading(self):
        category_count = Category.objects.count()
        self.assertEqual(category_count, 20)

    def test_verbose_name(self):
        field_verboses = {
            "name": "наименование",
            "sort_index": "индекс сортировки",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(self.category._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        max_length = self.category._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


class LoadFixturesTest(TestCase):
    fixtures = ["05-categories.json", "07-products.json"]

    def test_loaded_data(self):
        product_count = Product.objects.count()
        category_count = Category.objects.count()

        self.assertGreater(product_count, 0, _("No products loaded from fixtures"))
        self.assertGreater(category_count, 0, _("No categories loaded from fixtures"))
