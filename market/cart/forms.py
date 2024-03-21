""" Формы приложения Cart """

from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartUpdateProductForm(forms.Form):
    """Форма для обновления количества товаров в корзине"""

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


class CartAddProductForm(forms.Form):
    """Форма для добавления товаров в корзину"""

    quantity = forms.IntegerField(required=False, initial=1, widget=forms.HiddenInput)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
