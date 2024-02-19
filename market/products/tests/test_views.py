from django.test import TestCase
from django.urls import reverse

from products.models import Product, Category, Tag
from shops.models import Shop


class ProductDetailViewTest(TestCase):
    """
    Класс тестирования для детального просмотра продукта.

    Атрибуты:
    - fixtures (list): Список фикстур для загрузки данных перед выполнением тестов.
    """

    fixtures = [
        "02-users.json",
        "04-shops.json",
        "05-categories.json",
        "06-tags.json",
        "07-products.json",
        "08-offers.json",
    ]

    def setUp(self):
        """
        Метод настройки тестового окружения перед выполнением каждого теста.

        Создает экземпляры продукта, категории, магазина и тега для использования в тестах.
        """
        self.product = Product.objects.get(pk=1)
        self.category = Category.objects.get(pk=1)
        self.shop = Shop.objects.get(pk=1)
        self.tag = Tag.objects.get(pk=1)

    def test_product_detail_view(self):
        """
        Тест для проверки детального просмотра продукта.

        Параметры:
        - product: Экземпляр продукта.
        - category: Экземпляр категории.
        - shop: Экземпляр магазина.
        - response: Ответ сервера на запрос детальной информации о продукте.

        Проверяет, что при запросе детальной информации о продукте:
        - Код ответа сервера равен 200 (успех).
        - Имя продукта содержится в ответе.
        - Имя категории содержится в ответе.
        - Имя магазина содержится в ответе.
        """
        product = Product.objects.get(pk=1)
        category = Category.objects.get(pk=1)
        shop = Shop.objects.get(pk=1)

        response = self.client.get(reverse("product:details", args=[product.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.name)
        self.assertContains(response, category.name)
        self.assertContains(response, shop.name)
