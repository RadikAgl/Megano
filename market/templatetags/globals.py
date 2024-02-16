"""Модуль глобальных функций django_jinja"""

from django_jinja import library

from products.models import Category, Product


@library.global_function
def get_categories() -> dict:
    """Получение всех категорий"""
    all_categories = Category.objects.select_related("parent")

    children = {}

    for category in all_categories:
        children[category.id] = category.category_set.all()

    return {
        "main_categories": all_categories.filter(parent=None),
        "children": children,
    }


@library.global_function
def get_first_product_name() -> Product:
    """Получение названия первого товара из каталога"""

    return Product.objects.first()


@library.global_function
def get_cart_cost() -> float:
    """Получение стоимости товаров в корзине"""

    return 0.0
