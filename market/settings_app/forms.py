from django import forms
from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            "DOCS_DIR",
            "SUCCESSFUL_IMPORTS_DIR",
            "FAILED_IMPORTS_DIR",
            "BANNERS_EXPIRATION_TIME",
            "email_access_settings",
        ]
