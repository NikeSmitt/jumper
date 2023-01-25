from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


class Tag(models.Model):
    """Тег, для каждого товара"""
    
    title = models.CharField(max_length=20, unique=True)
    tag = models.SlugField(unique=True)
    image = models.ImageField(upload_to='tags', null=True, help_text='600x400')
    head_image = models.ImageField(
        upload_to='categories',
        verbose_name='Изображение в заголовке при выборе категории',
        help_text='Размер 1350х550',
        default='cat_head_image_default.jpeg'
    )
    
    def get_absolute_path(self):
        return reverse('mainapp:product_tag_list', kwargs={'slug': self.tag})
    
    def __str__(self):
        return self.tag
