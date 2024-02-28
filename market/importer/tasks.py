from celery import shared_task

from .common_utils import process_import_common


@shared_task
def process_import(file_name, user, import_log_instance):
    """
    Задача для обработки импорта продукции из CSV-файла.

    Параметры:
    - file_name: Имя CSV-файла для импорта.

    Вызывает:
    - IntegrityError: В случае ошибок целостности базы данных.
    - Exception: Для обработки неожиданных ошибок.

    Возвращает:
    - None
    """
    process_import_common(file_name, user, import_log_instance)
