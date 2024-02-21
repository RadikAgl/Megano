""" Маршруты приложения products """

from django.urls import path

from .views import MainPageView, DetailView

urlpatterns = [
    path("", MainPageView.as_view(), name="index"),
    path("<int:product_id>/", DetailView.as_view(), name="product-details"),
]
