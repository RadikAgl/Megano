from django import forms
from django.forms import Textarea
from .models import Review


class ReviewsForm(forms.ModelForm):
    """
    Форма для добавления отзыва к товару
    """

    class Meta:
        model = Review
        fields = ("text", "rating")
        widgets = {
            "text": Textarea(
                attrs={
                    "class": "form-textarea",
                    "placeholder": "Review",
                    "id": "review",
                }
            ),
        }
