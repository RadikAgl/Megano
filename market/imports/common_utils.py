import logging
import os
import time
from _csv import reader
from typing import List, Optional, Tuple

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.utils import timezone

from accounts.models import User
from products.models import Category, Product, Tag
from shops.models import Offer, Shop
from .models import ImportLog, ImportLogProduct

logger = logging.getLogger(__name__)

lock_key = "import_lock"


def acquire_lock():
    """
    Acquires the lock. If the lock already exists, waits for 1 second and retries.
    Creates a cache entry for the lock.

    Returns:
        None
    """
    while cache.get(lock_key):
        time.sleep(1)
    cache.set(lock_key, "locked")


def release_lock():
    """
    Releases the lock by deleting the cache entry.

    Returns:
        None
    """
    cache.delete(lock_key)


def create_or_update_category(name: str, parent_name: str = None, parent_id: int = None) -> Tuple[Category, bool]:
    """
    Создает или обновляет категорию.

    Args:
        name (str): Название категории.
        parent_name (str, optional): Название родительской категории. По умолчанию None.
        parent_id (int, optional): ID родительской категории. По умолчанию None.

    Returns:
        Tuple[Category, bool]: Кортеж с объектом категории и флагом, указывающим на создание (True)
         или обновление (False).
    """
    sort_index = get_next_sort_index(parent_id)

    try:
        defaults = {"sort_index": sort_index}
        if parent_name or parent_id:
            parent_filter = {"name": parent_name} if parent_name else {"id": parent_id}
            parent, _ = Category.objects.get_or_create(**parent_filter)
            defaults["parent"] = parent

        if parent_id is not None and not isinstance(parent_id, int):
            parent_id = int(parent_id)

        category, created = Category.objects.get_or_create(name=name, defaults=defaults)

        return category, created
    except IntegrityError as e:  # noqa
        return None, False


def get_next_sort_index(parent_id: int = None) -> int:
    """
    Возвращает следующий уникальный sort_index для категории.

    Args:
        parent_id (int, optional): ID родительской категории. По умолчанию None.

    Returns:
        int: Следующий уникальный sort_index.
    """
    existing_sort_indexes = Category.objects.filter(parent_id=parent_id).values_list("sort_index", flat=True)

    sort_index = 1
    while sort_index in existing_sort_indexes:
        sort_index += 1

    return sort_index


def create_product_and_offer(product_data, import_log, user_id):
    (
        name,
        main_category_name,
        subcategory_name,
        description,
        details,
        tags,
        price,
        remains,
    ) = product_data

    main_category, _ = create_or_update_category(main_category_name)
    create_or_update_category(subcategory_name, parent_name=main_category_name)
    tag_objects = [create_or_update_tag(tag) for tag in tags]  # noqa
    category = create_or_update_category(main_category_name)[0]

    product = Product.objects.create(name=name, category=category, description=description, details=details)
    product.tags.set(tags)

    import_log_product = ImportLogProduct.objects.create(import_log=import_log, product=product)  # noqa
    import_log.products.add(product)

    shop = get_user_shop(user_id)
    create_or_update_offer(shop, product, price, remains)


def get_user_shop(user_id: int) -> Shop:
    """
    Возвращает магазин пользователя.

    Args:
        user_id (int): ID пользователя.

    Returns:
        Shop: Магазин пользователя.
    """
    user = User.objects.get(id=user_id)
    return user.shop


def get_shop_name(user_id: int) -> str:
    """
    Retrieves the shop name for a given user ID.

    Args:
        user_id (int): ID of the user.

    Returns:
        str: Shop name.
    """
    user = User.objects.get(id=user_id)
    shop = user.shop
    return shop.name


def create_or_update_offer(shop: Shop, product: Product, price: float, remains: int) -> bool:
    """
    Создает или обновляет предложение в магазине для продукта.

    Args:
        shop (Shop): Магазин.
        product (Product): Продукт.
        price (float): Цена предложения.
        remains (int): Остаток предложения.

    Returns:
        bool: True, если предложение было создано; False, если было обновлено.
    """
    offer, created = Offer.objects.get_or_create(
        shop=shop, product=product, defaults={"price": price, "remains": remains}
    )
    return created


