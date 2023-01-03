

from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from mainapp.models.category import Category
from mainapp.models.product import Product


class IndexView(TemplateView):
    """Вьюшка заглавной страницы"""
    template_name = 'index.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.filter(parent__isnull=True)
        return context
    
    
class ProductListView(View):
    """Вьюшка товаров в соответствии с выбранной категорией"""
    template_name = 'product_list.html'
    
    def get(self, request, slug):
        products = []
        category = Category.objects.get(slug=slug)
        products.extend(list(category.products.all()))
        
        for subcategory in category.children.all():
            products.extend(list(subcategory.products.all()))
        
        context = {
            'category': category,
            'products': products
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
    