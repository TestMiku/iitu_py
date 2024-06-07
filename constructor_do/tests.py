from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from constructor_do.views import delete_order
from calculator.models import Data7112


class MainViewTests(TestCase):
    def setUp(self):
        self.orders = Data7112.objects.all()