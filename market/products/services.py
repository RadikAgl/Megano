from django.db.models import QuerySet

from products.models import Product


class MainPageService:
    """Сервисы главной страницы"""

    def get_products(self) -> QuerySet:
        """Самые продаваемые продукты"""
        return Product.objects.all().prefetch_related("images")
