import os
import traceback
from _csv import reader
from typing import List, Optional, Tuple

from django.core.cache import cache
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.db.models import Max
from django.utils import timezone
from filelock import FileLock

from accounts.models import User
from products.models import Category, Product, Tag
from settings_app.models import SiteSettings
from shops.models import Offer, Shop
from .models import ImportLog, ImportLogProduct

lock_key = "import_lock"
lock_path = "import_lock.lock"


def acquire_lock():
    """
    Получение файлового замка для предотвращения параллельного импорта.
    """
    lock = FileLock(lock_path)
    with lock:
        cache.set(lock_key, "locked")


def release_lock():
    """
    Освобождение файлового замка после завершения импорта.
    """
    lock = FileLock(lock_path)
    with lock:
        cache.delete(lock_key)


def create_or_update_category(name: str, parent_name: str = None, parent_id: int = None) -> Tuple[Category, bool]:
    """
    Создание или обновление категории.

    Args:
        name (str): Название категории.
        parent_name (str): Название родительской категории.
        parent_id (int): Идентификатор родительской категории.

    Returns:
        Tuple[Category, bool]: Кортеж, содержащий созданную или обновленную категорию и булевое значение,
                              указывающее, была ли она создана.
    """
    parent = None

    try:
        defaults = {}
        if parent_name or parent_id:
            parent_filter = {"name": parent_name} if parent_name else {"id": parent_id}
            parent, _ = Category.objects.get_or_create(**parent_filter)
            defaults["parent"] = parent

        if parent_id is not None and not isinstance(parent_id, int):
            parent_id = int(parent_id)

        max_sort_index = Category.objects.filter(parent=parent).aggregate(Max("sort_index"))["sort_index__max"] or 0

        category, created = Category.objects.get_or_create(
            name=name, defaults={"sort_index": max_sort_index + 1, **defaults}
        )

        if not created:
            for key, value in defaults.items():
                setattr(category, key, value)
            category.save()

        return category, created

    except IntegrityError as e:  # noqa
        return None, False


def get_next_sort_index(parent_id: int = None) -> int:
    """
    Получение следующего доступного индекса сортировки для категории.

    Args:
        parent_id (int): Идентификатор родительской категории.

    Returns:
        int: Следующий доступный индекс сортировки.
    """
    existing_sort_indexes = Category.objects.filter(parent_id=parent_id).values_list("sort_index", flat=True)

    sort_index = 1
    while sort_index in existing_sort_indexes:
        sort_index += 1

    return sort_index


def create_product(
    name: str,
    main_category_name: str,
    subcategory_name: str,
    description: str,
    details: dict,
    tags: List[str],
    import_log_instance: ImportLog,
) -> Product:
    """
    Создание продукта и связанного журнала импорта.

    Args:
        name (str): Название продукта.
        main_category_name (str): Название основной категории продукта.
        subcategory_name (str): Название подкатегории продукта.
        description (str): Описание продукта.
        details (dict): Детали продукта.
        tags (List[str]): Список тегов продукта.
        import_log_instance (ImportLog): Экземпляр журнала импорта.

    Returns:
        Product: Созданный продукт.
    """
    main_category, created_main = create_or_update_category(main_category_name)
    subcategory, created_sub = create_or_update_category(subcategory_name, parent_id=main_category.id)
    category = subcategory if subcategory else main_category

    product = Product.objects.create(name=name, category=category, description=description, details=details)
    product.tags.set(tags)

    import_log_product = ImportLogProduct.objects.create(import_log=import_log_instance, product=product)  # noqa
    import_log_instance.products.add(product)

    return product


