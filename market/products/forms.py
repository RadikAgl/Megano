""" Формы приложения products """
from django import forms
from django.forms import Textarea
from .models import Review


class ReviewsForm(forms.ModelForm):
    """
    Форма для добавления отзыва к товару
    """

    class Meta:
        """
        Метаданные класса ReviewForm
        """

        model = Review
        fields = ("product", "text", "rating")
        widgets = {
            "text": Textarea(
                attrs={
                    "class": "form-textarea",
                    "placeholder": "Review",
                    "id": "review",
                }
            ),
            "rating": forms.NumberInput(
                attrs={
                    "class": "form-numberinput",
                    "placeholder": "Rating",
                    "id": "rating",
                    "min": 1,
                    "max": 5,
                }
            ),
        }
