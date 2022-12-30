from django.contrib.contenttypes.fields import GenericRelation

from django.db import models

from django.utils.text import slugify

from mainapp.models.brand import Brand
from mainapp.models.category import Category
from mainapp.models.choices import GENDERS_CHOICES


class Product(models.Model):
    """Непосредственно товар"""
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    
    name = models.CharField(max_length=200, verbose_name='Название товара', db_index=True)
    # code = models.
    
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='products')
    gender = models.CharField(choices=GENDERS_CHOICES, max_length=1, verbose_name='Пол')
    slug = models.SlugField()
    colors = models.ManyToManyField('Color', related_name='products', blank=True)
    active = models.BooleanField(default=True, verbose_name='Активен')
    deleted = models.BooleanField(default=False)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    # quantity = models.PositiveIntegerField(default=0)
    manufacture = models.CharField(max_length=50, verbose_name='Производство', blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена', default=0.0)
    discount = models.SmallIntegerField(default=0, verbose_name='Скидка')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    
    def get_total_quantity(self):
        pass
    
    def __str__(self):
        return f'{self.name})'