def create_product_and_offer(product_data, import_log, user_id):
    """
    Создание продукта и связанного предложения.

    Args:
        product_data: Данные продукта.
        import_log: Экземпляр журнала импорта.
        user_id (int): Идентификатор пользователя.
    """
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
    tag_objects = [create_or_update_tag(tag) for tag in tags]
    category = create_or_update_category(main_category_name)[0]  # noqa

    existing_product = get_existing_product(name, main_category_name, subcategory_name)

    if existing_product:
        update_existing_product(existing_product, description, details, tag_objects)
        product = existing_product
    else:
        product = create_product(
            name, main_category_name, subcategory_name, description, details, tag_objects, import_log
        )

    import_log_product = ImportLogProduct.objects.create(import_log=import_log, product=product)  # noqa
    import_log.products.add(product)

    shop = get_user_shop(user_id)
    create_or_update_offer(shop, product, price, remains)


def get_existing_product(name: str, main_category_name: str, subcategory_name: str) -> Optional[Product]:
    """
    Получение существующего продукта.

    Args:
        name (str): Название продукта.
        main_category_name (str): Название основной категории продукта.
        subcategory_name (str): Название подкатегории продукта.

    Returns:
        Optional[Product]: Существующий продукт или None, если не найден.
    """
    try:
        main_category, _ = create_or_update_category(main_category_name)
        subcategory, _ = create_or_update_category(subcategory_name, parent_id=main_category.id)
        category = subcategory if subcategory else main_category

        existing_product = Product.objects.get(name=name, category=category)
        return existing_product
    except Product.DoesNotExist:
        return None


def update_existing_product(product: Product, description: str, details: dict, tags: List[Tag]):
    """
    Обновление существующего продукта.

    Args:
        product (Product): Экземпляр существующего продукта.
        description (str): Описание продукта.
        details (dict): Детали продукта.
        tags (List[Tag]): Список тегов продукта.
    """
    product.description = description
    product.details = details
    product.tags.set(tags)
    product.save()


def get_user_shop(user_id: int) -> Shop:
    """
    Получение магазина, связанного с пользователем.

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        Shop: Магазин, связанный с пользователем.
    """
    user = User.objects.get(id=user_id)
    return user.shop


def get_shop_name(user_id: int) -> str:
    """
    Получение названия магазина, связанного с пользователем.

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        str: Название магазина.
    """
    user = User.objects.get(id=user_id)
    shop = user.shop
    return shop.name


def create_or_update_offer(shop: Shop, product: Product, price: float, remains: int) -> bool:
    """
    Создание или обновление предложения.

    Args:
        shop (Shop): Экземпляр магазина.
        product (Product): Экземпляр продукта.
        price (float): Цена предложения.
        remains (int): Оставшееся количество.

    Returns:
        bool: True, если предложение было создано, False в противном случае.
    """
    offer, created = Offer.objects.get_or_create(
        shop=shop, product=product, defaults={"price": price, "remains": remains}
    )
    return created


