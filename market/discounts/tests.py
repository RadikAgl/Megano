"""Тесты приложения discounts"""

import os
from typing import List

from django.core.serializers import deserialize
from django.test import TestCase

from discounts.models import DiscountProduct, DiscountSet, DiscountCart
from settings_app.models import SiteSettings


class DiscountProductModelTest(TestCase):
    """Класс для тестирования модели скидок на продукты"""

    # todo попробовать так
    fixtures = ["05-categories.json", "06-tags.json", "07-products.json", "09-discounts_product.json"]

    # @classmethod
    # def setUpTestData(cls) -> None:
    #     cls.fixture_dir: str = SiteSettings.load().fixture_dir
    #     cls.fixtures: List[str] = [
    #         os.path.join(cls.fixture_dir, "05-categories.json"),
    #         os.path.join(cls.fixture_dir, "06-tags.json"),
    #         os.path.join(cls.fixture_dir, "07-products.json"),
    #         os.path.join(cls.fixture_dir, "09-discounts_product.json"),
    #     ]
    #     cls.load_fixtures()
    #
    # @classmethod
    # def load_fixtures(cls) -> None:
    #     for fixture_file in cls.fixtures:
    #         with open(fixture_file, "rb") as f:
    #             for obj in deserialize("json", f):
    #                 obj.save()

    def setUp(self) -> None:
        # super().setUp()  todo - эта инструкция нужна?
        self.discount: DiscountProduct = DiscountProduct.objects.get(pk=1)

    def test_fixture_loading(self) -> None:
        discount_products_count: int = DiscountProduct.objects.count()
        self.assertEqual(discount_products_count, 5)

    def test_name_max_length(self) -> None:
        max_length: int = self.discount._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)


class DiscountSetModelTest(TestCase):
    """Класс для тестирования модели скидок на продукты"""

    # todo попробовать так
    fixtures = ["05-categories.json", "06-tags.json", "07-products.json", "0-discounts_set.json"]

    # @classmethod
    # def setUpTestData(cls) -> None:
    #     cls.fixture_dir: str = SiteSettings.load().fixture_dir
    #     cls.fixtures: List[str] = [
    #         os.path.join(cls.fixture_dir, "05-categories.json"),
    #         os.path.join(cls.fixture_dir, "06-tags.json"),
    #         os.path.join(cls.fixture_dir, "07-products.json"),
    #         os.path.join(cls.fixture_dir, "10-discounts_set.json"),
    #     ]
    #     cls.load_fixtures()
    #
    # @classmethod
    # def load_fixtures(cls) -> None:
    #     for fixture_file in cls.fixtures:
    #         with open(fixture_file, "rb") as f:
    #             for obj in deserialize("json", f):
    #                 obj.save()

    def setUp(self) -> None:
        # super().setUp()  todo - эта инструкция нужна?
        self.discount: DiscountSet = DiscountSet.objects.get(pk=1)

    def test_fixture_loading(self) -> None:
        discount_set_count: int = DiscountSet.objects.count()
        self.assertEqual(discount_set_count, 5)

    def test_name_max_length(self) -> None:
        max_length: int = self.discount._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)


class DiscountCartModelTest(TestCase):
    """Класс для тестирования модели скидок на стоимость корзины"""
    # todo попробовать так
    fixtures = ["11-discounts_cart.json"]

    # @classmethod
    # def setUpTestData(cls) -> None:
    #     cls.fixture_dir: str = SiteSettings.load().fixture_dir
    #     cls.fixtures: List[str] = [
    #         os.path.join(cls.fixture_dir, "11-discounts_cart.json"),
    #     ]
    #     cls.load_fixtures()
    #
    # @classmethod
    # def load_fixtures(cls) -> None:
    #     for fixture_file in cls.fixtures:
    #         with open(fixture_file, "rb") as f:
    #             for obj in deserialize("json", f):
    #                 obj.save()

    def setUp(self) -> None:
        # super().setUp()  todo - эта инструкция нужна?
        self.discount: DiscountCart = DiscountCart.objects.get(pk=1)

    def test_fixture_loading(self) -> None:
        discount_cart_count: int = DiscountCart.objects.count()
        self.assertEqual(discount_cart_count, 5)

    def test_name_max_length(self) -> None:
        max_length: int = self.discount._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)
