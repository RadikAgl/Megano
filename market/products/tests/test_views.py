import os
from typing import Any, Dict, List
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.serializers import deserialize
from django.test import RequestFactory
from django.test import TestCase

from products.models import Product, Banner
from products.views import MainPageView
from settings_app.models import SiteSettings


class ProductDetailViewTestCase(TestCase):
    """
    Класс тестирования главной страницы
    """

    @classmethod
    def setUpTestData(cls) -> None:
        site_settings = SiteSettings.load()
        cls.fixture_dir: str = site_settings.fixture_dir
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


class TestMainPageView(TestCase):
    """Тестирование класса MainPageView."""

    def setUp(self) -> None:
        """Настройка теста."""
        self.factory = RequestFactory()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username="testuser", password="password")
        self.request = self.factory.get("/")
        self.request.user = self.user
        self.main_page_view: MainPageView = MainPageView(request=self.request)
        self.main_page_view.template_name: str = "products/index.jinja2"

    @patch("products.views.MainPageService")
    def test_get_context_data(self, MockMainPageService: Any) -> None:
        """Тестирование метода get_context_data."""
        # Заменяем экземпляр MainPageService на мок
        mock_main_page_service: Any = MockMainPageService.return_value

        # Мокируем метод get_products
        mock_products: List[str] = ["Product1", "Product2"]
        mock_main_page_service.get_top_products.return_value = mock_products

        # Мокируем метод banners_cache
        mock_banners: List[str] = ["Banner1", "Banner2"]
        mock_main_page_service.banners_cache.return_value = mock_banners

        # Вызываем тестируемый метод
        context: Dict[str, Any] = self.main_page_view.get_context_data()

        # Проверяем, были ли вызваны методы get_products и banners_cache
        mock_main_page_service.get_top_products.assert_called_once()
        mock_main_page_service.banners_cache.assert_called_once()

        # Проверяем, содержит ли контекст ожидаемые данные
        self.assertIn("products", context)
        self.assertIn("banners", context)
        self.assertEqual(context["products"], mock_products)
        self.assertEqual(context["banners"], mock_banners)
