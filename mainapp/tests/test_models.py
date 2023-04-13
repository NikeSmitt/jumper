
from django.test import TestCase
from django.utils import timezone

from mainapp.models.brand import Brand
from mainapp.models.category import Category
from mainapp.models.color import Color
from mainapp.models.product import Product
from mainapp.models.product_image import ProductImage, img_dir
from mainapp.models.size import Size
from mainapp.models.tag import Tag
from orderapp.models import Order, OrderItem, generate_order_number


class TestCategoryModel(TestCase):
    
    def setUp(self) -> None:
        self.category = Category.objects.create(name='shoes', slug='shoes')
        self.sub_category = Category.objects.create(name='snickers', slug='snickers', parent=self.category)
    
    def test_category_absolute_path(self):
        category_path = self.category.get_absolute_path()
        right_path = '/catalog/shoes/'
        self.assertEqual(category_path, right_path)
    
    def test_subcategory_absolute_path(self):
        category_path = self.sub_category.get_absolute_path()
        right_path = '/catalog/snickers/'
        self.assertEqual(category_path, right_path)
    
    def test_category_str(self):
        self.assertEqual('shoes', str(self.category))
    
    def test_subcategory_str(self):
        self.assertEqual('shoes -> snickers', str(self.sub_category))


class TestBrandModel(TestCase):
    
    def setUp(self) -> None:
        self.brand = Brand.objects.create(name='brand-1', slug='brand-1', description='brand-1 description')
    
    def test_brand_str(self):
        self.assertEqual(str(self.brand), 'brand-1')


class TestColorModel(TestCase):
    def setUp(self) -> None:
        self.color = Color.objects.create(name='purple', slug='purple')
    
    def test_color_str(self):
        self.assertEqual('purple', str(self.color))


class TestProductImage(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name='shoes', slug='shoes')
        self.sub_category = Category.objects.create(name='snickers', slug='snickers', parent=self.category)
        self.brand = Brand.objects.create(name='brand-1', slug='brand-1', description='brand-1 description')
        self.product_1 = Product.objects.create(
            category=self.sub_category,
            name='product_1',
            slug='product-1',
            code='123',
            shirt_slogan='short_slogan',
            brand=self.brand,
            active=True,
            description='product_1 desc',
            manufacture='China',
            price=100.99,
            discount=10,
        )
        
        self.image = ProductImage.objects.create(
            product=self.product_1,
            image='cat_head_image_default.jpeg',
        )
    
    def test_image_str(self):
        self.assertEqual('cat_head_image_default.jpeg', str(self.image))
    
    def test_image_dir(self):
        output = img_dir(self.image, 'image')
        self.assertEqual('images/brand-1/product-1-2', output)
    
    def test_image_dir_exception(self):
        image_name = img_dir(self.category, 'image')
        self.assertEqual('image', image_name)


class TestSizeTagModel(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name='shoes', slug='shoes')
        self.sub_category = Category.objects.create(name='snickers', slug='snickers', parent=self.category)
        self.brand = Brand.objects.create(name='brand-1', slug='brand-1', description='brand-1 description')
        self.product_1 = Product.objects.create(
            category=self.sub_category,
            name='product_1',
            code='123',
            shirt_slogan='short_slogan',
            brand=self.brand,
            active=True,
            description='product_1 desc',
            manufacture='China',
            price=100.99,
            discount=10,
        )
        
        self.size = Size.objects.create(
            product=self.product_1,
            value='40',
        )
        
        self.tag = Tag.objects.create(
            title='tag_title',
            tag='tag-title',
        )
    
    def test_size_str(self):
        self.assertEqual('40', str(self.size))
    
    def test_size_two_labels_in_same_time(self):
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            self.size.label_clothes = 'M'
            self.size.save()
    
    def test_tag_str(self):
        self.assertEqual('tag-title', str(self.tag))
    
    def test_tag_absolute_path(self):
        path = self.tag.get_absolute_path()
        self.assertEqual(path, '/tag/tag-title/')


class TestProductModel(TestCase):
    
    def setUp(self) -> None:
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
        
        self.product_2 = Product.objects.create(
            category=self.sub_category,
            name='product_2',
            code='222',
            slug='product-2',
            shirt_slogan='short_slogan',
            brand=self.brand,
            active=True,
            description='product_1 desc',
            manufacture='China',
            price=100,
            discount=10,
        )
    
    def test_product_str(self):
        self.assertEqual('product_1', str(self.product_1))
    
    def test_product_absolute_path(self):
        path = self.product_1.get_absolute_path()
        self.assertEqual('/product/product-1/', path)
    
    def test_old_price(self):
        self.assertEqual(self.product_1.get_old_price(), 55)
        self.assertEqual(self.product_2.get_old_price(), 111)
    
    def test_get_related_products(self):
        self.product_2.related_products.add(self.product_1)
        self.assertCountEqual([self.product_1], self.product_2.get_related_products())
        self.assertListEqual([self.product_1], list(self.product_2.get_related_products()))
    
    def test_custom_manager(self):
        self.product_1.active = False
        self.product_1.save()
        
        self.assertListEqual([self.product_2], list(Product.products.all()))

        self.product_2.deleted = True
        self.product_2.save()
        self.assertListEqual([], list(Product.products.all()))
        
        
class TestOrder(TestCase):
    def setUp(self) -> None:
        
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
    
        self.product_2 = Product.objects.create(
            category=self.sub_category,
            name='product_2',
            code='222',
            slug='product-2',
            shirt_slogan='short_slogan',
            brand=self.brand,
            active=True,
            description='product_1 desc',
            manufacture='China',
            price=100,
            discount=10,
        )

        self.size = Size.objects.create(
            product=self.product_1,
            value='40',
        )
        
        
        self.order = Order.objects.create(
            first_name='Alex',
            last_name='Bobin',
            phone='923423234',
            email='a@df.com',
            address='улица Ленина, д. 12',
            city='Москва',
            comment='Побыстрее',
        )
        
        self.order_item_1 = OrderItem.objects.create(
            order=self.order,
            product=self.product_1,
            size=self.size,
            quantity=2,
            
        )
        
    def test_order_str(self):
        now_date = timezone.now()
        self.order.created_at = now_date
        self.assertEqual(now_date.strftime("%m/%d/%Y - %H:%M:%S"), str(self.order))
        
    def test_order_item_str(self):
        test_output = 'product_1 - Размер: 40 - Количество: 2'
        self.assertEqual(test_output, str(self.order_item_1))
        
    def test_generate_order_number(self):
        output = f'{timezone.now().strftime("%y%m%d")}-1'
        tested_output = self.order.order_number
        self.assertEqual(output, tested_output)
        
        
