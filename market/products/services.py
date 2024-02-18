from products.models import Category


class MainPageService:
    """Сервисы главной страницы"""

    def __init__(self):
        self.products = Category.objects.prefetch_related("")


def _get_main_page_context() -> MainPageService:
    """Возвращает экземпляр класса MainPageService с контекстом для главной страницы сайта"""

    return MainPageService()
