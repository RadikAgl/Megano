from typing import Optional

from django.shortcuts import render
from django.views import View

from shops.models import Offer, Shop
from .models import Product
from .services.product_services import (
    cache_product_details,
    fetch_product_details_from_database,
    invalidate_product_details_cache,
)


class ProductDetailView(View):
    """
    Представление для детальной страницы продукта.

    Атрибуты:
    - template_name (str): Имя шаблона для отображения страницы продукта.
    """

    template_name: str = "products/product.jinja2"

    def get(self, request, *args, **kwargs) -> render:
        """
        Обработчик GET-запроса для отображения детальной страницы продукта.

        Параметры:
        - request: Запрос Django.
        - *args: Дополнительные аргументы.
        - **kwargs: Дополнительные именованные аргументы.

        Возвращает:
        - Ответ Django с отображением детальной страницы продукта.
        """

        product_id: int = kwargs.get("product_id")

        product: Optional[Product] = fetch_product_details_from_database(product_id)

        if not product:
            product = fetch_product_details_from_database(product_id)
            cache_product_details(product_id, expiration_time=86400)

        offers = Offer.objects.filter(product=product)
        shops = Shop.objects.filter(products=product)

        context = {
            "product": product,
            "offers": offers,
            "shops": shops,
        }

        return render(request, self.template_name, context)

    @staticmethod
    def invalidate_cache(product_id: int) -> None:
        """
        Сбросить кэш при обновлении продукта.

        Параметры:
        - product_id: Идентификатор продукта.
        """
        invalidate_product_details_cache(product_id)
