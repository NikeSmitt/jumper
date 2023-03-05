from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from mainapp.models.product import Product
from mainapp.models.size import Size


class Order(models.Model):
    """Заказ пользователя"""
    
    order_number = models.CharField(
        verbose_name='Номер заказа',
        max_length=10,
    )
    
    first_name = models.CharField(
        verbose_name='Имя заказчика',
        max_length=30,
        blank=True,
        null=True,
    )
    
    phone = models.CharField(
        verbose_name='Телефон заказчика для обратной связи',
        max_length=12,
    )
    
    email = models.EmailField(
        verbose_name='Email заказчика',
        blank=True,
        null=True,
    )
    
    last_name = models.CharField(
        verbose_name='Имя заказчика',
        max_length=30,
        blank=True,
        null=True,
    )
    
    address = models.CharField(
        verbose_name='Адрес заказчика',
        max_length=300,
        blank=True,
        null=True,
    )
    
    city = models.CharField(
        verbose_name='Город заказчика',
        max_length=30,
        blank=True,
        null=True,
    )
    
    created_at = models.DateTimeField(
        verbose_name='Дата создания заказа',
        auto_now_add=True,
    )
    
    comment = models.TextField(
        verbose_name='Дополнения к заказу',
        blank=True,
        null=True
    )
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self):
        return self.created_at.strftime("%m/%d/%Y - %H:%M:%S")


class OrderItem(models.Model):
    """Товар, который попадает в заказ"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='К какому заказу относится',
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Товар в заказе',
    )
    
    size = models.ForeignKey(
        Size,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Размер товара',
    )
    
    quantity = models.SmallIntegerField(
        verbose_name='Количество',
    )
    
    def __str__(self):
        return f'{self.product} - Размер: {self.size.value} - Количество: {self.quantity}'
    
    class Meta:
        verbose_name = 'Продукт в заказе'
        verbose_name_plural = 'Продукты в заказе'


@receiver(pre_save, sender=Order)
def generate_order_number(sender, instance, **kwargs):
    today = timezone.now()
    count = Order.objects.filter(created_at__day=today.day).count()
    try:
        number = f'{today.strftime("%y%m%d")}-{count + 1}'
    except ValueError as e:
        print(e)
    else:
        instance.order_number = number
        # instance.save()