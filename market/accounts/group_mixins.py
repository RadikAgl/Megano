"""
Модуль, содержащий миксины для проверки принадлежности пользователей к определенным группам.

Classes:
    GroupRequiredMixin: Миксин, требующий принадлежности пользователя к определенным группам.
    SellersRequiredMixin: Миксин, требующий принадлежности пользователя к группе "Sellers".
    BuyersRequiredMixin: Миксин, требующий принадлежности пользователя к группе "Buyers".
"""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group


class GroupRequiredMixin(UserPassesTestMixin):
    """
    Миксин, который требует, чтобы пользователь был членом определенной группы.
    """

    def test_func(self):
        user = self.request.user
        if Group.objects.filter(user=user, name__in=["Sellers", "Buyers"]).exists():
            return True
        return False


class SellersRequiredMixin(UserPassesTestMixin):
    """
    Миксин, который требует, чтобы пользователь был продавцом.
    """

    def test_func(self):
        user = self.request.user
        if Group.objects.filter(user=user, name="Sellers").exists():
            return True
        return False


class BuyersRequiredMixin(UserPassesTestMixin):
    """
    Миксин, который требует, чтобы пользователь был покупателем.
    """

    def test_func(self):
        user = self.request.user
        if Group.objects.filter(user=user, name="Buyers").exists():
            return True
        return False
