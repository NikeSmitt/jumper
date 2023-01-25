from django.db import models

from mainapp.models.product import Product


class ProductSpec(models.Model):
    """Спецификация товара"""
    name = models.CharField(
        verbose_name='Название спецификации',
        max_length=50,
        
    )
    
    value = models.CharField(
        verbose_name='Значение спецификации',
        max_length=100,
        
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='spec'
    )
    
    
    class Meta:
        verbose_name = 'Спецификация'
        verbose_name_plural = 'Спецификации'
        
    