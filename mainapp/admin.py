from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils.safestring import mark_safe

from mainapp.models import Banner
from mainapp.models.brand import Brand
from mainapp.models.category import Category
from mainapp.models.color import Color
from mainapp.models.product import Product
from mainapp.models.product_image import ProductImage
from mainapp.models.product_specification import ProductSpec
from mainapp.models.size import Size


class MainBannerInline(GenericTabularInline):
    model = Banner
    extra = 0


class ProductImageInline(TabularInline):
    extra = 1
    model = ProductImage


class SizeInline(TabularInline):
    extra = 1
    model = Size


class ProductSpecInline(TabularInline):
    extra = 1
    model = ProductSpec


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'header_show', 'order_pos']
    list_editable = ['header_show', 'order_pos']
    inlines = (MainBannerInline,)


@admin.register(ProductSpec)
class ProductSpecAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (SizeInline, ProductImageInline, ProductSpecInline, MainBannerInline)
    list_display = ['id', 'name', 'image_tag', 'active', 'deleted', 'get_categories']
    list_editable = ['active']
    list_display_links = ['id', 'name']
    list_filter = ['brand']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    actions = ['make_active', 'make_inactive']
    
    @admin.action(description='Показывать товары')
    def make_active(self, request, queryset):
        queryset.update(active=True)
    
    @admin.action(description='Спрятать товары')
    def make_inactive(self, request, queryset):
        queryset.update(active=False)
    
    def image_tag(self, obj):
        """Получаем изображение"""
        images = obj.images.all()
        if len(images):
            return mark_safe('<img src="%s" width="100" height="100" />' % images[0].image.url)
    
    image_tag.short_description = 'Image'
    
    def get_categories(self, obj):
        list_items = []
        for c in obj.categories.all():
            list_items.append(f'<li> {str(c)} </li>')
        return mark_safe(f'<ul>{" ".join(list_items)}</ul>')


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
    
@admin.register(Banner)
class MainBannerAdmin(admin.ModelAdmin):
    pass
