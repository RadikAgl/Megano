from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", "email", "password1"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password2"].required = False
        self.fields.pop("password2", None)


class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class CustomPasswordForm(SetPasswordForm):
    class Meta:
        fields = ["new_password1"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password2"].required = True
        self.fields.pop("new_password2", None)
