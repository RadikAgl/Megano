""" Представления приложения products """
from django.views.generic import TemplateView
from products.services import MainPageService
from products.services.review_services import ReviewsService
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from .forms import ReviewsForm


class MainPageView(TemplateView):
    """Класс представление главной страницы"""

    template_name = "products/index.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_page_service = MainPageService()
        context["products"] = main_page_service.get_products()
        return context


def add_review(request: WSGIRequest):
    """
    Добавляет отзыв о товаре
    :param request: пост запрос
    :return: обновляет страницу
    """
    if request.method == "POST":
        form = ReviewsForm(request.POST)
        if form.is_valid():
            review = ReviewsService(request, request.user, request.POST["product"])
            text = form.cleaned_data["text"]
            review.add(review=text)
    return redirect(request.META.get("HTTP_REFERER"))
