import json
import os

from django.test import TestCase

from config import settings
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


class CategoryModelTest(TestCase):
    """Класс тестов модели Категорий"""

    fixtures = [os.path.join(settings.FIXTURE_DIRS, "05-categories.json")]

    def test_fixture_loading(self):
        with open(self.fixtures[0], "r", encoding="utf-8") as file:
            loaded_fixtures = json.load(file)

        category_count = Category.objects.count()
        print(f"Actual category count: {category_count}")
        self.assertEqual(category_count, len(loaded_fixtures))

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
