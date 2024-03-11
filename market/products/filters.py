""" Модуль с фильтрами приложения products """

import django_filters
from django.db.models import QuerySet
from django_filters import CharFilter
from django_filters.filters import ModelMultipleChoiceFilter, ModelChoiceFilter

from products.models import Tag, Category
from shops.models import Offer


class CustomOrderingFilter(django_filters.OrderingFilter):
    """Для добавления сортировки по полю, отсутствующему в модели"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra["choices"] += [
            ("popularity", "Популярности"),
            ("-popularity", "Популярности (descending)"),
        ]

    def filter(self, qs, value):
        if value and any(v in ["popularity", "-popularity"] for v in value):
            # сортировка по популярности
            return qs.order_by("product__name")

        return super().filter(qs, value)


class ProductFilter(django_filters.FilterSet):
    """Фильтр для сортировки товаров в каталоге"""

    price_range = CharFilter(
        method="price_range_filter",
        help_text="Фильтр по диапазону цен товаров",
    )
    category = ModelChoiceFilter(
        field_name="product__category__name", to_field_name="name", queryset=Category.objects.all()
    )

    tag = ModelMultipleChoiceFilter(
        field_name="product__tags__name",
        to_field_name="name",
        queryset=Tag.objects.all(),
    )
    o = CustomOrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("price", "price"),
            ("product__reviews", "product__reviews"),
            ("product__created_at", "product__created_at"),
        ),
        field_labels={"price": "Цене", "product__reviews": "Отзывам", "product__created_at": "Новизне"},
    )

    class Meta:
        model = Offer
        fields = ("product__name",)

    def price_range_filter(self, queryset: QuerySet[Offer], _: str, value: str) -> QuerySet[Offer]:
        """Фильтрация по максимальной средней цене товара."""
        price_min, price_max = value.split(";")
        return queryset.filter(price__gte=price_min).filter(price__lte=price_max)
