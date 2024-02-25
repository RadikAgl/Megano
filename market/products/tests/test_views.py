from django.test import TestCase
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
        Создает экземпляры Продукта, Баннера
        """
        self.product = Product.objects.get(pk=1)
        self.banner = Banner.objects.get(pk=1)

    def test_index_view(self):
        """
        Метод тестирования главной страницы.
        Проверяет:
         - Код ответа: 200 (успешный статус ответа)
         - Имя продукта содержится в ответе
         - Имя баннера содержится в ответе
        """

        product = Product.objects.get(pk=1)
        banner = Banner.objects.get(pk=1)

        response = self.client.get(reverse("products:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.name)
        self.assertContains(response, banner.name)
