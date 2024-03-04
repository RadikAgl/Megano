from _csv import reader

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.utils import timezone

from accounts.models import User
from products.models import Category, Product, Tag
from shops.models import Offer
from .models import ImportLog, ImportLogProduct


def create_or_update_category(name, parent_name=None, parent_id=None):
    """
    Создает или обновляет категорию.

    Args:
        name (str): Название категории.
        parent_name (str, optional): Название родительской категории. По умолчанию None.
        parent_id (int, optional): ID родительской категории. По умолчанию None.

    Returns:
        tuple: Кортеж с объектом категории и флагом, указывающим на создание (True) или обновление (False).
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


def get_next_sort_index(parent_id=None):
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


def create_product(name, main_category_name, subcategory_name, description, details, tags, import_log_instance):
    """
    Создает продукт и связанный лог импорта.

    Args:
        name (str): Название продукта.
        main_category_name (str): Название основной категории продукта.
        subcategory_name (str): Название подкатегории продукта.
        description (str): Описание продукта.
        details (dict): Детали продукта.
        tags (list): Список тегов продукта.
        import_log_instance (ImportLog): Экземпляр лога импорта.

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


def get_user_shop(user_id):
    """
    Возвращает магазин пользователя.

    Args:
        user_id (int): ID пользователя.

    Returns:
        Shop: Магазин пользователя.
    """
    user = User.objects.get(id=user_id)
    return user.shop


def create_or_update_offer(shop, product, price, remains):
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


def log_and_notify_error(error_message, user_id, file_name, total_products, successful_imports, failed_imports):
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


def log_successful_import(file_name):
    """
    Логгирует успешный импорт.

    Args:
        file_name (str): Имя файла импорта.
    """
    ImportLog.objects.create(file_name=file_name, status="Выполнен")


def create_or_update_tag(name):
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
    file_name, user, status, total_products=0, successful_imports=0, failed_imports=0, error_details=None
):
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
    return import_log


def notify_admin_about_import_success(user_id, file_name, total_products, successful_imports, failed_imports):
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


def process_import_common(uploaded_file, user_id):
    """
    Общий процесс импорта.

    Args:
        uploaded_file (File): Загруженный файл для импорта.
        user_id (int): ID пользователя, выполнившего импорт.

    Returns:
        None: Функция не возвращает значений.
    """
    try:
        file_name = uploaded_file.name
        content = uploaded_file.read().decode("utf-8")
        lines = content.split("\n")
        csv_rows = reader(lines)
        total_products = 0
        successful_imports = 0
        failed_imports = 0
        user = User.objects.get(id=user_id)

        import_log = ImportLog.objects.create(file_name=file_name, user=user, status="В процессе выполнения")

        for row in csv_rows:
            product_data = extract_data_from_row(row)
            if product_data is None:
                continue
            try:
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

                product = create_product(
                    name, main_category_name, subcategory_name, description, details, tag_objects, import_log
                )
                import_log_product = ImportLogProduct.objects.create(import_log=import_log, product=product)  # noqa
                import_log.products.add(product)

                shop = get_user_shop(user_id)
                create_or_update_offer(shop, product, price, remains)

                total_products += 1
                successful_imports += 1

            except Exception as e:
                error_details = log_and_notify_error(  # noqa
                    str(e), user_id, file_name, total_products, successful_imports, failed_imports
                )
                failed_imports += 1

        import_log.status = "Выполнен"
        import_log.total_products = total_products
        import_log.successful_imports = successful_imports
        import_log.failed_imports = failed_imports
        import_log.save()

        if failed_imports == 0:
            notify_admin_about_import_success(user_id, file_name, total_products, successful_imports, failed_imports)

    except IntegrityError as e:
        return str(e)

    except Exception as e:
        return str(e)


def extract_data_from_row(row):
    """
    Извлекает данные из строки CSV.

    Args:
        row (list): Список значений строки CSV.

    Returns:
        tuple or None: Кортеж с данными (если строка не является заголовком) или None.
            Возвращаемый кортеж содержит следующие элементы:
            - name (str): Название продукта.
            - main_category_name (str): Название основной категории продукта.
            - subcategory_name (str): Название подкатегории продукта.
            - description (str): Описание продукта.
            - details (dict): Детали продукта в виде словаря.
            - tags (list): Список тегов продукта.
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
