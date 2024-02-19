from typing import Optional

from django.core.cache import cache

from products.models import Product


def cache_product_details(product_id: int, expiration_time: int = 86400) -> None:  # 86400 one day
    """
    Кэшировать детали продукта и установить опциональное время истечения срока действия.

    Параметры:
    - product_id: Идентификатор продукта для кэширования
    - expiration_time: Время истечения срока действия в секундах (по умолчанию 24 часа)
    """
    cache_key = f"product_details_{product_id}"
    product = fetch_product_details_from_database(product_id)

    # Кэшировать детали продукта
    cache.set(cache_key, product, expiration_time)


def invalidate_product_details_cache(product_id: int) -> None:
    """
    Сбросить кэш для деталей продукта.

    Параметры:
    - product_id: Идентификатор продукта для сброса кэша
    """
    cache_key = f"product_details_{product_id}"
    cache.delete(cache_key)


def fetch_product_details_from_database(product_id: int) -> Optional[Product]:
    """
    Замените эту функцию фактической логикой получения деталей продукта из базы данных.

    Параметры:
    - product_id: Идентификатор продукта

    Возвращает:
    - Детали продукта из базы данных
    """
    try:
        product = Product.objects.get(id=product_id)
        return product
    except Product.DoesNotExist:
        return None
