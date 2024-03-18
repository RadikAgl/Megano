from django import forms
from .models import Order


class FirstStepForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("name", "phone")


class SecondStepForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("city", "address", "delivery_type")


class ThirdStepForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('payment_type', )
