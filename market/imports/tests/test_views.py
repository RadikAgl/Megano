import uuid

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from imports.models import ImportLog, ImportLogProduct
from products.models import Product, Category


class ImportPageViewTest(TestCase):
    """
    Класс тестирования представления страницы импорта.

    Methods:
        test_import_page_view(): Тестирование GET-запроса для страницы импорта.
    """

    def test_import_page_view(self):
        """
        Тестирование GET-запроса для страницы импорта.

        Ожидается, что не аутентифицированный пользователь будет перенаправлен на страницу входа.
        """
        response = self.client.get(reverse("imports:import-page"))
        self.assertRedirects(
            response, reverse("accounts:login") + "?next=" + reverse("imports:import-page"), target_status_code=200
        )


class ImportDetailsViewTest(TestCase):
    """
    Тестовый класс для представления деталей импорта.
    """

    def setUp(self):
        """
        Настройка данных для тестов.
        """
        self.user_email = f"testuser_{uuid.uuid4()}@example.com"
        self.user = User.objects.create_user(username="testuser", password="testpassword", email=self.user_email)
        self.import_log = ImportLog.objects.create(user=self.user)
        self.category = Category.objects.create(name="Some Category")

    def test_import_details_view(self):
        """
        Тестирование GET-запроса для представления деталей импорта.
        """
        response = self.client.get(reverse("imports:import-details"), follow=True)
        self.assertRedirects(
            response,
            reverse("accounts:login") + "?next=" + reverse("imports:import-details"),
            target_status_code=200,
        )

    def test_authenticated_user_access(self):
        """
        Тестирование доступа для аутентифицированного пользователя.
        """

        # Аутентификация пользователя
        self.client.login(username="testuser", password="testpassword")

        # Отправка GET-запроса для представления деталей импорта
        response = self.client.get(reverse("imports:import-details"), follow=True)

        # Проверка, что ответ перенаправляет на страницу входа
        self.assertRedirects(
            response,
            reverse("accounts:login") + "?next=" + reverse("imports:import-details"),
        )

    def test_unauthenticated_user_access(self):
        """
        Тестирование доступа для неаутентифицированного пользователя.
        """

        # Отправка GET-запроса для представления деталей импорта
        response = self.client.get(reverse("imports:import-details"), args=[self.import_log.id], follow=True)

        # Проверка, что ответ перенаправляет на страницу входа
        self.assertRedirects(
            response,
            reverse("accounts:login") + "?next=" + reverse("imports:import-details"),
        )

    def test_import_counts(self):
        """
        Тестирование импорта количества.
        """

        # Создание некоторых продуктов
        some_product = Product.objects.create(name="Some Product", category=self.category)
        another_product = Product.objects.create(name="Another Product", category=self.category)

        # Создание импорта продуктов для журнала импорта
        ImportLogProduct.objects.create(import_log=self.import_log, product=some_product)
        ImportLogProduct.objects.create(import_log=self.import_log, product=another_product)

        # Аутентификация пользователя
        self.client.login(username="testuser", password="testpassword")

        # Отправка GET-запроса для представления деталей импорта
        response = self.client.get(reverse("imports:import-details"), follow=True)

        # Проверка, что код статуса ответа равен 200
        self.assertEqual(response.status_code, 200)


class DownloadCSVTemplateViewTest(TestCase):
    """
    Класс тестирования представления скачивания шаблона CSV-файла.

    Methods:
        test_download_csv_template_view(): Тестирование GET-запроса для скачивания шаблона CSV-файла.
    """

    def test_download_csv_template_view(self):
        """
        Тестирование GET-запроса для скачивания шаблона CSV-файла.

        Ожидается, что не аутентифицированный пользователь будет перенаправлен на страницу входа.
        """
        response = self.client.get(reverse("imports:download-csv-template"))
        self.assertRedirects(
            response,
            reverse("accounts:login") + "?next=" + reverse("imports:download-csv-template"),
            target_status_code=200,
        )
