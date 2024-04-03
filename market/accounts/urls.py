"""url пути"""
from django.urls import path
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from .views import (
    RegistrationView,
    MyLoginView,
    PasswordReset,
    UpdatePasswordView,
    AcountView,
    ProfileView,
    UserHistoryView,
)

app_name = "accounts"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("reset_password/", PasswordReset.as_view(), name="password_reset"),
    path("reset_password/done/", PasswordResetDoneView.as_view(), name="reset_password_done"),
    path("reset/<uidb64>/<token>/", UpdatePasswordView.as_view(), name="reset_password_confirm"),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("main_page/", AcountView.as_view(), name="main"),
    path("viewing_history/", UserHistoryView.as_view(), name="viewing_history"),
]
