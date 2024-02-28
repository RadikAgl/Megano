from _csv import reader

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Max

from accounts.models import User
from products.models import Category, Product, Tag
from shops.models import Offer
from .models import ImportLog


def create_or_update_category(name, parent_name=None, parent_id=None):
    """
    Создает или обновляет категорию.

    Параметры:
    - name: имя категории
    - parent_name: имя родительской категории
    - parent_id: идентификатор родительской категории

    Возвращает созданную или обновленную категорию и флаг, указывающий, была ли создана новая категория.
    """
    sort_index = get_next_sort_index(parent_id)

    while True:
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
        except IntegrityError:
            sort_index += 1


def get_next_sort_index(parent_id=None):
    """
    Получает следующий индекс сортировки для категории.

    Параметры:
    - parent_id: идентификатор родительской категории

    Возвращает следующий индекс сортировки для категории.
    """
    max_sort_index = Category.objects.filter(parent__id=parent_id).aggregate(max_index=Max("sort_index"))["max_index"]
    return max_sort_index + 1 if max_sort_index is not None else 0


def create_product(name, main_category_name, subcategory_name, description, details, tags, import_log_instance):
    """
    Создает продукт.

    Параметры:
    - name: имя продукта
    - main_category_name: имя основной категории
    - subcategory_name: имя подкатегории
    - description: описание продукта
    - details: детали продукта
    - tags: теги продукта
    - import_log_instance: экземпляр ImportLog

    Возвращает созданный продукт.
    """
    main_category, created_main = create_or_update_category(main_category_name, parent_id=None)
    subcategory, created_sub = create_or_update_category(subcategory_name, parent_id=main_category.id)
    category = subcategory if subcategory else main_category

    product = Product.objects.create(
        name=name, category=category, description=description, details=details, import_log=import_log_instance
    )
    product.tags.set(tags)
    return product


def get_user_shop(user_id):
    """
    Получает магазин пользователя.

    Параметры:
    - user_id: идентификатор пользователя

    Возвращает магазин пользователя.
    """
    user = User.objects.get(id=user_id)
    return user.shop


def create_or_update_offer(shop, product, price, remains):
    """
    Создает или обновляет предложение.

    Параметры:
    - shop: магазин
    - product: продукт
    - price: цена предложения
    - remains: остаток предложения
    """
    offer, created = Offer.objects.get_or_create(
        shop=shop, product=product, defaults={"price": price, "remains": remains}
    )


def log_and_notify_error(error_message, user_id, file_name, total_products, successful_imports, failed_imports):
    """
    Логгирует ошибку и отправляет уведомление об ошибке.

    Параметры:
    - error_message: сообщение об ошибке
    - user_id: идентификатор пользователя
    - file_name: имя файла
    - total_products: общее количество продуктов
    - successful_imports: количество успешных импортов
    - failed_imports: количество неудачных импортов
    """
    try:
        import_log = ImportLog.objects.create(file_name=file_name, status="Завершён с ошибкой")
        import_log.error_details = error_message
        import_log.save()

        user = User.objects.get(id=user_id)

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
        print(f"Ошибка при записи лога и уведомлении: {str(e)}")


def log_successful_import(file_name):
    """
    Логгирует успешный импорт.

    Параметры:
    - file_name: имя файла импорта
    """
    ImportLog.objects.create(file_name=file_name, status="Выполнен")


def create_or_update_tag(name):
    """
    Создает или обновляет тег.

    Параметры:
    - name: имя тега

    Возвращает созданный или обновленный тег.
    """
    tag, created = Tag.objects.get_or_create(name=name)
    return tag


def notify_admin_about_import_success(user_id, file_name, total_products, successful_imports, failed_imports):
    """
    Уведомляет администратора о успешном импорте.

    Параметры:
    - user_id: идентификатор пользователя
    - file_name: имя файла импорта
    - total_products: общее количество продуктов
    - successful_imports: количество успешных импортов
    - failed_imports: количество неудачных импортов
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


def process_import_common(uploaded_file, user_id, import_log_instance):
    """
    Общий процесс импорта.

    Параметры:
    - uploaded_file: загруженный файл
    - user: пользователь
    - import_log_instance: экземпляр ImportLog
    """
    try:
        file_name = uploaded_file.name
        content = uploaded_file.read().decode("utf-8")

        lines = content.split("\n")
        csv_rows = reader(lines)
        total_products = 0
        successful_imports = 0
        failed_imports = 0

        import_log_instance.status = "В процессе выполнения"
        import_log_instance.save()

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
                ) = extract_data_from_row(row)
                main_category, _ = create_or_update_category(main_category_name)
                create_or_update_category(subcategory_name, parent_name=main_category_name)
                tag_objects = [create_or_update_tag(tag) for tag in tags]

                product = create_product(
                    name, main_category_name, subcategory_name, description, details, tag_objects, import_log_instance
                )

                shop = get_user_shop(user_id)
                create_or_update_offer(shop, product, price, remains)

                total_products += 1
                successful_imports += 1

            except Exception as e:
                log_and_notify_error(str(e), user_id, file_name, total_products, successful_imports, failed_imports)
                failed_imports += 1

        import_log_instance.status = "Выполнен"
        import_log_instance.file_name = file_name
        import_log_instance.total_products = total_products
        import_log_instance.successful_imports = successful_imports
        import_log_instance.failed_imports = failed_imports
        import_log_instance.save()

        notify_admin_about_import_success(user_id, file_name, total_products, successful_imports, failed_imports)

    except IntegrityError as e:
        log_and_notify_error(
            f"Ошибка целостности данных при импорте: {str(e)}",
            user_id,
            file_name,
            total_products,
            successful_imports,
            failed_imports,
        )

    except Exception as e:
        log_and_notify_error(
            f"Неожиданная ошибка во время импорта: {str(e)}",
            user_id,
            file_name,
            total_products,
            successful_imports,
            failed_imports,
        )


def extract_data_from_row(row):
    """
    Извлекает данные из строки CSV.

    Параметры:
    - row: строка CSV
    - my_import_log_instance: экземпляр ImportLog

    Возвращает кортеж с данными о продукте.
    """
    # Check if the row is the header
    if row[0].lower() == "name":
        # Skip processing the header row
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
