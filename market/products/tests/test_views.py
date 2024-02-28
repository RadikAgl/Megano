﻿from django.test import TestCase
from django.urls import reverse

from products.models import Product, Banner


class ProductDetailViewTestCase(TestCase):
    """
    Класс тестирования главной страницы
    """

    fixtures = [
        "01-groups.json",
        "02-users.json",
        "04-shops.json",
        "05-categories.json",
        "06-tags.json",
        "07-products.json",
        "08-offers.json",
        "14-images.json",
        "15-banners.json",
    ]

    def setUp(self):
        """
        Метод настройки окружения для тестирования.
        Создает экземпляр Продукта, Баннера
        """
        self.product = Product.objects.get(pk=1)
        self.banner = Banner.objects.get(pk=1)

    def test_index_view(self):
        """
        Метод тестирования главной страницы.
        Проверяет:
         - Код ответа: 200 (успешный статус ответа)
         - Содержатся ли "banners" в контексте ответа
         - Содержатся ли "products" в контексте ответа
         - Имя продукта содержится в ответе
        """

        response = self.client.get(reverse("products:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "banners")
        self.assertContains(response, "products")
        self.assertContains(response, self.product.name)
