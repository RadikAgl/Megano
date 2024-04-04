from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.test import TestCase

from products.views import MainPageView


class TestMainPageView(TestCase):
    """Тестирование класса MainPageView."""

    @classmethod
    def setUpClass(cls) -> None:
        """Настройка теста."""
        super().setUpClass()
        cls.factory = RequestFactory()
        cls.user_model = get_user_model()
        cls.user = cls.user_model.objects.create_user(username="testuser", password="password")
        cls.request = cls.factory.get("/")
        cls.request.user = cls.user
        cls.main_page_view = MainPageView(request=cls.request)
        cls.main_page_view.template_name = "products/index.jinja2"

    @classmethod
    def tearDownClass(cls) -> None:
        """Завершение теста."""
        super().tearDownClass()

    @patch("products.views.MainPageService")
    def test_get_context_data(cls, MockMainPageService):
        """Тестирование метода get_context_data."""
        # Заменяем экземпляр MainPageService на мок
        mock_main_page_service = MockMainPageService.return_value

        # Мокируем метод get_products
        mock_products = ["Product1", "Product2"]
        mock_main_page_service.get_top_products.return_value = mock_products

        # Мокируем метод banners_cache
        mock_banners = ["Banner1", "Banner2"]
        mock_main_page_service.banners_cache.return_value = mock_banners

        # Вызываем тестируемый метод
        context = cls.main_page_view.get_context_data()

        # Проверяем, были ли вызваны методы get_products и banners_cache
        mock_main_page_service.get_top_products.assert_called_once()
        mock_main_page_service.banners_cache.assert_called_once()

        # Проверяем, содержит ли контекст ожидаемые данные
        cls.assertIn("top_products", context)
        cls.assertIn("banners", context)
        cls.assertEqual(context["top_products"], mock_products)
        cls.assertEqual(context["banners"], mock_banners)
