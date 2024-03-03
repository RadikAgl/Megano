import logging
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView

from .common_utils import process_import_common
from .models import ImportLog, ImportLogProduct


class ImportPageView(LoginRequiredMixin, TemplateView):
    """
    Представление для отображения страницы импорта.

    Шаблон: 'imports/import_page.jinja2'
    """

    template_name = "imports/import_page.jinja2"

    def get_context_data(self, **kwargs):
        """
        Получение контекстных данных для шаблона страницы импорта.
        """
        context = super().get_context_data(**kwargs)
        context["import_logs"] = ImportLog.objects.all()
        return context


@method_decorator(login_required, name="dispatch")
class StartImportView(LoginRequiredMixin, View):
    """
    Представление для начала процесса импорта.

    Шаблон: 'imports/start_import.jinja2'
    Успешный шаблон: 'imports/start_import.jinja2'
    """

    template_name = "imports/start_import.jinja2"
    success_template_name = "imports/start_import.jinja2"
    error_template_name = "imports/start_import.jinja2"

    def get(self, request, *args, **kwargs):
        """
        Обработка GET-запроса, возможно, отображение некоторой информации.
        """
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """
        Обработка POST-запроса, начало процесса импорта.

        Параметры:
        - importFile: файл для импорта

        Если пользователь аутентифицирован, создается экземпляр ImportLog,
        и вызывается процесс импорта через common_utils.process_import_common.
        В случае успеха, возвращается успешный шаблон, иначе возвращается шаблон с ошибкой.
        """
        try:
            file_name = request.FILES.get("importFile")
            user = request.user

            if user.is_authenticated:
                process_import_common(file_name, user.id)

                return render(
                    request,
                    self.success_template_name,
                    {"success_message": "Процесс импорта успешно запущен.", "import_complete": True},
                )
            else:
                # Redirect to the login page if the user is not authenticated
                return redirect(reverse_lazy("account_login"))
        except Exception as e:
            error_message = str(e)
            return render(
                request, self.error_template_name, {"error_message": error_message, "import_complete": False}
            )


class ImportDetailsView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения подробностей об импорте.

    Атрибуты:
        model (ImportLog): Модель для данного представления - ImportLog.
        template_name (str): Имя шаблона для отображения - 'imports/import_details.jinja2'.
        context_object_name (str): Имя объекта контекста - 'import_log'.

    Methods:
        get_context_data(**kwargs): Получение контекстных данных для передачи в шаблон.
        get(request, *args, **kwargs): Обработка GET-запроса для представления.

    """

    model = ImportLog
    template_name = "imports/import_details.jinja2"
    context_object_name = "import_log"

    def get_context_data(self, **kwargs):
        """
        Получение контекстных данных для передачи в шаблон.

        Возвращает информацию о логе импорта, списке импортированных продуктов и
        количестве успешных и неудачных импортов.

        Returns:
            dict: Словарь с контекстными данными.
        """
        import_log = self.get_object()
        imported_products = (
            ImportLogProduct.objects.filter(import_log=import_log).select_related("product").distinct("product")
        )

        # Подсчет успешных импортов
        successful_imports_count = imported_products.filter(import_log__status="Выполнен").count()

        # Подсчет неудачных импортов
        failed_imports_count = imported_products.filter(import_log__status="Завершён с ошибкой").count()

        context = {
            "import_log": import_log,
            "imported_products": imported_products,
            "successful_imports_count": successful_imports_count,
            "failed_imports_count": failed_imports_count,
        }
        return context

    def get(self, request, *args, **kwargs):
        """
        Обработка GET-запроса для представления.

        Получает контекстные данные и рендерит шаблон.

        Args:
            request (HttpRequest): Объект запроса.
            args: Позиционные аргументы.
            kwargs: Именованные аргументы.

        Returns:
            HttpResponse: Ответ с отображенным шаблоном и контекстными данными.
        """
        import_log = self.get_object()
        imported_products = (
            ImportLogProduct.objects.filter(import_log=import_log).select_related("product").distinct("product")
        )
        context = self.get_context_data(import_log=import_log, imported_products=imported_products)
        return render(request, self.template_name, context)


class DownloadCSVTemplateView(LoginRequiredMixin, View):
    """
    Представление для скачивания шаблона CSV-файла.

    Attributes:
        docs_dir (str): Путь к директории с документами.
        file_name (str): Имя CSV-файла.
        file_path (str): Полный путь к CSV-файлу.

    Methods:
        get(request, *args, **kwargs): Обработка GET-запроса для скачивания файла.
    """

    def get(self, request, *args, **kwargs):
        """
        Обработка GET-запроса для скачивания файла.

        Parameters:
            request (HttpRequest): Объект запроса.
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.

        Returns:
            HttpResponse: HTTP-ответ с содержимым CSV-файла.
        """
        docs_dir = "./docs"
        file_name = "Sheet1.csv"
        file_path = os.path.join(docs_dir, file_name)

        if not os.path.isfile(file_path):
            return HttpResponse("File not found!")

        try:
            with open(file_path, "rb") as file:
                response = HttpResponse(file.read(), content_type="text/csv")
                response["Content-Disposition"] = f'attachment; filename="{file_name}"'
            return response
        except Exception as e:
            logging.error(f"Error opening file: {str(e)}")
            return HttpResponse("Error opening file.")
