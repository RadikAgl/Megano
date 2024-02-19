from django.urls import path

from .views import ProductDetailView

app_name = "products"
"""url пути"""
urlpatterns = [
    # path("", MainPageView.as_view(), name="index"),
    path("details/<int:product_id>/", ProductDetailView.as_view(), name="details"),
]
