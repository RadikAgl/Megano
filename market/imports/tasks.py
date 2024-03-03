from django.db import IntegrityError

from .common_utils import process_import_common, create_import_log


def process_import(file_name, user_id):
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
    try:
        create_import_log(file_name, user_id, "В процессе выполнения")
        process_import_common(file_name, user_id)
    except IntegrityError as e:
        create_import_log(file_name, user_id, "Завершён с ошибкой", error_details=str(e))
    except Exception as e:
        create_import_log(file_name, user_id, "Завершён с ошибкой", error_details=str(e))
