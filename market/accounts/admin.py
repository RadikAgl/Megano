"""Настройки админ панели приложения accounts"""
from django.contrib import admin
from .models import User, ViewHistory


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Администратор для управления пользователями.

    Поля:

    email: адрес электронной почты пользователя
    is_superuser: признак суперпользователя
    password: пароль пользователя
    """

    list_display = ("email", "is_superuser", "password")


@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    """
    Администратор для  истории просмотров пользователей.

    Поля:

    user: пользователь, просматривающий товар
    product: товар, просматриваемый пользователем
    view_date: дата и время просмотра
    view_count: количество просмотров
    """

    list_display = ("user", "product", "view_date", "view_count")
