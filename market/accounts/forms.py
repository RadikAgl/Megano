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
        model = get_user_model()
        fields = ["email", "password"]

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
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


class ProfilePasswordForm(SetPasswordForm):
    email = forms.EmailField(required=True)
    """форма для изменения пароля и email"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'new_password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поле для повторного ввода нового пароля не обязательным
        self.fields["new_password2"].required = False
        # Убираем поле для повторного ввода нового пароля
        self.fields.pop("new_password2", None)
