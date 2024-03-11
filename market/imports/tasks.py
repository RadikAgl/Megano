from typing import Optional

from celery import shared_task
from django.db import IntegrityError, transaction

from .common_utils import process_import_common, create_import_log, logger
from django.core.cache import cache


@transaction.atomic
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
        create_import_log(
            file_name,
            user_id,
            "В процессе выполнения",
        )
        process_import_common(file_name, user_id)
    except IntegrityError as e:
        create_import_log(file_name, user_id, "Завершён с ошибкой", error_details=str(e))
        # Optionally, you can re-raise the IntegrityError if you want to log it separately or handle it differently.
        raise
    except Exception as e:
        create_import_log(file_name, user_id, "Завершён с ошибкой", error_details=str(e))
        # Optionally, you can re-raise the exception if you want to log it separately or handle it differently.
        raise


@shared_task(ignore_result=False)
def async_import_task(file_name: Optional[str] = None, user_id: Optional[int] = None) -> None:
    if file_name is None or user_id is None:
        return

    # Use a unique key based on file_name and user_id
    task_key = f"async_import_task:{file_name}:{user_id}"

    # Check if the task has already been enqueued
    if cache.get(task_key):
        logger.info(f"Task already enqueued for file: {file_name}, user: {user_id}")
        return

    logger.info(f"Enqueuing async_import_task for file: {file_name}, user: {user_id}")

    try:
        # Your existing task logic here
        process_import(file_name, user_id)
    except Exception as e:
        logger.error(f"Error in async_import_task: {e}")
    finally:
        # Set a cache entry to mark that the task has been enqueued
        cache.set(task_key, "enqueued", timeout=None)
