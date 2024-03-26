"""Периодические задачи celery"""
import random

from config import celery_app
from products.models import Product


@celery_app.task
def set_product_of_the_day():
    current_product_of_the_day = Product.objects.filter(is_product_of_the_day=True).first()
    new_product_of_the_day = random.choice(Product.objects.filter(is_limited=True).filter(is_product_of_the_day=True))
    new_product_of_the_day.is_product_of_the_day = True
    new_product_of_the_day.save()
    current_product_of_the_day.is_product_of_the_day = False
    current_product_of_the_day.save()
