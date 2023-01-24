from django.contrib import admin

from newsapp.models import NewsTag, NewsCategory, NewsItem


@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    pass


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    pass
