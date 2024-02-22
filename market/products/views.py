""" Представления приложения products """

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView
from django.views.generic import TemplateView

from market.products.services.mainpage_services import MainPageService
from shops.models import Offer, Shop
from .models import Product, ProductImage

from .services.product_services import (
    invalidate_product_details_cache,
)


class MainPageView(TemplateView):
    """Класс представление главной страницы"""

    template_name = "products/index.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_page_service = MainPageService()
        context["products"] = main_page_service.get_products()
        return context


class ProductDetailView(DetailView):
    """
    Представление для детальной страницы продукта.

    Атрибуты:
    - template_name (str): Имя шаблона для отображения страницы продукта.
    - model: Класс модели для этого представления.
    - context_object_name: Имя переменной контекста для объекта модели.
    """

    template_name = "products/product.jinja2"
    model = Product
    context_object_name = "product"

    def get_object(self, queryset=None):
        product_id = self.kwargs.get("product_id")
        return Product.objects.get(id=product_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Fetch related data
        context["offers"] = Offer.objects.filter(product=product)
        context["shops"] = Shop.objects.filter(products=product)
        context["images"] = ProductImage.objects.filter(product=product)

        return context

    @method_decorator(cache_page(86400))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @receiver(post_save, sender=Product)
    def invalidate_product_cache(sender, instance, **kwargs):
        """
        Функция-получатель сигнала для сброса кэша при сохранении экземпляра Product.
        """
        product_id = instance.id
        invalidate_product_details_cache(product_id)
