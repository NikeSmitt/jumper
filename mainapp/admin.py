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
from mainapp.models.product_specification import ProductSpec
from mainapp.models.size import Size
from mainapp.models.tag import Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductSpec)
class ProductSpecAdmin(admin.ModelAdmin):
    pass


class ProductImageInline(TabularInline):
    extra = 1
    model = ProductImage


class SizeInline(TabularInline):
    extra = 1
    model = Size


class ProductSpecInline(TabularInline):
    extra = 1
    model = ProductSpec


@admin.action(description='Показывать товары')
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


@admin.action(description='Спрятать товары')
def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (SizeInline, ProductImageInline, ProductSpecInline)
    list_display = ['id', 'name', 'image_tag', 'active']
    list_display_links = ['id', 'name']
    list_filter = ['brand']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    actions = [make_active, make_inactive]
    
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
    list_display = ['value', 'label_clothes', 'product', 'quantity']


admin.site.register(Tag)
