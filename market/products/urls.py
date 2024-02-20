from django.urls import path

from .views import DetailView

app_name = "products"
"""url пути"""
urlpatterns = [
    # path("", MainPageView.as_view(), name="index"),
    path("<int:product_id>/", DetailView.as_view(), name="product-details"),
]
