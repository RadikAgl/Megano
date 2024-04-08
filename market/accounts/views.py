"""
Модуль, содержащий представления для работы с учетными записями пользователей.

Модуль включает в себя следующие классы и функции:

- ProfileView: вью для изменения пароля и email.
- AcountView: вью для страницы пользователя.
- RegistrationView: вью класс для регистрации новых пользователей.
- MyLoginView: вью для аутентификации пользователей.
- PasswordReset: представление для сброса пароля.
- UpdatePasswordView: представление для обновления пароля.
- UserHistoryView: представление истории просмотров пользователя.
- logout_view: функция для выхода из учетной записи.

"""

from typing import Any, List

from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    LoginView,
)
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import FormView, TemplateView

from order.models import OrderStatus, Order
from .forms import RegistrationForm, LoginForm, CustomPasswordForm, ProfilePasswordForm
from .models import ViewHistory


class ProfileView(LoginRequiredMixin, FormView):
    """вью для изменения пароля и email"""

    template_name = "accounts/profile.jinja2"
    form_class = ProfilePasswordForm
    success_url = reverse_lazy("user:profile")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.error(self.request, _("успешно"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("не верный ввод полей"))
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AcountView(LoginRequiredMixin, TemplateView):
    """вюь для страницы пользователя"""

    template_name = "accounts/account.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.request.user
        try:
            if self.request.session[f"{self.request.user.id}"]["id"]:
                Order.objects.filter(user=self.request.user.id).update(status=OrderStatus.PAID)
                context["paid"] = _("оплачено")
                return context
        except KeyError:
            return context


class RegistrationView(FormView):
    """вью класс для регистрации"""

    template_name = "accounts/register.jinja2"
    form_class = RegistrationForm
    success_url = reverse_lazy("user:main")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("не валидная форма или такой пользователь уже есть"))
        return super().form_invalid(form)


class MyLoginView(LoginView):
    """Представление для входа пользователя в систему."""

    template_name = "accounts/login.jinja2"
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, _("нет пользователя с таким Email или неверный пароль"))
            return super().form_invalid(form)


class PasswordReset(LoginRequiredMixin, PasswordResetView):
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
            messages.error(self.request, _("нет пользователя с таким Email"))
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


class UserHistoryView(LoginRequiredMixin, View):
    """Представление истории просмотров пользователя."""

    template_name: str = "accounts/viewing_history.jinja2"

    def get(self, request) -> Any:
        user = request.user
        user_history = ViewHistory.objects.filter(user=user).order_by("-view_date")
        viewed_products: List[Any] = [history.product for history in user_history]

        return render(request, self.template_name, {"viewed_products": viewed_products})


def logout_view(request):
    """Представление для выхода из учетной записи"""
    logout(request)
    return HttpResponseRedirect(reverse("products:index"))
