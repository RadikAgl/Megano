import os

from django.core.serializers import deserialize
from django.test import TestCase
from django.urls import reverse

from products.models import Product, Banner
from settings_app.models import SiteSettings


class ProductDetailViewTestCase(TestCase):
    """
    Класс тестирования главной страницы
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.fixture_dir: str = SiteSettings.load().fixture_dir
        cls.fixtures = [
            os.path.join(cls.fixture_dir, "05-categories.json"),
            os.path.join(cls.fixture_dir, "06-tags.json"),
            os.path.join(cls.fixture_dir, "07-products.json"),
            os.path.join(cls.fixture_dir, "15-banners.json"),
        ]
        cls.load_fixtures()

    @classmethod
    def load_fixtures(cls) -> None:
        for fixture_file in cls.fixtures:
            with open(fixture_file, "rb") as fixture:
                for obj in deserialize("json", fixture, ignorenonexistent=True):
                    obj.save()

    def setUp(self) -> None:
        """
        Метод настройки окружения для тестирования.
        Создает экземпляр Продукта, Баннера
        """
        self.product = Product.objects.get(pk=1)
        self.banner = Banner.objects.get(pk=1)

    def test_index_view(self) -> None:
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
