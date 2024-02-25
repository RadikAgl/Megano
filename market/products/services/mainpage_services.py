from django.db.models import QuerySet
from django.core.cache import cache
from products.models import Product, Banner


class MainPageService:
    """Сервисы главной страницы"""

    def get_products(self) -> QuerySet:
        """Самые продаваемые продукты"""
        return Product.objects.all().prefetch_related("images")

    def banners_cache(self, expiration_time: int = 600) -> QuerySet:
        """
        Функция возвращает 3 случайных объекта модели Banner в кэшированном виде.

        :param expiration_time: Время кэширования данных (10 минут)
        """

        cache_key = "banners_cache"
        data = cache.get(cache_key)
        if not data:
            data = Banner.objects.all().filter(actual=True).order_by("?")[:3]
            cache.set(cache_key, data, expiration_time)
        return data
