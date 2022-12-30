from mainapp.models.mixins import ContentTypeMixin
from django.db import models

from mainapp.models.product import Product


def img_dir(instance, filename):
    try:
        images = instance.product.images.all()
        count = len(images)
        return '/'.join(
            ['images', f'{instance.product.brand.name}', f'{instance.product.slug}-{count + 1}'])
    except AttributeError as e:
        print(e)
        return filename


class ProductImage(models.Model):
    """Картинка для товара"""
    image = models.ImageField(upload_to=img_dir)
    added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    
    def __str__(self):
        return self.image.name
