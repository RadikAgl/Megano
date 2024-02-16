""" Представления приложения products """
from django.views.generic import TemplateView

from products.services import _get_main_page_context

# Create your views here.


class MainPageView(TemplateView):
    """Класс представление главной страницы"""

    template_name = "products/index.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context["products"] = _get_main_page_context()
        return context
