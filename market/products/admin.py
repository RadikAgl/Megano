from django.contrib import admin  # noqa F401

from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)
