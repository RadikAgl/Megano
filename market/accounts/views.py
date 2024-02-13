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


def main_page(request):
    """ф-я которая возвращает на главную страницу"""
    return render(request, "accounts/catalog.jinja2")


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
            return redirect("user:main_page")
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
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("user:main_page")
            else:
                messages.error(request, "нет пользователя с таким Email или неверный пароль")
                return render(request, "accounts/login.jinja2", {"form": form})

        else:
            messages.error(request, 'не верно указаны данные')
            return render(request, "accounts/login.jinja2", {"form": form})
    else:
        form = LoginForm()
        return render(request, "accounts/login.jinja2", {"form": form})


class PasswordReset(PasswordResetView):
    """
    Представление для сброса пароля. Отправляет электронное письмо с инструкциями
    по сбросу пароля на указанный электронный адрес.



    success_url: str
        URL-адрес, на который перенаправляется пользователь после успешного
        запроса на сброс пароля.
    """

    template_name = "accounts/e-mail.jinja2"
    email_template_name = "accounts/reset_password.jinja2"
    form_class = PasswordResetForm
    success_url = reverse_lazy("user:reset_password_done")

    def form_valid(self, form):
        """
        Обработчик вызывается при успешном вводе данных в форму.
        Перед отправкой электронного письма проверяет наличие пользователя
        с указанным адресом электронной почты.

        Parameters:
        - form: Form
            Форма с введенными данными.

        Returns:
        - HttpResponseRedirect
            Перенаправляет пользователя на страницу успешного запроса на сброс пароля.
        """
        email = form.cleaned_data["email"]
        try:
            get_user_model().objects.get(email=email)
        except ObjectDoesNotExist:
            messages.error(self.request, "нет пользователя с таким Email")
            return self.form_invalid(form)
        return super().form_valid(form)


class UpdatePasswordView(PasswordResetConfirmView):
    """
    Представление для обновления пароля. Позволяет пользователю изменить свой пароль
    после успешного запроса на сброс.


    success_url: str
        URL-адрес, на который перенаправляется пользователь после успешного
        обновления пароля.
    """

    template_name = "accounts/password.jinja2"
    form_class = CustomPasswordForm
    success_url = reverse_lazy("user:password_reset_complete")

    def form_valid(self, form):
        """
        Обработчик вызывается при успешном вводе нового пароля.
        Сохраняет новый пароль пользователя.

        Parameters:
        - form: Form
            Форма с введенным новым паролем.


        """
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Обработчик вызывается при ошибке ввода нового пароля.
        Добавляет сообщение об ошибке в систему сообщений Django.

        Parameters:
        - form: Form
            Форма с ошибками.

        Returns:
        - HttpResponseRedirect
            Перенаправляет пользователя на страницу с формой обновления пароля.
        """
        messages.error(self.request, f"{form.errors}")
        return super().form_invalid(form)
