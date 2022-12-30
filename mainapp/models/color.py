from django.db import models
from django.db.models import Q


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название цвета', unique=True)
    slug = models.SlugField(unique=True)
    
    
    
    def __str__(self):
        return self.name
