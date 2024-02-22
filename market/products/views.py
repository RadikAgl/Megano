""" Представления приложения products """
from typing import Optional

from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from market.products.services.mainpage_services import MainPageService
from shops.models import Offer, Shop
from .models import Product, ProductImage
from .services.product_services import (
    cache_product_details,
    fetch_product_details_from_database,
)


class MainPageView(TemplateView):
    """Класс представление главной страницы"""

    template_name = "products/index.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_page_service = MainPageService()
        context["products"] = main_page_service.get_products()
        return context


class DetailView(View):
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
        images = ProductImage.objects.filter(product=product)

        context = {
            "product": product,
            "offers": offers,
            "shops": shops,
            "images": images,
        }

        return render(request, self.template_name, context)
