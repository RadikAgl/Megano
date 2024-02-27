""" Представления приложения products """

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView
from django.views.generic import TemplateView

from shops.models import Offer, Shop
from products.models import Product, ProductImage
from market.products.services.mainpage_services import MainPageService


class MainPageView(TemplateView):
    """Класс представление главной страницы"""

    template_name = "products/index.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_page_service = MainPageService()
        context["products"] = main_page_service.get_products()
        context["banners"] = main_page_service.banners_cache()
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
