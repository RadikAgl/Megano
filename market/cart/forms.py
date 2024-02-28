""" Формы приложения Cart """

from django import forms

from cart.models import ProductInCart


class CartAddProductForm(forms.Form):
    """Форма для обновления товаров в корзине"""

    quantity = forms.IntegerField(
        min_value=1,
        max_value=21,
        widget=forms.TextInput(
            attrs={
                "class": "Amount-input form-input",
                "min": "1",
                "max": "101",
                "size": "2",
                "maxlength": "2",
                "readonly": True,
            }
        ),
        label="",
    )
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartAddProductModelForm(forms.ModelForm):
    """Форма для добавления товаров в корзину из карточки товара"""

    class Meta:
        model = ProductInCart
        fields = ("quantity",)
        widgets = {
            "quantity": forms.TextInput(
                attrs={
                    "class": "Amount-input form-input",
                    "min": "1",
                    "max": "21",
                    "size": "2",
                    "maxlength": "2",
                    "readonly": True,
                }
            )
        }
