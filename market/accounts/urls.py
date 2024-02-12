from django.urls import path

from .views import register, login_view, PasswordReset, UpdatePasswordView, main_page
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetCompleteView,
)


app_name = "accounts"
"""url пути"""
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("reset_password/", PasswordReset.as_view(), name="password_reset"),
    path("reset_password/done/", PasswordResetDoneView.as_view(), name="reset_password_done"),
    path("reset/<uidb64>/<token>/", UpdatePasswordView.as_view(), name="reset_password_confirm"),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("main_page/", main_page, name="main_page"),
]
