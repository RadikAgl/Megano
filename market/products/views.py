""" Представления приложения products """
from django.views.generic import TemplateView

from products.services import MainPageService


class MainPageView(TemplateView):
    """Класс представление главной страницы"""

    template_name = "products/index.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_page_service = MainPageService()
        context["products"] = main_page_service.get_products()
        return context
