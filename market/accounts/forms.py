"""
Модуль, содержащий различные формы для работы с пользователями.

Содержит следующие формы:
- RegistrationForm: Форма регистрации нового пользователя.
- LoginForm: Форма для входа в аккаунт.
- CustomPasswordForm: Форма изменения пароля.
- ProfilePasswordForm: Форма для изменения пароля профиля пользователя.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя.
    """

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        """
        форма для регистрации пользователя
        """

        model = get_user_model()
        fields = ["email", "password1"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле для повторного ввода пароля
        self.fields.pop("password2", None)
        self.fields.pop("username", None)


class LoginForm(AuthenticationForm):
    """форма для входа в аккаунт"""

    email = forms.EmailField(required=True)

    class Meta:
        """
        Метаданные формы для работы с пользовательской моделью.
        """

        model = get_user_model()
        fields = ["email", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["username"]


class CustomPasswordForm(SetPasswordForm):
    """
    Форма изменения пароля.
    """

    class Meta:
        """поля для измены пароля"""

        fields = ["new_password1"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поле для повторного ввода нового пароля не обязательным
        self.fields["new_password2"].required = False
        # Убираем поле для повторного ввода нового пароля
        self.fields.pop("new_password2", None)


class ProfilePasswordForm(PasswordChangeForm):
    """Форма для изменения пароля"""

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")

        if new_password1 and not new_password2:
            # Поле new_password2 не заполнено, но мы не хотим, чтобы это вызывало ошибку валидации
            return new_password2

        # Продолжаем с обычной валидацией
        if new_password1 != new_password2:
            raise forms.ValidationError(_("Пароли не совпадают"))

        return new_password2
