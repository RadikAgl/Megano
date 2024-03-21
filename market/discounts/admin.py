"""Настройки админ панели приложения discounts"""

from django.contrib import admin
from .models import DiscountProduct, DiscountSet, DiscountCart


class DiscountSetAdmin(admin.ModelAdmin):
    list_display = ["title", "discount_amount", "start_date", "end_date"]


class DiscountCartAdmin(admin.ModelAdmin):
    list_display = ["title", "percentage", "start_date", "end_date", "price_from", "price_to"]


class DiscountProductAdmin(admin.ModelAdmin):
    list_display = ["title", "percentage", "start_date", "end_date", "is_active"]


admin.site.register(DiscountProduct, DiscountProductAdmin)
admin.site.register(DiscountSet, DiscountSetAdmin)
admin.site.register(DiscountCart, DiscountCartAdmin)
