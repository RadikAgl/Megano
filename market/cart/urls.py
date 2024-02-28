""" Настройки URL приложения cart """

from django.urls import path

from cart.views import CartView, cart_add, cart_remove, cart_change_quantity

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/<int:pk>/", cart_add, name="cart-add"),
    path("change/<int:pk>/", cart_change_quantity, name="cart-change-quantity"),
    path("remove/<int:pk>/", cart_remove, name="cart-remove"),
]
