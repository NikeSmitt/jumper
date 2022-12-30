from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import IntegrityError
from django.utils import timezone

from mainapp.models.brand import Brand
from mainapp.models.category import Category
from mainapp.models.color import Color
from mainapp.models.product import Product
from mainapp.models.product_image import ProductImage


class Command(BaseCommand):
    help = 'This will populate your db with fake products'
    
    def handle(self, *args, **options):
        self._create_superuser()
        self._create_categories()
        self._create_colors()
        self._create_brands()
        self._create_products()
    
    def _create_categories(self):
        c, _ = Category.objects.get_or_create(name='Обувь', slug='shoes')
        for n, slug in [('Кроссовки', 'snickers'),
                        ('Баскетбольные кроссовки', 'basket_snickers'),
                        ('Сандалии', 'sandals'),
                        ('Кеды', 'gumshoes')]:
            try:
                Category.objects.create(name=n, parent=c, slug=slug)
            except IntegrityError:
                pass
        
        c, _ = Category.objects.get_or_create(name='Одежда', slug='clothes')
        for n, slug in [
            ('Компрессионное бельё', 'compression-underwear'),
            ('Толстовки', 'hoodies'),
            ('Футболки', 't-shirts',),
            ('Шорты', 'Shorts'),
        ]:
            try:
                Category.objects.create(name=n, parent=c, slug=slug)
            except IntegrityError:
                pass
    
    def _create_colors(self):
        colors = [
            ('Черный', 'black'),
            ('Белый', 'white')
        ]
        
        for col, slug in colors:
            try:
                Color.objects.create(name=col, slug=slug)
            except IntegrityError:
                pass
    
    def _create_brands(self):
        lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et ' \
                'dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris'
        brands = [
            ('Nike', 'nike'),
            ('Adidas', 'adidas'),
            ('Hard', 'hard'),
            ('Puma', 'puma'),
        ]
        
        for name, slug in brands:
            try:
                Brand.objects.create(name=name, slug=slug, description=lorem)
            except IntegrityError:
                pass
    
    def _create_products(self):
        products = [
            {"category": 2,
             "name": "jordan 1 mid se",
             "brand": 1,
             "gender": "М",
             "slug": "jordan-1-mid-se",
             "active": True,
             "created": "2022-12-29T20:01:07.308Z",
             "modified": "2022-12-29T20:03:34.990Z",
             "deleted": False,
             "description": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
             "manufacture": "Китай",
             "price": "16990.00",
             "discount": 0,
             "colors": [
                 1,
                 2
             ]}
        ]
        
        for product in products:
            p = Product.objects.create(
                category_id=product['category'],
                name=product['name'],
                brand_id=product['brand'],
                gender=product['gender'],
                slug=product['slug'],
                active=product['active'],
                deleted=False,
                description=product['description'],
                manufacture=product['manufacture'],
                price=product['price'],
                discount=product['discount'],
            )
            for _id in product['colors']:
                p.colors.add(_id)
            p.save()
        
        ProductImage.objects.create(image='images/Nike/jordan-1-mid-se-1', product=p)
    
    def _create_superuser(self):
        user = get_user_model()
        name = 'admin'
        try:
            user.objects.create_superuser(username=name, password=name)
        except IntegrityError:
            pass
