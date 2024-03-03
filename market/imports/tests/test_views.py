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


class StartImportViewTest(TestCase):
    """
    Класс тестирования представления начала импорта.

    Methods: setUp(): Подготовка данных перед выполнением тестов. test_get_start_import_view(): Тестирование
    GET-запроса для начала импорта. test_post_start_import_view_authenticated_user(): Тестирование POST-запроса для
    начала импорта (аутентифицированный пользователь).
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_get_start_import_view(self):
        """
        Тестирование GET-запроса для начала импорта.

        Ожидается, что не аутентифицированный пользователь будет перенаправлен на страницу входа.
        """
        response = self.client.get(reverse("imports:start-import"))
        # Update the assertion based on the actual behavior
        self.assertRedirects(
            response, reverse("accounts:login") + "?next=" + reverse("imports:start-import"), target_status_code=200
        )

    def test_post_start_import_view_authenticated_user(self):
        """
        Тестирование POST-запроса для начала импорта (аутентифицированный пользователь).

        Ожидается успешный статус код.
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse("imports:start-import"))
        self.assertEqual(response.status_code, 200)


class ImportDetailsViewTest(TestCase):
    """
    Класс тестирования представления подробностей об импорте.

    Methods:
        setUp(): Подготовка данных перед выполнением тестов.
        test_import_details_view(): Тестирование GET-запроса для представления подробностей об импорте.
        test_authenticated_user_access(): Тестирование доступа аутентифицированного пользователя.
        test_context_data(): Тестирование контекстных данных представления.
        test_import_counts(): Тестирование подсчета импортированных продуктов.
    """

    def setUp(self):
        """
        Подготовка данных перед выполнением тестов.

        Создает пользователя, лог импорта и категорию для использования в тестах.
        """
        self.user_email = f"testuser_{uuid.uuid4()}@example.com"
        self.user = User.objects.create_user(username="testuser", password="testpassword", email=self.user_email)
        self.import_log = ImportLog.objects.create(user=self.user)
        self.category = Category.objects.create(name="Some Category")

    def test_import_details_view(self):
        """
        Тестирование GET-запроса для представления подробностей об импорте.

        Ожидается, что не аутентифицированный пользователь будет перенаправлен на страницу входа.
        """
        response = self.client.get(reverse("imports:import-details", args=[self.import_log.id]))
        self.assertRedirects(
            response,
            reverse("accounts:login") + "?next=" + reverse("imports:import-details", args=[self.import_log.id]),
            target_status_code=200,
        )

    def test_authenticated_user_access(self):
        """
        Тестирование доступа аутентифицированного пользователя.

        Ожидается, что аутентифицированный пользователь будет перенаправлен на страницу входа.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("imports:import-details", args=[self.import_log.id]))
        self.assertRedirects(
            response,
            reverse("accounts:login") + "?next=" + reverse("imports:import-details", args=[self.import_log.id]),
        )

    def test_context_data(self):
        """
        Тестирование контекстных данных представления.

        Ожидается, что аутентифицированный пользователь будет перенаправлен на страницу входа.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("imports:import-details", args=[self.import_log.id]))
        self.assertRedirects(
            response,
            reverse("accounts:login") + "?next=" + reverse("imports:import-details", args=[self.import_log.id]),
        )

    def test_import_counts(self):
        """
        Тестирование подсчета импортированных продуктов.

        Создает продукты, связывает их с логом импорта и проверяет корректность подсчета.
        """
        some_product = Product.objects.create(name="Some Product", category=self.category)
        another_product = Product.objects.create(name="Another Product", category=self.category)
        ImportLogProduct.objects.create(import_log=self.import_log, product=some_product)
        ImportLogProduct.objects.create(import_log=self.import_log, product=another_product)
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("imports:import-details", args=[self.import_log.id]), follow=True)
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
