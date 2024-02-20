""" Маршруты приложения products """

from django.urls import path
from products import views

urlpatterns = [
    path("", views.MainPageView.as_view(), name="index"),
]
