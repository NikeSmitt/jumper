from django.db import models
from django.urls import reverse


class NewsTag(models.Model):
    """Тег новости"""
    
    slug = models.SlugField(
        primary_key=True
    )
    
    title = models.CharField(
        max_length=20,
    )
    
    def __str__(self):
        return self.title

class NewsCategory(models.Model):
    """Категория новости"""
    
    title = models.CharField(
        max_length=30,
    )
    
    slug = models.SlugField(primary_key=True)
    
    def __str__(self):
        return self.title


class NewsItem(models.Model):
    """Новость"""
    
    title = models.CharField(
        verbose_name='Название новости',
        max_length=50,
        db_index=True,
    )
    
    trailer = models.CharField(
        verbose_name='Анонс статьи',
        max_length=200,
        blank=True,
        null=True,
    )
    
    author_name = models.CharField(
        verbose_name='Автор',
        max_length=40,
        blank=True,
        null=True,
    )
    
    slug = models.SlugField()
    
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    
    thumb_image = models.ImageField(
        upload_to='news',
        blank=True,
        null=True,
        help_text='Изображение на главной странице 400x266'
    )
    
    body_image = models.ImageField(
        upload_to='news',
        blank=True,
        null=True,
        help_text='Изображение в новости 900х450'
    )
    
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='news',
        null=True,
    )
    
    tags = models.ManyToManyField(
        NewsTag,
        related_name='news',
    )
    
    body = models.TextField(
        verbose_name='Сама новость',
        help_text='Для форматирования можно использовать html теги'
    )
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    
    def __str__(self):
        return self.title
    
    def get_absolute_path(self):
        return reverse('newsapp:news', kwargs={'slug': self.slug})
