from django.test import TestCase
from django.contrib.auth import get_user_model
from comparison.models import Comparison
from products.models import Product, Category, Tag

User = get_user_model()


class ComparisonModelTestCase(TestCase):
    """
    Тест модели сравнения.
    """

    def setUp(self):
        """
        Настройка теста.
        """
        # Создание пользователя
        self.user = User.objects.create_user(username="testuser", password="12345")

        # Создание некоторых категорий
        self.category = Category.objects.create(name="Тестовая категория")

        # Создание некоторых тегов
        self.tag1 = Tag.objects.create(name="Тег1")
        self.tag2 = Tag.objects.create(name="Тег2")

        # Создание некоторых продуктов
        self.product1 = Product.objects.create(name="Продукт 1", category=self.category, description="Описание 1")
        self.product1.tags.add(self.tag1)

        self.product2 = Product.objects.create(name="Продукт 2", category=self.category, description="Описание 2")
        self.product2.tags.add(self.tag2)

    def test_comparison_creation(self):
        """
        Тест создания сравнения.
        """
        # Создание экземпляра сравнения
        comparison = Comparison.objects.create(user=self.user)

        # Добавление продуктов в сравнение
        comparison.products.add(self.product1, self.product2)

        # Получение созданного сравнения
        saved_comparison = Comparison.objects.get(user=self.user)

        # Проверки
        self.assertEqual(saved_comparison.user, self.user)
        self.assertIn(self.product1, saved_comparison.products.all())
        self.assertIn(self.product2, saved_comparison.products.all())
        self.assertIsNotNone(saved_comparison.created_at)
