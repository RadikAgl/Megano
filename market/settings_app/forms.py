from typing import Type

from django import forms

from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    """
    Форма для создания и редактирования настроек сайта.

    Эта форма позволяет пользователю создавать и изменять настройки сайта,
    используя соответствующую модель `SiteSettings`.
    """

    class Meta:
        model: Type[SiteSettings] = SiteSettings  # Модель, связанная с формой
        fields: list[str] = [
            "docs_dir",
            "successful_imports_dir",
            "failed_imports_dir",
            "banners_expiration_time",
            "email_access_settings",
            "email_credentials",
        ]  # Поля, отображаемые в форме для редактирования настроек сайта
