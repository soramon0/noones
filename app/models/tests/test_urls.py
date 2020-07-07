import uuid

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from models import views


class TestUrls(SimpleTestCase):
    def test_list_models_url_resolves(self):
        url = reverse('models')
        self.assertEquals(resolve(url).func, views.list_models)

    def test_detail_model_url_resolves(self):
        url = reverse('model', args=[uuid.uuid4()])
        self.assertEquals(resolve(url).func, views.detail_model)
