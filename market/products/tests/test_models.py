from django.test import TestCase
from products.models import Product, Banner


class BannerModelTest(TestCase):
    """Класс тестов модели баннера"""

    @classmethod
    def setUpTestData(cls):
        cls.banner = Banner.objects.create(
            name="Тестовый баннер",
            actual=True,
            preview="",
        )

    def test_verbose_name(self):
        banner = Banner()
        field_verboses = {
            "name": "название",
            "actual": "актуальность",
            "preview": "превью",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(banner._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        banner = BannerModelTest.banner
        max_length = banner._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


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