def log_and_notify_error(
    error_message: str, user_id: int, file_name: str, total_products: int, successful_imports: int, failed_imports: int
) -> str:
    """
    Запись ошибки и уведомление об ошибке при импорте.

    Args:
        error_message (str): Сообщение об ошибке.
        user_id (int): Идентификатор пользователя.
        file_name (str): Название импортированного файла.
        total_products (int): Общее количество продуктов.
        successful_imports (int): Количество успешных импортов.
        failed_imports (int): Количество неудачных импортов.

    Returns:
        str: Сообщение об ошибке.
    """
    try:
        user = User.objects.get(id=user_id)
        site_settings = SiteSettings.load()
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
            site_settings.DEFAULT_FROM_EMAIL,
            [site_settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
    except Exception as e:
        return str(e)


def create_or_update_tag(name: str) -> Tag:
    """
    Создание или обновление тега.

    Args:
        name (str): Название тега.

    Returns:
        Tag: Созданный или обновленный тег.
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
    Создание журнала импорта.

    Args:
        file_name (str): Название импортированного файла.
        user (User): Экземпляр пользователя.
        status (str): Состояние импорта.
        total_products (int): Общее количество продуктов.
        successful_imports (int): Количество успешных импортов.
        failed_imports (int): Количество неудачных импортов.
        error_details (str): Детали ошибки, если они есть.

    Returns:
        ImportLog: Созданный журнал импорта.
    """
    import_log = ImportLog.objects.create(
        file_name=file_name,
        user=user,
        status=status,
        timestamp=timezone.now(),
    )
    import_log.total_products = total_products
    import_log.successful_imports = successful_imports
    import_log.failed_imports = failed_imports
    import_log.error_details = error_details
    import_log.save()

    return import_log


def notify_admin_about_import_success(
    user_id: int, file_name: str, total_products: int, successful_imports: int, failed_imports: int
) -> None:
    """
    Notify the admin about a successful import.

    Args:
        user_id (int): The user's ID.
        file_name (str): The name of the imported file.
        total_products (int): Total number of products imported.
        successful_imports (int): Number of successful imports.
        failed_imports (int): Number of failed imports.
    """
    try:
        user = User.objects.get(id=user_id)
        site_settings = SiteSettings.load()

        message = (
            f"Импорт файла {file_name} успешно завершен.\n"
            f"Загружено пользователем: {user.username} ({user.email}).\n"
            f"Всего товаров: {total_products}\n"
            f"Успешных импортов: {successful_imports}\n"
            f"Неудачных импортов: {failed_imports}"
        )

        email_host = site_settings.email_access_settings.get("EMAIL_HOST", "")

        print("Sending email...")
        print("Subject:", "Импорт успешно завершен")
        print("Message:", message)
        print("Email Host:", email_host)
        print("To:", site_settings.email_access_settings.get("EMAIL_HOST_USER"))
        print("Sender:", user.email)
        response = send_mail(
            "Импорт успешно завершен",
            message,
            user.email,
            [site_settings.email_access_settings.get("EMAIL_HOST_USER")],
            fail_silently=False,
        )

        # Print sending status and server response
        if response == 1:
            print("Email sent successfully.")
        else:
            print("Failed to send email.")

        print(f"Server response: {response}")
        print(f'EMAIL_HOST_USER: {site_settings.email_access_settings.get("EMAIL_HOST_USER", "")}')
    except Exception as e:  # noqa
        print("An error occurred while sending email:")
        print(traceback.format_exc())


@transaction.atomic
def process_import_common(uploaded_file, user_id: int) -> str:
    """
    Общий процесс импорта.

    Args:
        uploaded_file: Загруженный файл для импорта.
        user_id (int): Идентификатор пользователя.

    Returns:
        str: Сообщение об ошибке (пустая строка в случае успешного импорта).
    """
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
        import_log = get_existing_in_progress_import_log(user, file_name)

        if import_log is None:
            import_log = create_import_log(file_name, user, "in_progress")

        site_settings = SiteSettings.load()
        successful_imports_dir = os.path.join(site_settings.docs_dir, site_settings.successful_imports_dir)
        failed_imports_dir = os.path.join(site_settings.docs_dir, site_settings.failed_imports_dir)

        for row in csv_rows:
            try:
                product_data = extract_data_from_row(row)

                if product_data is None:
                    continue

                create_product_and_offer(product_data, import_log, user_id)
                total_products += 1
                successful_imports += 1

            except IndexError as index_error:
                handle_failed_import(
                    index_error, file_name, user_id, total_products, successful_imports, failed_imports
                )
                failed_imports += 1
                break

            except Exception as e:
                handle_failed_import(e, file_name, user_id, total_products, successful_imports, failed_imports)
                failed_imports += 1
                break
    except (IntegrityError, ImportError, Exception) as e:
        error_message = f"Error occurred: {str(e)}"

        handle_failed_import(e, file_name, user_id, total_products, successful_imports, failed_imports)
        return error_message
    finally:
        release_lock()
        handle_import_log_status(import_log, successful_imports, failed_imports)
        handle_destination_path(file_name, content, import_log, successful_imports_dir, failed_imports_dir)

    return ""


def get_existing_in_progress_import_log(user, file_name):
    """
    Получение существующего журнала импорта, находящегося в процессе выполнения.

    Args:
        user: Экземпляр пользователя.
        file_name (str): Название импортированного файла.

    Returns:
        ImportLog: Существующий журнал импорта в процессе выполнения (или None, если не найден).
    """
    return ImportLog.objects.filter(user=user, file_name=file_name, status="in_progress").first()


def handle_empty_file(file_name, user_id):
    """
    Обработка случая пустого файла.

    Args:
        file_name (str): Название импортированного файла.
        user_id (int): Идентификатор пользователя.

    Returns:
        str: Сообщение об ошибке.
    """
    error_message = "Uploaded file is empty"
    return log_and_notify_error(error_message, user_id, file_name, 0, 0, 1)


def handle_failed_import(error, file_name, user_id, total_products, successful_imports, failed_imports):
    """
    Обработка случая неудачного импорта.

    Args:
        error: Объект ошибки.
        file_name (str): Название импортированного файла.
        user_id (int): Идентификатор пользователя.
        total_products (int): Общее количество продуктов.
        successful_imports (int): Количество успешных импортов.
        failed_imports (int): Количество неудачных импортов.
    """
    log_and_notify_error(str(error), user_id, file_name, total_products, successful_imports, failed_imports)
    import_log = ImportLog.objects.filter(user_id=user_id, file_name=file_name).order_by("-id").first()  # noqa


@transaction.atomic
def handle_import_log_status(import_log, successful_imports, failed_imports):
    """
    Обработка статуса журнала импорта.

    Args:
        import_log: Экземпляр журнала импорта.
        successful_imports (int): Количество успешных импортов.
        failed_imports (int): Количество неудачных импортов.
    """
    if failed_imports > 0:
        import_log.status = "Завершён с ошибкой"
    else:
        import_log.status = "Выполнен"

    import_log.total_products = successful_imports + failed_imports
    import_log.successful_imports = successful_imports
    import_log.failed_imports = failed_imports
    import_log.save()


def handle_destination_path(file_name, content, import_log, successful_imports_dir, failed_imports_dir):
    """
    Обработка пути назначения для успешного и неудачного импорта.

    Args:
        file_name (str): Название импортированного файла.
        content (str): Содержимое файла.
        import_log: Экземпляр журнала импорта.
        successful_imports_dir (str): Директория для успешных импортов.
        failed_imports_dir (str): Директория для неудачных импортов.
    """
    os.makedirs(failed_imports_dir, exist_ok=True)

    new_file_name = f"{import_log.timestamp.strftime('%H-%M-%S_%d-%m-%Y')}_{get_shop_name(import_log.user.id)}.csv"

    destination_dir = successful_imports_dir if import_log.failed_imports == 0 else failed_imports_dir
    destination_path = os.path.join(destination_dir, new_file_name)

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
    Извлечение данных из строки CSV.

    Args:
        row (List[str]): Строка CSV.

    Returns:
        Optional[Tuple[str, str, str, str, dict, List[str], str, str]]: Кортеж данных продукта или None,
                                                                      если данные не могут быть извлечены.
    """
    try:
        name = row[0].strip()
        main_category_name = row[1].strip()
        subcategory_name = row[2].strip()
        description = row[3].strip()
        details = row[4].strip()
        tags = [tag.strip() for tag in row[5].split(",")] if row[5] else []
        price = row[6].strip()
        remains = row[7].strip()

        details_dict = {}

        if details:
            details_list = details.split(",")
            for detail in details_list:
                key, value = detail.split(":")
                details_dict[key.strip()] = value.strip()

        return name, main_category_name, subcategory_name, description, details_dict, tags, price, remains
    except IndexError:
        return None
