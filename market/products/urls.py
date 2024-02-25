""" Маршруты приложения products """

from django.urls import path
from .views import MainPageView, ProductDetailView

urlpatterns = [
    path("", MainPageView.as_view(), name="index"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-details"),
]
