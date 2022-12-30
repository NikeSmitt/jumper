from django.db.models.signals import post_delete
from django.dispatch import receiver

from mainapp.models.product_image import ProductImage


@receiver(post_delete, sender=ProductImage)
def _product_image_delete(sender, instance, **kwargs):
    instance.image.delete(False)
