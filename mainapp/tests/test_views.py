from django.contrib.admin import AdminSite
from django.test import TestCase, Client

from mainapp.admin import ProductAdmin
from mainapp.models.brand import Brand
from mainapp.models.category import Category
from mainapp.models.product import Product

class MockRequest:
    pass

request = MockRequest()

class TestMainAppModelAdmin(TestCase):
    
    def setUp(self) -> None:
        self.c = Client()
        self.category = Category.objects.create(name='shoes', slug='shoes')
        self.sub_category = Category.objects.create(name='snickers', slug='snickers', parent=self.category)
        self.brand = Brand.objects.create(name='brand-1', slug='brand-1', description='brand-1 description')
    
        self.product_1 = Product.objects.create(
            category=self.sub_category,
            name='product_1',
            code='123',
            slug='product-1',
            shirt_slogan='short_slogan',
            brand=self.brand,
            active=True,
            description='product_1 desc',
            manufacture='China',
            price=50,
            discount=10,
        )

        self.app_admin = ProductAdmin(Product, AdminSite())

    def test_make_inactive(self):
        self.app_admin.make_inactive(request, Product.objects.all())
        self.assertFalse(self.product_1.active)
    
    def test_make_active(self):
        self.app_admin.make_active(request, Product.objects.all())
        self.assertTrue(self.product_1.active)
        
    