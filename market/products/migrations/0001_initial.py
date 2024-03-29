# Generated by Django 4.2.9 on 2024-03-29 13:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Banner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=512, verbose_name="название")),
                ("description", models.TextField(null=True, verbose_name="описание")),
                ("actual", models.BooleanField(default=True, verbose_name="актуальность")),
                ("preview", models.ImageField(upload_to="banners", verbose_name="превью")),
                ("link", models.URLField(db_index=True, unique=True, verbose_name="ссылка")),
            ],
            options={
                "verbose_name": "Баннер",
                "verbose_name_plural": "Баннеры",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=512, unique=True, verbose_name="наименование")),
                ("description", models.TextField(blank=True, null=True, verbose_name="описание")),
                ("sort_index", models.PositiveIntegerField(null=True, unique=True, verbose_name="индекс сортировки")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="products.category"
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категорий",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(db_index=True, max_length=100, verbose_name="наименование")),
                ("description", models.CharField(max_length=1000, verbose_name="описание")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="дата создания")),
                ("details", models.JSONField(blank=True, default=dict, verbose_name="детали")),
                ("is_limited", models.BooleanField(default=False, verbose_name="ограниченный тираж")),
                ("is_product_of_the_day", models.BooleanField(default=False, verbose_name="товар дня")),
                (
                    "category",
                    models.ForeignKey(
                        max_length=100,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.category",
                        verbose_name="категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "продукт",
                "verbose_name_plural": "продукты",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="тег")),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="products/%Y/%m/%d/", verbose_name="изображения")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="products.product",
                        verbose_name="продукт",
                    ),
                ),
            ],
            options={
                "verbose_name": "изображения",
                "verbose_name_plural": "изображение",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="tags",
            field=models.ManyToManyField(related_name="product", to="products.tag", verbose_name="тег"),
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "text",
                    models.TextField(
                        validators=[
                            django.core.validators.MinLengthValidator(10),
                            django.core.validators.MaxLengthValidator(1000),
                        ],
                        verbose_name="text",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="дата создания")),
                ("rating", models.IntegerField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="products.product",
                        verbose_name="продукт",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "отзыв",
                "verbose_name_plural": "отзывы",
                "unique_together": {("user", "product")},
            },
        ),
    ]
