""" Маршруты приложения comparison """

from django.urls import path

from comparison.views import ComparisonView, add_to_comparison

urlpatterns = [
    path("", ComparisonView.as_view(), name="comparison"),
    path("add_to_comparison/<int:product_id>/", add_to_comparison, name="add_to_comparison"),
]
