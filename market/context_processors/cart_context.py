"""Модуль с глобльным контекстом сайта"""

from cart.cart import Cart


def get_cart_cost(request):
    """Стоимость корзины"""
    cart = Cart(request)
    return {"cart_cost": cart.get_total_price()}
