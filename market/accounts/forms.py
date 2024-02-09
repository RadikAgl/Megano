from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django import forms


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
        fields = ["username", "email", "password1"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле для повторного ввода пароля
        self.fields.pop("password2", None)


class LoginForm(AuthenticationForm):
    """
    Форма входа пользователя.
    """

    class Meta:
        """указание полей для логина"""
        model = get_user_model()
        fields = ["username", "password"]


class CustomPasswordForm(SetPasswordForm):
    """
    Форма изменения пароля.
    """

    class Meta:
        """поля для измены пароля"""
        fields = ["new_password1"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поле для повторного ввода нового пароля обязательным
        self.fields["new_password2"].required = True
        # Убираем поле для повторного ввода нового пароля
        self.fields.pop("new_password2", None)
