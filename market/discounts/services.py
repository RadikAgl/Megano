"""Сервисы приложения discounts"""

from typing import Tuple
from _decimal import Decimal

from django.utils import timezone

from .models import DiscountCart, DiscountProduct, DiscountSet
from shops.models import Offer


def calculate_set(offers: list[Offer]) -> Tuple[Decimal | int, int]:
    """Возвращает вес скидки и скидку на набор товаров"""

    discounts = DiscountSet.objects.filter(
        start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date(), is_active=True
    ).order_by("-weight")

    weight = 0
    percentage = 0

    for discount in discounts:
        for offer in offers:
            if offer.product.id in discount.first_group.all():
                for offer_ in offers:
                    if offer_.product.id in discount.second_group.all() and offer_.product != offer.product:
                        return discount.weight, discount.percentage

    return weight, percentage


def calculate_cart(price: Decimal) -> Tuple[Decimal | int, int]:
    """Возвращает вес скидки и скидку на корзину"""

    discount_carts = DiscountCart.objects.filter(
        start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date(), is_active=True
    ).order_by("-weight")

    weight = 0
    percentage = 0

    for discount in discount_carts:
        if discount.price_from <= price <= discount.price_to:
            weight = discount.weight
            percentage = discount.percentage
    return weight, percentage


def calculate_product_price_with_discount(offer: Offer) -> Decimal:
    """Возвращает стоимость товара в корзине с учетом скидки"""

    discount_products = DiscountProduct.objects.filter(
        start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date(), is_active=True
    ).order_by("-weight")

    price = offer.price

    for discount in discount_products:
        if offer.product in discount.products.all():
            return Decimal(price - price * discount.percentage / 100)
    return price


def calculate_products_discount_total_price(
    offers: list[tuple[Offer, int]],
) -> Decimal | int:
    """Возвращает стоимость корзины с учетом скидок на товары"""
    total_price = 0
    for offer in offers:
        total_price += calculate_product_price_with_discount(offer[0]) * offer[1]
    return total_price
