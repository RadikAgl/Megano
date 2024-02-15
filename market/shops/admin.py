from django.contrib import admin  # noqa F401
from .models import Shop


class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_info", "description")
    list_filter = ("name", "user")
    search_fields = ("name", "contact_info", "description")


admin.site.register(Shop, ShopAdmin)
