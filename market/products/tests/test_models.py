import json
from pathlib import Path

from django.test import TestCase

from products.models import Product, Category


class ProductModelTest(TestCase):
    """Класс тестов модели товара"""

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(
            name="Тестовый продукт",
            details={"Диагональ, дм": 101},
        )

    def test_verbose_name(self):
        product = ProductModelTest.product
        field_verboses = {
            "name": "наименование",
            "details": "характеристики",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(product._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        product = ProductModelTest.product
        max_length = product._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures"


class CategoryModelTest(TestCase):
    """Класс тестов модели Категорий"""

    fixtures = ["fixtures/categories.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load fixtures
        with open(FIXTURES_DIR / "categories.json", "r", encoding="utf-8") as file:
            cls.fixtures = json.load(file)

    def test_fixture_loading(self):
        category_count = Category.objects.count()
        print(f"Actual category count: {category_count}")
        self.assertEqual(category_count, len(self.fixtures))

    def test_verbose_name(self):
        category = Category()
        field_verboses = {
            "name": "наименование",
            "sort_index": "индекс сортировки",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(category._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        category = Category()
        max_length = category._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)
