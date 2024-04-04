from django.contrib.auth import get_user_model
from django.test import TestCase

from comparison.models import Comparison
from products.models import Product, Category, Tag

User = get_user_model()


class ComparisonModelTestCase(TestCase):
    """
    Тест модели сравнения.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Настройка теста.
        """
        super().setUpClass()

        # Создание пользователя
        cls.user: User = User.objects.create_user(username="testuser", password="12345")

        # Создание некоторых категорий
        cls.category: Category = Category.objects.create(name="Тестовая категория")

        # Создание некоторых тегов
        cls.tag1: Tag = Tag.objects.create(name="Тег1")
        cls.tag2: Tag = Tag.objects.create(name="Тег2")

        # Создание некоторых продуктов
        cls.product1: Product = Product.objects.create(
            name="Продукт 1", category=cls.category, description="Описание 1"
        )
        cls.product1.tags.add(cls.tag1)

        cls.product2: Product = Product.objects.create(
            name="Продукт 2", category=cls.category, description="Описание 2"
        )
        cls.product2.tags.add(cls.tag2)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Очистка данных после завершения теста.
        """
        super().tearDownClass()
        # Очистка данных
        Comparison.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        User.objects.all().delete()

    def test_comparison_creation(self) -> None:
        """
        Тест создания сравнения.
        """
        # Создание экземпляра сравнения
        comparison: Comparison = Comparison.objects.create(user=self.user)

        # Добавление продуктов в сравнение
        comparison.products.add(self.product1, self.product2)

        # Получение созданного сравнения
        saved_comparison: Comparison = Comparison.objects.get(user=self.user)

        # Проверки
        self.assertEqual(saved_comparison.user, self.user)
        self.assertIn(self.product1, saved_comparison.products.all())
        self.assertIn(self.product2, saved_comparison.products.all())
        self.assertIsNotNone(saved_comparison.created_at)