def log_and_notify_error(
    error_message: str, user_id: int, file_name: str, total_products: int, successful_imports: int, failed_imports: int
) -> str:
    """
    Логгирует ошибку импорта и отправляет уведомление о ошибке.

    Args:
        error_message (str): Сообщение об ошибке.
        user_id (int): ID пользователя.
        file_name (str): Имя файла импорта.
        total_products (int): Общее количество товаров в файле.
        successful_imports (int): Количество успешных импортов.
        failed_imports (int): Количество неудачных импортов.

    Returns:
        str: Строка с деталями ошибки.
    """
    try:
        user = User.objects.get(id=user_id)
        import_log = ImportLog.objects.create(file_name=file_name, status="Завершён с ошибкой", user=user)
        import_log.error_details = error_message
        import_log.save()

        send_mail(
            "Ошибка при импорте",
            f"Возникла ошибка во время импорта файла {file_name}.\nОшибка: {error_message}\n"
            f"Загружено пользователем: {user.username} ({user.email}).\n"
            f"Всего товаров: {total_products}\n"
            f"Успешные импорты: {successful_imports}\n"
            f"Неудачные импорты: {failed_imports}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
    except Exception as e:
        return str(e)


def create_or_update_tag(name: str) -> Tag:
    """
    Создает или обновляет тег.

    Args:
        name (str): Название тега.

    Returns:
        Tag: Созданный или существующий тег.
    """
    tag, created = Tag.objects.get_or_create(name=name)
    return tag


def create_import_log(
    file_name: str,
    user: User,
    status: str,
    total_products: int = 0,
    successful_imports: int = 0,
    failed_imports: int = 0,
    error_details: str = None,
) -> ImportLog:
    """
    Создает лог импорта.

    Args:
        file_name (str): Имя файла импорта.
        user (User): Пользователь, загрузивший файл.
        status (str): Статус импорта.
        total_products (int, optional): Общее количество товаров в файле. По умолчанию 0.
        successful_imports (int, optional): Количество успешных импортов. По умолчанию 0.
        failed_imports (int, optional): Количество неудачных импортов. По умолчанию 0.
        error_details (str, optional): Строка с деталями ошибки. По умолчанию None.

    Returns:
        ImportLog: Созданный лог импорта.
    """
    logger.info(f"Creating import log for file: {file_name}, user: {user.id}")
    import_log = ImportLog.objects.create(
        file_name=file_name,
        user=user,
        status=status,
        timestamp=timezone.now(),
        total_products=total_products,
        successful_imports=successful_imports,
        failed_imports=failed_imports,
        error_details=error_details,
    )
    logger.info(f"Import log created for file: {file_name}, user: {user.id}")
    return import_log


def notify_admin_about_import_success(
    user_id: int, file_name: str, total_products: int, successful_imports: int, failed_imports: int
) -> None:
    """
    Оповещает администратора о успешном завершении импорта.

    Args:
        user_id (int): ID пользователя.
        file_name (str): Имя файла импорта.
        total_products (int): Общее количество товаров в файле.
        successful_imports (int): Количество успешных импортов.
        failed_imports (int): Количество неудачных импортов.
    """
    user = User.objects.get(id=user_id)
    message = (
        f"Импорт файла {file_name} успешно завершен.\n"
        f"Загружено пользователем: {user.username} ({user.email}).\n"
        f"Всего товаров: {total_products}\n"
        f"Успешных импортов: {successful_imports}\n"
        f"Неудачных импортов: {failed_imports}"
    )
    send_mail(
        "Импорт успешно завершен",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )


@transaction.atomic
def process_import_common(uploaded_file, user_id: int) -> str:
    logger.info(f"Processing import for file: {uploaded_file.name}, user: {user_id}")
    successful_imports_dir = os.path.join(settings.DOCS_DIR[0], settings.SUCCESSFUL_IMPORTS_DIR)
    failed_imports_dir = os.path.join(settings.DOCS_DIR[0], settings.FAILED_IMPORTS_DIR)

    try:
        acquire_lock()
        file_name = uploaded_file.name
        content = uploaded_file.read().decode("utf-8")

        if not content.strip():
            return handle_empty_file(file_name, user_id)

        lines = content.split("\n")
        csv_rows = reader(lines)
        total_products, successful_imports, failed_imports = 0, 0, 0

        user = User.objects.get(id=user_id)
        import_log = create_import_loger(file_name, user)

        for row in csv_rows:
            try:
                product_data = extract_data_from_row(row)

                if product_data is None:
                    continue

                create_product_and_offer(product_data, import_log, user_id)
                total_products += 1
                successful_imports += 1

            except IndexError as index_error:
                print(f"Failed to process row due to error: {str(index_error)}")
                handle_failed_import(
                    index_error, file_name, user_id, total_products, successful_imports, failed_imports
                )
                failed_imports += 1

            except Exception as e:
                print(f"Unhandled exception occurred: {str(e)}")
                handle_failed_import(e, file_name, user_id, total_products, successful_imports, failed_imports)
                failed_imports += 1

    except (IntegrityError, Exception) as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message)
        handle_failed_import(e, file_name, user_id, total_products, successful_imports, failed_imports)
        return error_message
    finally:
        logger.info(f"Import process completed for file: {uploaded_file.name}, user: {user_id}")
        handle_import_log_status(import_log, successful_imports, failed_imports)
        handle_destination_path(file_name, content, import_log, successful_imports_dir, failed_imports_dir)
        transaction.on_commit(lambda: release_lock())


