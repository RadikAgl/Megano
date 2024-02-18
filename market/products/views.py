""" Представления приложения products """
from django.views.generic import TemplateView

from products.services import MainPageService


class MainPageView(TemplateView):
    """Класс представление главной страницы"""

    template_name = "products/index.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_page_service = MainPageService()
        context["top_categories"] = main_page_service.get_top_categories()
        context["most_popular_products"] = main_page_service.get_most_popular_products()
        context["limited_products"] = main_page_service.get_limited_products()
        return context
