"""Сервисы главной страницы"""

from django.db.models import QuerySet
from django.core.cache import cache
from django.conf import settings

from products.models import Banner
from shops.models import Offer


class MainPageService:
    """Сервисы главной страницы"""

    def get_products(self) -> QuerySet:
        """Самые продаваемые продукты"""
        return Offer.objects.all().select_related("product").prefetch_related("product__images")

    def banners_cache(self) -> QuerySet:
        """
        Функция возвращает 3 случайных объекта модели Banner в кэшированном виде.
        """

        cache_key = "banners_cache"
        data = cache.get(cache_key)
        if not data:
            data = Banner.objects.filter(actual=True).order_by("?")[:3]
            cache.set(cache_key, data, settings.BANNERS_EXPIRATION_TIME)
        return data
