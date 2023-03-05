from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from mainapp.forms import ProductSearchForm
from mainapp.models.category import Category
from mainapp.models.product import Product
from mainapp.models.tag import Tag
from newsapp.models import NewsItem


class IndexView(TemplateView):
    """Вьюшка заглавной страницы"""
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_products'] = Product.objects.filter(top_selling=True).filter(active=True)
        context['head_products'] = Product.objects.filter(shown_on_main=True).filter(active=True)
        context['tag_man'] = Tag.objects.filter(tag='man').first()
        context['tag_woman'] = Tag.objects.filter(tag='woman').first()
        context['tag_lifestyle'] = Tag.objects.filter(tag='lifestyle').first()
        context['additional_product'] = Product.objects.filter(
            ~Q(additional_product_image='') & Q(additional_product_image__isnull=False)
        ).filter(active=True).first()
        context['products_for_user'] = Product.objects.all().filter(active=True)[:7]
        context['news_list'] = NewsItem.objects.all()[:10]
        
        return context


class ProductListView(View):
    """Вьюшка товаров в соответствии с выбранной категорией"""
    template_name = 'product_list.html'
    
    def get(self, request, slug):
        
        category = Category.objects.get(slug=slug)
        products = category.products.filter(active=True)
        
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
        products = tag.products.filter(active=True)

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



class ProductSearchListView(View):
    """Поиск продуктов"""
    template_name = 'product_list.html'
    context = {'searching': True}
    def get(self, request):
        
        paginator = Paginator(Product.objects.all(), 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
        context = {
            # 'products': products,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            products = Product.objects.filter(name__icontains=form.cleaned_data['name'])
            
            paginator = Paginator(products, 8)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            self.context.update({
                'products': products,
                'page_obj': page_obj,
            })
            return render(request, self.template_name, context=self.context)
        return render(request, self.template_name, context=self.context)
    