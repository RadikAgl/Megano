import os
from typing import List

from django.core.serializers import deserialize
from django.test import TestCase

from products.models import Product, Category, Tag, Banner
from settings_app.models import SiteSettings


class ProductModelTest(TestCase):
    """Класс для тестирования модели продукта"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.fixture_dir: str = SiteSettings.load().fixture_dir
        cls.fixtures: List[str] = [
            os.path.join(cls.fixture_dir, "05-categories.json"),
            os.path.join(cls.fixture_dir, "06-tags.json"),
            os.path.join(cls.fixture_dir, "07-products.json"),
        ]
        cls.load_fixtures()

    @classmethod
    def load_fixtures(cls) -> None:
        for fixture_file in cls.fixtures:
            with open(fixture_file, "rb") as f:
                for obj in deserialize("json", f):
                    obj.save()

    def setUp(self) -> None:
        super().setUp()
        self.product: Product = Product.objects.get(pk=1)
        self.category: Category = Category.objects.get(pk=1)
        self.tag: Tag = Tag.objects.get(pk=1)

    def test_fixture_loading(self) -> None:
        products_count: int = Product.objects.count()
        self.assertEqual(products_count, 53)

    def test_name_max_length(self) -> None:
        max_length: int = self.product._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)


class CategoryModelTest(TestCase):
    """Класс для тестирования модели категории"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.fixture_dir: str = SiteSettings.load().fixture_dir
        cls.fixtures: List[str] = [os.path.join(cls.fixture_dir, "05-categories.json")]
        cls.load_fixtures()

    @classmethod
    def load_fixtures(cls) -> None:
        for fixture_file in cls.fixtures:
            with open(fixture_file, "rb") as f:
                for obj in deserialize("json", f):
                    obj.save()

    def setUp(self) -> None:
        super().setUp()
        self.category: Category = Category.objects.get(pk=1)

    def test_fixture_loading(self) -> None:
        category_count: int = Category.objects.count()
        self.assertEqual(category_count, 20)

    def test_name_max_length(self) -> None:
        max_length: int = self.category._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


class TagModelTest(TestCase):
    """Класс для тестирования модели тега"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.fixture_dir: str = SiteSettings.load().fixture_dir
        cls.fixtures: List[str] = [os.path.join(cls.fixture_dir, "06-tags.json")]
        cls.load_fixtures()

    @classmethod
    def load_fixtures(cls) -> None:
        for fixture_file in cls.fixtures:
            with open(fixture_file, "rb") as f:
                for obj in deserialize("json", f):
                    obj.save()

    def setUp(self) -> None:
        super().setUp()
        self.tag: Tag = Tag.objects.get(pk=1)

    def test_fixture_loading(self) -> None:
        tag_count: int = Tag.objects.count()
        self.assertEqual(tag_count, 35)

    def test_name_max_length(self) -> None:
        max_length: int = self.tag._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)


class BannerModelTest(TestCase):
    """Класс для тестирования модели баннера"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.fixture_dir: str = SiteSettings.load().fixture_dir
        cls.fixtures: List[str] = [os.path.join(cls.fixture_dir, "15-banners.json")]
        cls.load_fixtures()

    @classmethod
    def load_fixtures(cls) -> None:
        for fixture_file in cls.fixtures:
            with open(fixture_file, "rb") as f:
                for obj in deserialize("json", f):
                    obj.save()

    def setUp(self) -> None:
        super().setUp()
        self.banner: Banner = Banner.objects.get(pk=1)

    def test_fixture_loading(self) -> None:
        banners_count: int = Banner.objects.count()
        self.assertEqual(banners_count, 4)

    def test_verbose_name(self) -> None:
        banner: Banner = Banner.objects.get(pk=1)
        field_verboses: dict = {"name": "название", "actual": "актуальность", "preview": "превью", "link": "ссылка"}
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(banner._meta.get_field(field).verbose_name, expected_value)
