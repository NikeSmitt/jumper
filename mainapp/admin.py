from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils.safestring import mark_safe

from mainapp.models.brand import Brand
from mainapp.models.category import Category
from mainapp.models.color import Color
from mainapp.models.product import Product
from mainapp.models.product_image import ProductImage
from mainapp.models.size import Size


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class ProductImageInline(TabularInline):
    extra = 1
    model = ProductImage


class SizeInline(TabularInline):
    extra = 1
    model = Size


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (SizeInline, ProductImageInline, )
    list_display = ['id', 'name', 'image_tag']
    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': CheckboxSelectMultiple}
    # }
    
    def image_tag(self, obj):
        """Получаем изображение"""
        images = obj.images.all()
        if len(images):
            return mark_safe('<img src="%s" width="100" height="100" />' % images[0].image.url)
    
    image_tag.short_description = 'Image'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass
