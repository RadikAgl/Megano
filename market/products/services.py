from django.db.models import QuerySet

from products.models import Category, Product


class MainPageService:
    """Сервисы главной страницы"""

    def get_top_categories(self) -> QuerySet:
        """Выбор топовых категорий по продажам"""

        return Category.objects.all()

    def get_most_popular_products(self) -> QuerySet:
        """Самые продаваемые продукты"""
        return Product.objects.all().prefetch_related("images")[:3]

    def get_limited_products(self) -> QuerySet:
        """Товары ограниченной серии"""
        return Product.objects.all().prefetch_related("images")[3:6]


def get_min_price_in_category(category: Category) -> float:
    """Получение минимальной цены товаров в категории"""
    return min(Product.objects.filter(category=category).values_list("offer_set__price", flat=True))
