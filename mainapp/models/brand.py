
from django.db import models


class Brand(models.Model):
    """Бренд товара"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название бренда')
    description = models.TextField(verbose_name='Описание бренда')
    slug = models.SlugField()
    
    def __str__(self):
        return self.name


