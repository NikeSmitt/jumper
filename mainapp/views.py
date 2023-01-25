from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from mainapp.models.category import Category
from mainapp.models.product import Product
from mainapp.models.tag import Tag
from newsapp.models import NewsItem


class IndexView(TemplateView):
    """Вьюшка заглавной страницы"""
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_products'] = Product.objects.filter(top_selling=True)
        context['head_products'] = Product.objects.filter(shown_on_main=True)
        context['tag_man'] = Tag.objects.filter(tag='man').first()
        context['tag_woman'] = Tag.objects.filter(tag='woman').first()
        context['tag_lifestyle'] = Tag.objects.filter(tag='lifestyle').first()
        context['additional_product'] = Product.objects.filter(
            ~Q(additional_product_image='') & Q(additional_product_image__isnull=False)
        ).first()
        context['products_for_user'] = Product.objects.all()[:7]
        context['news_list'] = NewsItem.objects.all()[:10]
        return context


class ProductListView(View):
    """Вьюшка товаров в соответствии с выбранной категорией"""
    template_name = 'product_list.html'
    
    def get(self, request, slug):
        products = []
        category = Category.objects.get(slug=slug)
        for sub_category in category.children.all():
            products.extend(list(sub_category.products.all()))
        
        paginator = Paginator(products, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        for subcategory in category.children.all():
            products.extend(list(subcategory.products.all()))
        
        context = {
            'category': category,
            'products': products,
            'page_obj': page_obj,
        }
        
        return render(request, self.template_name, context=context)


class ProductTagListView(View):
    """Вьюшка товаров в соответствии с выбранным тегом"""
    
    template_name = 'product_list.html'
    
    def get(self, request, slug):
        tag = get_object_or_404(Tag, tag=slug)
        products = tag.products.all()

        paginator = Paginator(products, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'tag': tag,
            'products': products,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context=context)


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Product
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['category'] = self.object.category
        context['sizes'] = self.object.sizes
        return context



