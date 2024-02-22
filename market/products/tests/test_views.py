from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product


class DetailViewTest(TestCase):
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
        "14-images.json",
    ]

    def test_product_detail_view(self):
        """
        Тест для проверки детального просмотра продукта.
        Параметры:
        - product: Экземпляр продукта.
        - category: Экземпляр категории.
        - shops: Список магазинов.
        - response: Ответ сервера на запрос детальной информации о продукте.

        Проверяет, что при запросе детальной информации о продукте:
        - Код ответа сервера равен 200 (успех).
        - Имя продукта содержится в ответе.
        - Имя категории содержится в ответе.
        - Имена всех магазинов содержатся в ответе.
        """

        product = Product.objects.get(pk=1)
        category = Category.objects.get(pk=1)
        shops = list(product.shops.all())
        images = list(product.images.all())

        # Use the 'pk' as the URL parameter for the detail view
        response = self.client.get(reverse("product:product-details", kwargs={"product_id": product.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.name)
        self.assertContains(response, category.name)

        for shop in shops:
            self.assertContains(response, shop.name)
        count = 0
        for image in images:
            count += 1
            self.assertContains(response, image.image)  # Assuming 'image' is a string field
        print(f"product images: {count}")
