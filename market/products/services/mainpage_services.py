""" Сервисы главной страницы """

from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet, Avg
from django.db.models.functions import Round

from products import constants
from products.models import Product, Banner


class MainPageService:
    """Сервисы главной страницы"""

    def get_products(self) -> QuerySet:
        """Самые продаваемые продукты"""
        return (
            Product.objects.all()
            .prefetch_related("offer_set", "images")
            .annotate(avg_price=Round(Avg("offer__price"), constants.DECIMAL_PRECISION))
        )

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
