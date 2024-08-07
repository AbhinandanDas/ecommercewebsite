from unittest import skip
from django.test import TestCase

from django.contrib.auth.models import User
from store.models import Category,Product

from django.test import Client

class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
    
    def test_url_allowed_hosts(self):
        """test allowed hosts"""
        response = self.c.get('/')
        self.assertEqual(response.status_code,200)


