from django.test import TestCase

from products.models import Product, Category, Tag, Banner


class ProductModelTest(TestCase):
    """Класс для тестирования модели продукта"""

    fixtures = [
        "05-categories.json",
        "06-tags.json",
        "07-products.json",
    ]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.product: Product = Product.objects.get(pk=1)
        cls.category: Category = Category.objects.get(pk=1)
        cls.tag: Tag = Tag.objects.get(pk=1)

    def test_fixture_loading(cls) -> None:
        products_count: int = Product.objects.count()
        cls.assertEqual(products_count, 53)

    def test_name_max_length(cls) -> None:
        max_length: int = cls.product._meta.get_field("name").max_length
        cls.assertEqual(max_length, 100)


class CategoryModelTest(TestCase):
    """Класс для тестирования модели категории"""

    fixtures = ["05-categories.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.category: Category = Category.objects.get(pk=1)

    def test_fixture_loading(cls) -> None:
        category_count: int = Category.objects.count()
        cls.assertEqual(category_count, 20)

    def test_name_max_length(cls) -> None:
        max_length: int = cls.category._meta.get_field("name").max_length
        cls.assertEqual(max_length, 512)


class TagModelTest(TestCase):
    """Класс для тестирования модели тега"""

    fixtures = ["06-tags.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tag: Tag = Tag.objects.get(pk=1)

    def test_fixture_loading(cls) -> None:
        tag_count: int = Tag.objects.count()
        cls.assertEqual(tag_count, 35)

    def test_name_max_length(cls) -> None:
        max_length: int = cls.tag._meta.get_field("name").max_length
        cls.assertEqual(max_length, 100)


class BannerModelTest(TestCase):
    """Класс для тестирования модели баннера"""

    fixtures = ["15-banners.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.banner: Banner = Banner.objects.get(pk=1)

    def test_fixture_loading(cls) -> None:
        banners_count: int = Banner.objects.count()
        cls.assertEqual(banners_count, 4)

    def test_verbose_name(cls) -> None:
        banner: Banner = cls.banner
        field_verboses: dict = {"name": "названия", "actual": "актуальность", "preview": "превью", "link": "ссылка"}
        for field, expected_value in field_verboses.items():
            with cls.subTest(field=field):
                cls.assertEqual(banner._meta.get_field(field).verbose_name, expected_value)
