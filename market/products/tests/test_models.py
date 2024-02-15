from django.test import TestCase

from products.models import Product, Category, Tag, Banner


class ProductModelTest(TestCase):
    """Класс тестов модели товара"""

    fixtures = ["05-categories.json", "06-tags.json", "07-products.json"]

    def setUp(self):
        self.product = Product.objects.get(pk=1)
        self.category = Category.objects.get(pk=1)
        self.tag = Tag.objects.get(pk=1)

    def test_fixture_loading(self):
        products_count = Product.objects.count()
        self.assertEqual(products_count, 53)

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


class TagModelTest(TestCase):
    """Класс тестов модели теги"""

    fixtures = ["06-tags.json"]

    def setUp(self):
        self.tag = Tag.objects.get(pk=1)

    def test_fixture_loading(self):
        tag_count = Tag.objects.count()
        self.assertEqual(tag_count, 35)

    def test_name_max_length(self):
        max_length = self.tag._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)


class BaseModelTest(TestCase):
    """Класс тестов для модели баннер"""

    fixtures = ["15-banners.json"]

    def setUp(self):
        self.banner = Banner.objects.get(pk=1)

    def test_fixture_loading(self):
        banners_count = Banner.objects.count()
        self.assertEqual(banners_count, 4)

    def test_verbose_name(self):
        banner = Banner.objects.get(pk=1)
        field_verboses = {"name": "название", "actual": "актуальность", "preview": "превью", "link": "ссылка"}
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(banner._meta.get_field(field).verbose_name, expected_value)
