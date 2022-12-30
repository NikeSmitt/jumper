from django.test import TestCase

from mainapp.models import ShoeProduct


class TestMainappProducts(TestCase):
    
    def testCreatingShoeProduct(self):
        shoe = ShoeProduct()
        