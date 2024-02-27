""" Модуль с представлениями приложения cart """

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from cart.cart import Cart
from cart.forms import CartAddProductForm
from shops.models import Offer


class CartView(TemplateView):
    """Представление для отображения корзины"""

    template_name = "cart/cart.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context["cart"] = cart
        for item in cart:
            item["update_quantity_form"] = CartAddProductForm(initial={"quantity": item["quantity"], "update": False})
        return context


def change_quantity_in_cart(request, pk: int) -> HttpResponseRedirect:
    """Изменение количества товаров в корзине"""
    cart = Cart(request)
    offer = get_object_or_404(Offer, id=pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(offer=offer, quantity=cd["quantity"], override_quantity=True)

    return redirect("cart:cart")


def cart_add(request, pk: int) -> HttpResponseRedirect:
    """Добавление товара в корзину"""
    cart = Cart(request)
    offer = get_object_or_404(Offer, id=pk)
    cart.add(offer=offer)

    return redirect(request.META.get("HTTP_REFERER"))


def cart_remove(request, pk: int) -> HttpResponseRedirect:
    """Удаление товара из корзины"""
    cart = Cart(request)
    offer = get_object_or_404(Offer, id=pk)
    cart.remove(offer)
    return redirect("cart:cart")
