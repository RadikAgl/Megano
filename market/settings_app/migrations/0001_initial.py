# Generated by Django 4.2.11 on 2024-04-04 18:34

from django.db import migrations, models
import settings_app.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("docs_dir", models.CharField(default="docs", max_length=255, verbose_name="Директория документов")),
                (
                    "successful_imports_dir",
                    models.CharField(
                        default="successful_imports", max_length=255, verbose_name="Директория успешных импортов"
                    ),
                ),
                (
                    "failed_imports_dir",
                    models.CharField(
                        default="failed_imports", max_length=255, verbose_name="Директория неудачных импортов"
                    ),
                ),
                (
                    "fixture_dir",
                    models.CharField(default="fixtures", max_length=255, verbose_name="Директория фикстур"),
                ),
                (
                    "banners_expiration_time",
                    models.PositiveIntegerField(default=600, verbose_name="Время истечения баннеров"),
                ),
                (
                    "email_access_settings",
                    models.JSONField(
                        default=settings_app.models.get_default_email_settings,
                        help_text="Email access settings from .env",
                        verbose_name="настройки e-mail",
                    ),
                ),
            ],
            options={
                "verbose_name": "настройки сайта",
                "verbose_name_plural": "настройки сайта",
            },
        ),
    ]
