from django.db import models


class Category(models.Model):
    """Категория товаров, которая может быть подкатегорией любой глубины"""
    name = models.CharField(max_length=100, verbose_name='название категории')
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)
    
    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name_plural = 'categories'
    
    def __str__(self):
        """Собираем полный путь к данной категории"""
        full_path = [self.name]
        parent = self.parent
        while parent is not None:
            full_path.append(parent.name)
            parent = parent.parent
        
        return ' -> '.join(full_path[::-1])