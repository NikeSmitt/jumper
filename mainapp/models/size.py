from django.db import models, IntegrityError
from django.db.models import Q

from mainapp.models.product import Product


class Size(models.Model):
    SHOES_SIZE_LIBELS = (
        ('rus', 'RUS'),
        ('uk', 'UK'),
        ('us', 'US'),
        ('eur', 'EUR'),
        ('sm', 'SM'),
    )
    
    CLOTHES_SIZE_LIBELS = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', '2 Extra Large'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    quantity = models.PositiveIntegerField(default=0)
    label_shoes = models.CharField(
        choices=SHOES_SIZE_LIBELS,
        max_length=3,
        verbose_name='Система размера обуви',
        null=True,
        blank=True,
    )
    label_clothes = models.CharField(
        choices=CLOTHES_SIZE_LIBELS,
        max_length=3,
        verbose_name='Система размера одежды',
        null=True,
        blank=True,
    )
    value = models.FloatField(verbose_name='Значение')
    
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    
    def __str__(self):
        return f'{self.value} - {self.product.name}'
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                name='Нельзя использовать сразу несколько систем размеров',
                check=(
                    ~Q(label_shoes__isnull=False, label_clothes__isnull=False)
                )
            )
        ]
        
        ordering = ['product']
        