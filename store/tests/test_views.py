from importlib import import_module
from unittest import skip
from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase,RequestFactory

from django.contrib.auth.models import User
from store.models import Category,Product
from django.urls import reverse
from store.views import products_all 
from django.test import Client

@skip("demonstrating skipping")
class Testskip(TestCase):
    def test_skip_sample(self):
        pass

class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        User.objects.create(username='admin')
        Category.objects.create(name='django',slug='django')
        Product.objects.create(categories_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')


    def test_homepage_url(self):
        """Test homepage response status"""
        response = self.c.get('/')
        self.assertEqual(response.status_code,200)

    def test_url_allowed_hosts(self):
        """test allowed hosts"""
        response = self.c.get('/',HTTP_HOST="noaddress.com")
        self.assertEquals(response.status_code,400)
        response = self.c.get('/',HTTP_HOST="yourdomain.com")
        self.assertEquals(response.status_code,200)

    def test_product_detail(self):
        """test the product detail page"""
        response = self.c.get(reverse('store:product_detail',args=['django-beginners']))
        self.assertEqual(response.status_code,200)

    def test_category_detail(self): 
        """test the category page"""
        response = self.c.get(reverse('store:category_list',args=['django']))
        self.assertEqual(response.status_code,200)

    def test_homepage_html(self):
        """test the homepage html"""
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = products_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
