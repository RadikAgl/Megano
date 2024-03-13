from django.urls import path
from .views import ResetCacheView, edit_settings

app_name = "settings_app"

urlpatterns = [
    path("reset-cache/", ResetCacheView.as_view(), name="reset_cache"),
    path("edit-settings/", edit_settings, name="edit_settings"),
]
