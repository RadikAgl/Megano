""" Модуль с представлениями приложения cart """
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView

from cart.cart import CartInstance
from cart.forms import CartAddProductForm, CartAddProductModelForm
from cart.models import ProductInCart
from shops.models import Offer


class CartView(TemplateView):
    """Представление для отображения корзины"""

    template_name = "cart/cart.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartInstance(self.request)
        context["cart"] = cart
        if self.request.user.is_authenticated:
            context["forms"] = [CartAddProductModelForm(instance=item) for item in cart.qs]
        else:
            for item in cart:
                item["update_quantity_form"] = CartAddProductForm(
                    initial={"quantity": item["quantity"], "update": False}
                )
        return context


@require_POST
def cart_change_quantity(request, pk):
    cart = CartInstance(request)
    offer = get_object_or_404(Offer, id=pk)
    if request.user.is_authenticated:
        product_in_cart = get_object_or_404(ProductInCart, offer=offer)
        form = CartAddProductModelForm(request.POST, instance=product_in_cart)
        form.save()
    else:
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(offer=offer, quantity=cd["quantity"], update_quantity=cd["update"])
    return redirect("cart:cart")


@require_GET
def cart_add(request, pk):
    """Добавление товара в корзину из карточки товара"""
    cart = CartInstance(request)
    offer = get_object_or_404(Offer, id=pk)
    user = request.user
    if user.is_authenticated:
        try:
            product_in_cart = ProductInCart.objects.filter(cart=cart.cart).get(offer=offer)
            product_in_cart.quantity += 1
            product_in_cart.save()
        except ObjectDoesNotExist:
            ProductInCart.objects.create(cart=cart.cart, offer=offer, quantity=1)
    else:
        cart.add(offer, quantity=1, update_quantity=True)
    return redirect(request.META.get("HTTP_REFERER"))


@require_POST
def cart_remove(request, pk):
    cart = CartInstance(request)
    offer = get_object_or_404(Offer, id=pk)
    cart.remove(offer)
    return redirect("cart:cart")
