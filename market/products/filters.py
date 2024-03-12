""" Модуль с фильтрами приложения products """

import django_filters
from django.db.models import QuerySet, Count
from django_filters import CharFilter
from django_filters.filters import ModelMultipleChoiceFilter, ModelChoiceFilter

from products.models import Tag, Category, Product
from shops.models import Offer


class CustomOrderingFilter(django_filters.OrderingFilter):
    """Для добавления сортировки по полю, отсутствующему в модели"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra["choices"] += [
            ("popularity", "Популярности"),
            ("-popularity", "Популярности (по убыванию)"),
            ("reviews", "Отзывам"),
            ("-reviews", "Отзывам (по убыванию)"),
        ]

    def filter(self, qs, value):
        if value and any(v in ["popularity", "-popularity"] for v in value):
            # сортировка по популярности
            return qs.order_by("name")

        if value and any(v in ["reviews", "-reviews"] for v in value):
            qs = qs.annotate(cnt=Count("reviews__id"))
            if "reviews" in value:
                return qs.order_by("-cnt")
            return qs.order_by("cnt")

        return super().filter(qs, value)


class ProductFilter(django_filters.FilterSet):
    """Фильтр для сортировки товаров в каталоге"""

    name = CharFilter(field_name="name", lookup_expr="icontains")

    price_range = CharFilter(
        method="filter_price_range",
        help_text="Фильтр по диапазону цен товаров",
    )
    category = ModelChoiceFilter(field_name="category__name", to_field_name="name", queryset=Category.objects.all())

    tag = ModelMultipleChoiceFilter(
        field_name="tags__name",
        to_field_name="name",
        queryset=Tag.objects.all(),
    )

    is_exist = CharFilter(method="filter_exist")
    free_delivery = CharFilter(method="filter_free_delivery")

    o = CustomOrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("avg_price", "avg_price"),
            ("created_at", "created_at"),
        ),
        field_labels={"avg_price": "Цене", "created_at": "Новизне"},
    )

    class Meta:
        model = Product
        fields = {"name": ["iexact", "icontains"]}

    def filter_price_range(self, queryset: QuerySet[Offer], _: str, value: str) -> QuerySet[Offer]:
        """Фильтрация по максимальной средней цене товара."""
        price_min, price_max = value.split(";")
        return queryset.filter(avg_price__gte=price_min).filter(avg_price__lte=price_max)

    def filter_exist(self, queryset, name, value):
        # construct the full lookup expression.
        if value:
            return queryset.filter(remains__gt=0)
        return queryset

    def filter_free_delivery(self, queryset, name, value):
        if value:
            return queryset  # Доделать
        return queryset
