"""Сервисы приложения cart"""

from decimal import Decimal
import random

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, F

from accounts.models import User
from cart.models import ProductInCart, Cart
from shops.models import Offer


class CartInstance:
    """Класс корзины покупок"""

    def __init__(self, request):
        self.use_db = False
        self.cart = None
        self.user = request.user
        self.session = request.session
        self.qs = None
        cart = self.session.get(settings.CART_SESSION_ID)
        if self.user.is_authenticated:
            self.use_db = True
            if cart:
                self.save_in_db(cart, request.user)
                self.clear(True)
            try:
                cart = Cart.objects.get(user=self.user, is_active=True)
            except ObjectDoesNotExist:
                cart = Cart.objects.create(user=self.user)
            self.qs = ProductInCart.objects.filter(cart=cart)
        else:
            # сохранить пустую корзину в сеансе
            if not cart:
                cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save_in_db(self, cart: dict, user: User) -> None:
        """
        Перенос корзины из сессии в БД
        :param cart: корзина из сессии
        :param user: пользователь
        :return: None
        """
        try:
            cart_ = Cart.objects.get(user=user, is_active=True)
            cart_exists = True
        except ObjectDoesNotExist:
            cart_exists = False

        for key, value in cart.items():
            if cart_exists:
                try:
                    product = ProductInCart.objects.filter(cart=cart_).get(offer=key)
                    product.quantity += cart[key]["quantity"]
                    product.save()
                except ObjectDoesNotExist:
                    ProductInCart.objects.create(
                        offer=Offer.objects.get(pk=key),
                        cart=Cart.objects.filter(user=user, is_active=True).first(),
                        quantity=cart[key]["quantity"],
                    )
            else:
                offer = Offer.objects.get(id=key)
                cart_ = Cart.objects.update_or_create(user=user)
                ProductInCart.objects.create(
                    offer=offer,
                    cart=cart_,
                    quantity=value["quantity"],
                )

    def add(self, offer: Offer, quantity: int = 1, update_quantity: bool = False) -> None:
        """
        Добавляет товар в корзину и обновляет его количество
        :param offer: предложение товара
        :param quantity: количество
        :param update_quantity: флаг, указывающий, нужно ли обновить товар (True) либо добавить его (False)
        :return: None
        """
        if self.use_db:
            if self.qs.filter(offer=offer).exists():
                product_in_cart = self.qs.select_for_update().get(offer=offer)
            else:
                product_in_cart = ProductInCart(offer=offer, cart=self.cart, quantity=0)
            print("cart_add", product_in_cart)
            if update_quantity:
                product_in_cart.quantity += quantity
            else:
                product_in_cart.quantity = quantity
            product_in_cart.save()
        else:
            offer_id = str(offer.id)
            if offer_id not in self.cart:
                self.cart[offer_id] = {"quantity": 0, "price": str(offer.price)}
            if update_quantity:
                self.cart[offer_id]["quantity"] += quantity
            else:
                self.cart[offer_id]["quantity"] = quantity
            self.save()

    def save(self) -> None:
        """
        Сохранение корзины в сессии
        :return: None
        """
        if not self.use_db:
            self.session[settings.CART_SESSION_ID] = self.cart
            self.session.modified = True

    def remove(self, offer: Offer) -> None:
        """
        Удаление товара из корзины
        :param offer: товар
        :return: None
        """
        if self.use_db:
            offer_ = self.qs.filter(offer=offer)
            if offer_.exists():
                offer_.delete()
        else:
            offer_id = str(offer.id)
            if offer_id in self.cart:
                del self.cart[offer_id]
                self.save()

    def __iter__(self):
        """
        Перебор товаров из корзины
        """

        offer_ids = self.cart.keys()
        # получить объекты продукта и добавить их в корзину
        offers = Offer.objects.filter(id__in=offer_ids)
        for offer in offers:
            self.cart[str(offer.id)]["offer"] = offer

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            yield item

    def __len__(self) -> int:
        """
        Считает количество товаров в корзине
        :return: количество товаров в корзине
        """
        if self.use_db:
            result = ProductInCart.objects.filter(cart=self.cart).aggregate(Sum("quantity"))["quantity__sum"]
            return result if result else 0
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self) -> Decimal | int:
        """
        Считает итоговую цену товаров корзины
        :return: цена товаров в корзине
        """
        if self.use_db:
            total = self.qs.only("quantity").aggregate(total=Sum(F("quantity") * F("offer__price")))["total"]
            if not total:
                total = Decimal("0")
            return total.quantize(Decimal("1.00"))

        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self, only_session: bool = False) -> None:
        """
        Удалить корзину из сеанса или из базы данных, если пользователь авторизован
        :return:
        """
        if only_session:
            del self.session[settings.CART_SESSION_ID]
            self.session.modified = True
        else:
            if self.qs:
                self.qs.delete()

    def get_offer(self, product):
        """Подбор предложения для товара"""
        if self.use_db:
            products_in_cart = self.qs.filter(offer__product=product)
            if products_in_cart:
                return products_in_cart[0].offer

        else:
            offers = Offer.objects.filter(product=product)
            for offer in offers:
                if str(offer.id) in self.cart:
                    return offer

        return random.choice(Offer.objects.filter(product=product))
