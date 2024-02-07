from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True)

    class Meta:
        app_label = "accounts"


class BuyerGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(User, related_name="buyers", blank=True)

    def __str__(self):
        return self.name


class UserGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(User, related_name="users", blank=True)


class AdminGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(User, related_name="admins", blank=True)
