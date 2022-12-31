

from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView

from mainapp.models.category import Category


class IndexView(TemplateView):
    template_name = 'index.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.filter(parent__isnull=True)
        return context
    
    
class ProductListView(View):
    template_name = 'product_list.html'
    
    def get(self, request, slug):
        products = []
        category = Category.objects.get(slug=slug)
        products.extend(list(category.products.all()))
        
        for subcategory in category.children.all():
            products.extend(list(subcategory.products.all()))
        
        context = {
            'products': products
        }

        return render(request, self.template_name, context=context)
        