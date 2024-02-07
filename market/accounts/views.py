from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, CustomPasswordForm


def register(request):
    """
    Обрабатывает запросы на регистрацию пользователя.

    Args:
        request: HttpRequest объект.

    Returns:
        HttpResponse: Возвращает HttpResponse с редиректом на указанный URL в случае успешной регистрации.
                      В случае ошибки возвращает HttpResponse с отображением формы регистрации и ошибок.

    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("#")
        else:
            return render(request, "accounts/registr.jinja2", {"form": form.errors})
    else:
        form = RegistrationForm()
        return render(request, "accounts/registr.jinja2", {"form": form.errors})


def login_view(request):
    """
    Обрабатывает запросы на вход пользователя.

    Args:
        request: HttpRequest объект.

    Returns:
        HttpResponse: Возвращает HttpResponse с редиректом на указанный URL в случае успешного входа.
                      В случае ошибки возвращает HttpResponse с отображением формы входа и сообщением об ошибке.

    """
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("#")
        else:
            return render(request, "accounts/login.jinja2", {"form": form.error_messages.get("invalid_login")})
    else:
        form = LoginForm()
        return render(request, "accounts/login.jinja2", {"form": form})


class PasswordReset(PasswordResetView):
    template_name = "accounts/e-mail.jinja2"
    email_template_name = "accounts/reset_password.jinja2"
    form_class = PasswordResetForm
    success_url = reverse_lazy("user:reset_password_done")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            get_user_model().objects.get(email=email)
        except ObjectDoesNotExist:
            messages.error(self.request, "нет пользователя с таким Email")
            return self.form_invalid(form)

        return super().form_valid(form)


class UpdatePasswordView(PasswordResetConfirmView):
    template_name = "accounts/password.jinja2"
    form_class = CustomPasswordForm
    success_url = reverse_lazy("user:password_reset_complete")

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f"{form.errors}")
