""" Сервисы страницы каталога товаров """
from django.db.models import Count

from products.filters import ProductFilter
from products.models import Tag


def get_ordering_fields(filter_class: ProductFilter) -> list:
    """Возвращает параметры сортировки и их название для отображения на странице"""

    return [item for item in filter_class.filters["o"].field.choices[1:] if not item[0].startswith("-")]


def get_popular_tags() -> list:
    """Возвращает популярные теги"""

    return Tag.objects.all().annotate(cnt=Count("product")).order_by("-cnt")[:5]
