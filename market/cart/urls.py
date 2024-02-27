""" Настройки URL приложения cart """

from django.urls import path

from cart.views import CartView, cart_add, cart_remove, change_quantity_in_cart

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/<int:pk>/", cart_add, name="cart_add"),
    path("remove/<int:pk>/", cart_remove, name="cart-remove"),
    path("change/<int:pk>/", change_quantity_in_cart, name="cart-change"),
    # path('add_from_product_card/<int:pk>/', cart_add_from_product_card, name='cart_add_from_product_card'),
    # path('remove/<int:pk>/', cart_remove, name='cart_remove'),
    # path('get_cart_data/', get_cart_data, name='get_cart_data'),
]
