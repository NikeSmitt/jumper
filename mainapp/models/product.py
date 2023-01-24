import decimal

from django.contrib.contenttypes.fields import GenericRelation

from django.db import models
from django.urls import reverse

from django.utils.text import slugify

from mainapp.models.brand import Brand
from mainapp.models.category import Category
from mainapp.models.choices import GENDERS_CHOICES
from mainapp.models.tag import Tag


class Product(models.Model):
    """Непосредственно товар"""
    
    category = models.ForeignKey(Category, related_name='products', blank=True, on_delete=models.SET_NULL, null=True)
    
    name = models.CharField(max_length=200, verbose_name='Название товара', db_index=True)
    code = models.CharField(max_length=30, verbose_name='Артикул', db_index=True, null=True, blank=True)
    
    shirt_slogan = models.CharField(
        max_length=200,
        verbose_name='Короткое описание',
        null=True,
        blank=True,
    )
    
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='products')
    gender = models.CharField(choices=GENDERS_CHOICES, max_length=1, verbose_name='Пол')
    slug = models.SlugField()
    colors = models.ManyToManyField('Color', related_name='products', blank=True)
    active = models.BooleanField(default=True, verbose_name='Активен')
    deleted = models.BooleanField(default=False)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    # quantity = models.PositiveIntegerField(default=0)
    manufacture = models.CharField(max_length=50, verbose_name='Производство', blank=True, null=True)
    price = models.FloatField(verbose_name='Цена', default=0.0)
    
    discount = models.SmallIntegerField(default=0, verbose_name='Скидка')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    top_selling = models.BooleanField(
        verbose_name='Топовые товары',
        help_text='Вывод товара на главную страницу в разделе лучшие продажи',
        default=False,
    )
    
    index_page_image = models.ImageField(
        verbose_name='Картинка на заглавной странице',
        upload_to='main_page_images',
        null=True,
        help_text='Размер изображения 1450х750',
        blank=True,
    )
    
    main_page_title = models.CharField(
        max_length=50,
        null=True,
        verbose_name='Заголовок товара на главной странице',
        blank=True,
    )
    
    main_page_subtitle = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Подзаголовок товара на главной странице',
        blank=True,
    )
    
    shown_on_main = models.BooleanField(
        verbose_name='Показывать на главной странице',
        default=False,
        help_text='Проверить наличие соответсвующий картинки'
    )
    
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)
    
    additional_product_image = models.ImageField(
        verbose_name='Дополнительное изображение',
        upload_to='main_page_images/additional',
        null=True,
        help_text='1200x800 - Изображение для отображения товара как дополнительного в центре заглавной страницы',
        blank=True,
    )
    
    def get_old_price(self):
        if self.discount and self.price:
            return int(self.price * (self.discount / (100 - self.discount) + 1))
    
    def get_total_quantity(self):
        pass
    
    def get_absolute_path(self):
        return reverse('mainapp:product_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return f'{self.name})'
