""" Модуль с фильтрами приложения products """

import django_filters
from django.db.models import QuerySet, Count
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
            ("reviews", "Отзывам"),
            ("-reviews", "Отзывам (descending)"),
        ]

    def filter(self, qs, value):
        if value and any(v in ["popularity", "-popularity"] for v in value):
            # сортировка по популярности
            return qs.order_by("product__name")

        if value and any(v in ["reviews", "-reviews"] for v in value):
            qs = qs.annotate(cnt=Count("product__reviews__id"))
            if "reviews" in value:
                return qs.order_by("-cnt")
            return qs.order_by("cnt")

        return super().filter(qs, value)


class ProductFilter(django_filters.FilterSet):
    """Фильтр для сортировки товаров в каталоге"""

    name = CharFilter(field_name="product__name", lookup_expr="icontains")

    price_range = CharFilter(
        method="filter_price_range",
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

    is_exist = CharFilter(method="filter_exist")
    free_delivery = CharFilter(method="filter_free_delivery")

    o = CustomOrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("price", "price"),
            ("product__created_at", "product__created_at"),
        ),
        field_labels={"price": "Цене", "product__reviews": "Отзывам", "product__created_at": "Новизне"},
    )

    class Meta:
        model = Offer
        fields = {"product__name": ["iexact", "icontains"]}

    def filter_price_range(self, queryset: QuerySet[Offer], _: str, value: str) -> QuerySet[Offer]:
        """Фильтрация по максимальной средней цене товара."""
        price_min, price_max = value.split(";")
        return queryset.filter(price__gte=price_min).filter(price__lte=price_max)

    def filter_exist(self, queryset, name, value):
        # construct the full lookup expression.
        if value:
            return queryset.filter(remains__gt=0)
        return queryset

    def filter_free_delivery(self, queryset, name, value):
        if value:
            return queryset  # Доделать
        return queryset
