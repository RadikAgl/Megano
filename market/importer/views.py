import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from .common_utils import process_import_common
from .models import ImportLog

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ImportPageView(LoginRequiredMixin, TemplateView):
    """
    Представление для отображения страницы импорта.

    Шаблон: 'importer/import_page.jinja2'
    """

    template_name = "importer/import_page.jinja2"

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

    Шаблон: 'importer/start-import.jinja2'
    Успешный шаблон: 'importer/start-import.jinja2'
    """

    template_name = "importer/start-import.jinja2"
    success_template_name = "importer/start-import.jinja2"
    error_template_name = "importer/start-import.jinja2"

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
            user = request.user  # Ensure you are getting the user from the request

            # Ensure the user is authenticated before creating the ImportLog
            if user.is_authenticated:
                import_log_instance = ImportLog.objects.create(user=user, file_name=file_name.name)
                process_import_common(file_name, user.id, import_log_instance)

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


class ImportDetailsView(LoginRequiredMixin, TemplateView):
    """
    Представление для отображения деталей импорта.

    Шаблон: 'importer/import_details.jinja2'

    Методы:
    - get: Обработка GET-запроса для страницы деталей импорта.

    Атрибуты:
    - template_name (str): Имя шаблона для отображения деталей импорта.
    """

    template_name = "importer/import_details.jinja2"

    def get(self, request, *args, **kwargs):
        """
        Обработка GET-запроса для страницы деталей импорта.

        Параметры:
        - import_id (int): Идентификатор импорта.

        Если импорт существует, извлекаются продукты, связанные с импортом, и передаются в контекст шаблона.
        """
        import_id = kwargs.get("import_id")
        import_log = get_object_or_404(ImportLog, id=import_id)
        imported_products = import_log.products.all()

        context = {"import_log": import_log, "imported_products": list(imported_products)}

        return self.render_to_response(context)


class DownloadCSVTemplateView(LoginRequiredMixin, View):
    """
    Представление для скачивания шаблона CSV-файла.

    URL: /download-csv-template/
    """

    def get(self, request, *args, **kwargs):
        """
        Обработка GET-запроса для скачивания шаблона CSV-файла.

        Если файл не найден, возвращается сообщение о том, что файл не найден.
        Если файл найден, открывается и возвращается HTTP-ответ с содержимым файла и заголовками.

        В случае ошибки при открытии файла, возвращается сообщение об ошибке.
        """
        file_path = finders.find("importer/Sheet1.csv")

        if file_path is None:
            return HttpResponse("Файл не найден!")

        try:
            with open(file_path, "rb") as file:
                response = HttpResponse(file.read(), content_type="text/csv")
                response["Content-Disposition"] = 'attachment; filename="Sheet1.csv"'
            return response
        except Exception as e:
            logging.error(f"Ошибка при открытии файла: {str(e)}")
            return HttpResponse("Ошибка при открытии файла.")
