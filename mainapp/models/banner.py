from django.db import models
from .mixins import ContentTypeMixin


class Banner(ContentTypeMixin):
    title = models.CharField(max_length=200, blank=True, null=True, default='banner')
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    show = models.BooleanField(default=False)
    image = models.ImageField(upload_to='banners/')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-title']
