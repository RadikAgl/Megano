"""Настройки админ панели приложения shops"""
from django.contrib import admin  # noqa F401
from .models import Shop, Offer


class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_info", "description")
    list_filter = ("name", "user")
    search_fields = ("name", "contact_info", "description")


admin.site.register(Shop, ShopAdmin)


class OfferAdmin(admin.ModelAdmin):
    list_display = ("shop", "product", "price", "remains")
    list_filter = ("shop", "remains")
    search_fields = ("shop", "product")


admin.site.register(Offer, OfferAdmin)
