from django.db import models
from cart.models import Cart
from accounts.models import User


class PaymentTypes(models.TextChoices):
    CARD = 'card', 'Онлайн картой'


class OrderStatus(models.TextChoices):
    CREATED = 'created', 'Создан'
    OK = 'ok', 'Выполнен'
    DELIVERED = 'delivered', 'Доставляется'
    PAID = 'paid', 'Оплачен'
    NOT_PAID = 'not_paid', 'Не оплачен'


class DeliveryTypes(models.TextChoices):
    REGULAR = 'regular', 'Обычная доставка'
    EXPRESS = 'express', 'Экспресс-доставка'


class Order(models.Model):
    """Модель заказа"""

    name = models.TextField(max_length=20, blank=False, null=False)
    phone = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    delivery_type = models.CharField(max_length=50, choices=DeliveryTypes.choices, verbose_name='delivery type',
                                     blank=False,
                                     default=DeliveryTypes.REGULAR)
    city = models.CharField(max_length=50, verbose_name='city')
    address = models.CharField(max_length=255, verbose_name='address')
    payment_type = models.CharField(max_length=50, choices=PaymentTypes.choices, blank=False,
                                    default=PaymentTypes.CARD,
                                    verbose_name='payment type')
    status = models.CharField(max_length=15, choices=OrderStatus.choices, default=OrderStatus.CREATED,
                              verbose_name='status')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, verbose_name='cart')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='total price')

    class Meta:
        db_table = 'order'
