from django.test import TestCase

from products.models import Product, Category


class ProductModelTest(TestCase):
    """Класс тестов модели товара"""

    fixtures = ["05-categories.json", "07-products.json"]

    def setUp(self):
        self.product = Product.objects.get(pk=1)
        self.category = Category.objects.get(pk=1)

    def test_fixture_loading(self):
        products_count = Product.objects.count()
        self.assertEqual(products_count, 54)

    def test_name_max_length(self):
        max_length = self.product._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)


class CategoryModelTest(TestCase):
    """Класс тестов модели Категорий"""

    fixtures = ["05-categories.json"]

    def setUp(self):
        self.category = Category.objects.get(pk=1)

    def test_fixture_loading(self):
        category_count = Category.objects.count()
        self.assertEqual(category_count, 20)

    def test_name_max_length(self):
        max_length = self.category._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)
