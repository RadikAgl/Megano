import json

from django.test import TestCase
from accounts.models import User
from products.models import Product, Category
from shops.models import Shop, Offer


class ShopModelTest(TestCase):
    """Класс тестов модели Магазин"""

    fixtures = ["02-users.json", "04-shops.json"]

    def test_fixture_loading(self):
        shop_count = Shop.objects.count()
        print(f"Actual shop count: {shop_count}")
        self.assertEqual(shop_count, 9)

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="тестовая категория")
        cls.product = Product.objects.create(
            name="тестовый продукт",
            category=category,
            details={"Диагональ, дм": 101},
        )

        cls.user = User.objects.create(username="testuser")
        cls.shop = Shop.objects.create(name="тестовый магазин", user=cls.user)
        cls.offer = Offer.objects.create(shop=cls.shop, product=cls.product, price=25)

    def test_verbose_name(self):
        shop = ShopModelTest.shop
        field_verboses = {
            "name": "название",
            "products": "товары в магазине",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(shop._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        shop = ShopModelTest.shop
        max_length = shop._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


class OfferModelTest(TestCase):
    """Класс тестов модели Предложение магазина"""

    fixtures = [
        "02-users.json",
        "04-shops.json",
        "05-categories.json",
        "06-tags.json",
        "07-products.json",
        "08-offers.json",
    ]

    def setUp(self):
        """Настроить тестовое окружение для каждого теста."""

        self.offer = Offer.objects.get(pk=1)

    def test_verbose_name(self):
        """Тест на проверку правильных имен полей модели."""

        field_verboses = {
            "price": "цена",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(self.offer._meta.get_field(field).verbose_name, expected_value)

    def test_price_max_digits(self):
        """Тест на проверку максимального числа цифр в цене."""

        max_digits = self.offer._meta.get_field("price").max_digits
        self.assertEqual(max_digits, 10)

    def test_price_decimal_places(self):
        """Тест на проверку десятичных знаков в цене."""

        decimal_places = self.offer._meta.get_field("price").decimal_places
        self.assertEqual(decimal_places, 2)

    def test_fixture_loading(self):
        """Тест загрузки данных через фикстуры."""

        with open("fixtures/08-offers.json", "r", encoding="utf-8") as file:
            offers_data = json.load(file)

        remains_products_in_offers = sum(
            entry["fields"]["remains"] for entry in offers_data if "fields" in entry and "remains" in entry["fields"]
        )

        shops_count = Shop.objects.count()
        offers_count = Offer.objects.count()

        print(f"Remains products count in offers: {remains_products_in_offers}")
        self.assertEqual(remains_products_in_offers, 2036)

        print(f"Shops count in offers: {shops_count}")
        self.assertEqual(shops_count, 8)
        print(f"Offers count : {offers_count}")
        self.assertEqual(offers_count, 69)
