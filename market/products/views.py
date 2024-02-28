""" Представления приложения products """

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, TemplateView

from products.services.mainpage_services import MainPageService
from products.services.review_services import ReviewService
from shops.models import Offer, Shop
from .forms import ReviewsForm
from .models import Product, ProductImage


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
        review_service = ReviewService(self.request, self.request.user, self.get_object())
        product = self.object

        # Fetch related data
        context["offers"] = Offer.objects.filter(product=product)
        context["shops"] = Shop.objects.filter(products=product)
        context["images"] = ProductImage.objects.filter(product=product)
        context["reviews"] = review_service.get_reviews_for_product()
        context["paginator"], context["page_obj"] = review_service.paginate(context["reviews"])
        context["review_form"] = ReviewsForm()
        return context

    @method_decorator(cache_page(86400))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def add_review(request: WSGIRequest):
    """
    Добавляет отзыв о товаре
    :param request: пост запрос
    :return: обновляет страницу
    """
    if request.method == "POST":
        form = ReviewsForm(request.POST)
        if form.is_valid():
            review = ReviewService(request, request.user, request.POST["product"])
            text = form.cleaned_data["text"]
            review.add(review=text)
    return redirect(request.META.get("HTTP_REFERER"))
