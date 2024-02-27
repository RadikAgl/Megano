"""Сервисы приложения cart"""

from decimal import Decimal
from django.conf import settings
from shops.models import Offer


class Cart:
    """Класс корзины покупок"""

    def __init__(self, request):
        """
        Инициализировать корзину.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, offer: Offer, quantity: int = 1, override_quantity: bool = False) -> None:
        """
        Добавить товар в корзину, либо обновить его количество.
        """
        offer_id = str(offer.id)
        if offer_id not in self.cart:
            self.cart[offer_id] = {"quantity": 0, "price": str(offer.price)}

        if override_quantity:
            self.cart[offer_id]["quantity"] = quantity
        else:
            self.cart[offer_id]["quantity"] += quantity
        self.save()

    def save(self):
        """Поднять флаг, чтобы сессия обновилась"""
        self.session.modified = True

    def remove(self, offer):
        """
        Удалить товар из корзины.
        """
        offer_id = str(offer.id)
        if offer_id in self.cart:
            del self.cart[offer_id]
            self.save()

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле и
        получить товары из базы данных.
        """
        offer_ids = self.cart.keys()
        offers = Offer.objects.filter(id__in=offer_ids)
        cart = self.cart.copy()
        for offer in offers:
            cart[str(offer.id)]["offer"] = offer
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            yield item

    def get_total_price(self):
        """Получение стоимости корзины"""
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())