def handle_empty_file(file_name, user_id):
    error_message = "Uploaded file is empty"
    return log_and_notify_error(error_message, user_id, file_name, 0, 0, 1)


def create_import_loger(file_name, user):
    return ImportLog.objects.create(file_name=file_name, user=user, status="in_progress")


def handle_failed_import(error, file_name, user_id, total_products, successful_imports, failed_imports):
    log_and_notify_error(str(error), user_id, file_name, total_products, successful_imports, failed_imports)


def handle_import_log_status(import_log, successful_imports, failed_imports):
    if failed_imports > 0:
        import_log.status = "Завершён с ошибкой"
    else:
        import_log.status = "Выполнен"

    import_log.total_products = successful_imports + failed_imports
    import_log.successful_imports = successful_imports
    import_log.failed_imports = failed_imports
    import_log.save()


def handle_destination_path(file_name, content, import_log, successful_imports_dir, failed_imports_dir):
    os.makedirs(failed_imports_dir, exist_ok=True)

    new_file_name = f"{import_log.timestamp.strftime('%H-%M-%S_%d-%m-%Y')}_{get_shop_name(import_log.user.id)}.csv"

    destination_dir = successful_imports_dir if import_log.failed_imports == 0 else failed_imports_dir
    destination_path = os.path.join(destination_dir, new_file_name)

    print(f"Saving to destination path: {destination_path}")

    with open(destination_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(content)

    if import_log.failed_imports == 0:
        notify_admin_about_import_success(
            import_log.user.id,
            new_file_name,
            import_log.total_products,
            import_log.successful_imports,
            import_log.failed_imports,
        )


def extract_data_from_row(row: List[str]) -> Optional[Tuple[str, str, str, str, dict, List[str], str, str]]:
    """
    Извлекает данные из строки CSV.

    Args:

        row (List[str]): Список значений строки CSV.

    Returns:
        Optional[Tuple[str, str, str, str, dict, List[str], str, str]]: Кортеж с данными (
        если строка не является заголовком) или None.
            Возвращаемый кортеж содержит следующие элементы:
            - name (str): Название продукта.
            - main_category_name (str): Название основной категории продукта.
            - subcategory_name (str): Название подкатегории продукта.
            - description (str): Описание продукта.
            - details (dict): Детали продукта в виде словаря.
            - tags (List[str]): Список тегов продукта.
            - price (str): Цена продукта.
            - remains (str): Остаток продукта.
    """

    if row[0].lower() == "name":
        return None

    name = row[0]
    main_category_name = row[1]
    subcategory_name = row[2]
    description = row[3]
    details_raw = {row[i]: row[i + 1] for i in range(4, len(row) - 4, 2) if row[i]}
    details = {key.strip(): value.strip() for key, value in details_raw.items()}
    tags = [tag.strip() for tag in row[-3].split(",")]
    price = row[-2]
    remains = row[-1]

    return name, main_category_name, subcategory_name, description, details, tags, price, remains
