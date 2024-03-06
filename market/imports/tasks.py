from typing import Optional

from celery import shared_task
from django.db import IntegrityError

from .common_utils import process_import_common, create_import_log


def process_import(file_name: str, user_id: int) -> None:
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


@shared_task(ignore_result=False)
def async_import_task(file_name: Optional[str] = None, user_id: Optional[int] = None) -> None:
    if file_name is None or user_id is None:
        return

    process_import(file_name, user_id)
