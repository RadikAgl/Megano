""" Сервисы страницы каталога товаров """

from django.db.models import Count
from django.http import HttpRequest

from products.filters import ProductFilter
from products.models import Tag


def get_ordering_fields(filter_class: ProductFilter) -> list:
    """Возвращает параметры сортировки и их название для отображения на странице"""

    return [item for item in list(filter_class.filters["o"].field.choices)[1:] if not item[0].startswith("-")]


def get_popular_tags() -> list:
    """Возвращает популярные теги"""

    return Tag.objects.all().annotate(cnt=Count("product")).order_by("-cnt")[:5]


def relative_url(request: HttpRequest):
    """Создание url для отображения страниц пагинации с фильтрацией"""
    url = request.get_full_path()
    if "?" not in url:
        return url, False
    if "page" not in url:
        return url, True
    params = url.split("?")[1].split("&")
    url_params = "?"
    for param in params:
        if not param.startswith("page"):
            url_params += param
    return url.split("?")[0] + url_params, True
