""" Сервисы главной страницы """
import datetime
import random
from typing import Any

from django.core.cache import cache
from django.db.models import QuerySet, Count, Min, Sum, Avg

from products.models import Product, Banner, Category
from shops.models import Offer


def get_top_products() -> QuerySet:
    """Самые продаваемые продукты"""

    return Offer.objects.order_by("remains").select_related("product")[:8]


def get_top_categories() -> list[Any]:
    """Самые популярные категории"""

    categories = (
        Category.objects.all()
        .annotate(cnt=Count("category"))
        .annotate(min_price=Min("product__offer__price"))
        .annotate(remains=Sum("product__offer__remains"))
        .filter(cnt=0)
        .order_by("remains")
    )

    return [category for category in categories if category.is_active()][:3]


def get_hot_offers() -> QuerySet:
    """Горячие предложения"""

    products = (
        Product.objects.all()
        .annotate(cnt=Count("discount_products"))
        .annotate(avg_price=Avg("offer__price"))
        .filter(cnt__gt=0)
    )

    return random.sample(list(products), k=9)


def get_limited_products() -> QuerySet:
    """Ограниченные предложения"""

    return (
        Product.objects.annotate(avg_price=Avg("offer__price"))
        .filter(is_limited=True)
        .filter(is_product_of_the_day=False)
    )[:16]


def get_product_of_day() -> Product:
    """Товар дня"""

    return Product.objects.annotate(avg_price=Avg("offer__price")).filter(is_product_of_the_day=True).first()


def get_midnight_tomorrow() -> datetime:
    """Возвращает объект времени полночи следующего дня"""
    today = datetime.datetime.today()
    one_day = datetime.timedelta(days=1)
    tomorrow = today + one_day

    time_midnight = datetime.time(0)

    return datetime.datetime.combine(tomorrow, time_midnight)


def banners_cache() -> QuerySet:
    """
    Функция возвращает 3 случайных объекта модели Banner в кэшированном виде.
    """

    cache_key = "banners_cache"
    data = cache.get(cache_key)
    # banners_expiration_time = SiteSettings.load().banners_expiration_time
    banners_expiration_time = 100
    if not data:
        data = Banner.objects.filter(actual=True).order_by("?")[:3]
        cache.set(cache_key, data, banners_expiration_time)
    return data
