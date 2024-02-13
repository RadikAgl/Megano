from django.contrib import admin  # noqa F401

from .models import Category, Product, Tag

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Tag)
