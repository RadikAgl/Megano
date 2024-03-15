from django.contrib import admin

from .forms import SiteSettingsForm
from .models import SiteSettings
from .views import edit_settings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsForm
    change_form_template = "settings_app/settings.html"

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path("edit-settings/", self.admin_site.admin_view(edit_settings), name="settings_app"),
        ]
        return custom_urls + urls
