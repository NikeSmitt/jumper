from copy import copy

from django.core.paginator import Paginator
from django.db.models import Q, Prefetch, Count
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from mainapp.forms import ProductSearchForm
from mainapp.models import Brand, Banner
from mainapp.models.category import Category
from mainapp.models.product import Product
from newsapp.models import NewsItem


class IndexView(TemplateView):
    """Вьюшка заглавной страницы"""
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['top_products'] = Product.products.filter(top_selling=True)
        # context['head_products'] = Product.products.filter(shown_on_main=True)
        context['additional_product'] = Product.objects.filter(
            ~Q(additional_product_image='') & Q(additional_product_image__isnull=False)
        ).filter(active=True).first()
        context['products_for_user'] = Product.objects.all().filter(active=True)[:7]
        context['news_list'] = NewsItem.objects.all()[:10]
        context['banners'] = Banner.objects.filter(show=True)
        
        return context


class ProductListView(View):
    """Вьюшка товаров в соответствии с выбранной категорией"""
    template_name = 'product_list.html'
    
    def get(self, request, slug):
        
        # получаем список фильтров
        filtered_values = []
        filtered_values.extend(request.GET.getlist('brands'))
        filtered_values.extend(request.GET.getlist('filter_categories'))
        sort_value = request.GET.get('sort')
        
        pr_prod = Prefetch('products', queryset=Product.products.all())
        category = Category.objects.prefetch_related('children').prefetch_related(pr_prod).get(slug=slug)
        
        # получаем продукты для данной категории,
        # то есть фильтрация происходит в рамках той категории в которую мы вошли
        products = category.products.prefetch_related('categories').all()
        filtered_products = set()
        
        # получаем список продуктов с фильтром
        if filtered_values:
            categories = Category.objects.filter(slug__in=filtered_values)
            
            for p in products:
                for cat in p.categories.all():
                    if cat in categories:
                        filtered_products.add(p)
            
            [filtered_products.add(p) for p in category.products.filter(
                Q(brand__slug__in=filtered_values))]
            filtered_products = list(filtered_products)
        else:
            filtered_products = products[:]
        
        # сортировка
        if sort_value and sort_value == 'price':
            filtered_products = sorted(filtered_products, key=lambda a: a.price, reverse=True)
        elif sort_value and sort_value == 'price-desc':
            filtered_products = sorted(filtered_products, key=lambda a: a.price)
        
        # пагинация
        paginator = Paginator(filtered_products, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # получаем списки брендов и категорий
        brands = Brand.objects.filter(products__in=products) \
            .prefetch_related('products') \
            .distinct() \
            .annotate(product_quantity=Count('products', filter=Q(products__active=True)))
        filter_categories = Category.objects.filter(products__in=products).prefetch_related('products').distinct()
        
        context = {
            'filter_categories': filter_categories,
            'category': category,
            'products': filtered_products,
            'page_obj': page_obj,
            'brands': brands,
            'filtered_values': filtered_values,
            'sort_value': sort_value,
            
        }
        
        return render(request, self.template_name, context=context)


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Product
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
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
            products = Product.products.filter(name__icontains=form.cleaned_data['name'])
            
            paginator = Paginator(products, 8)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            self.context.update({
                'products': products,
                'page_obj': page_obj,
            })
            return render(request, self.template_name, context=self.context)
        return render(request, self.template_name, context=self.context)
