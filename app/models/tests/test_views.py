import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from . import factories


class TestViews(TestCase):
    def setUp(self):
        self.search_url = reverse('search')
        self.model = factories.ModelFactory()
        self.model_details_url = reverse('model', args=(self.model.id,))

    def test_list_models(self):
        res = self.client.get(reverse('models'))

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'models/index.html')

    def test_model_details_returns_404(self):
        res = self.client.get(reverse('model', args=(uuid.uuid4(),)))

        self.assertEquals(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_model_details_with_no_pictures(self):
        res = self.client.get(self.model_details_url)
        context = res.context[-1]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'models/model.html')
        self.assertIn('model', context)
        self.assertIn('measures', context)
        self.assertIn('photos', context)
        self.assertIn('profile', context)
        self.assertIn('cover', context)
        self.assertEqual(len(context['photos']), 0)
        self.assertEqual(context['profile'], None)
        self.assertEqual(context['cover'], None)

    def test_model_details(self):
        factories.ProfilePictureFactory(model=self.model)

        res = self.client.get(self.model_details_url)
        context = res.context[-1]

        self.assertNotEqual(len(context['photos']), 0)
        self.assertNotEqual(context['profile'], None)
        self.assertNotEqual(context['cover'], None)

    def test_search_models_with_bad_fields_returns_400(self):
        res = self.client.get(self.search_url)

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(res, 'models/search.html')

    def test_search_models(self):
        q = 'pays=maroc&ville=marrakech&sexe=h&cheveux=brown&yeux=brown&taille=1.40-1.60'
        search_url_with_query_params = f'{self.search_url}?{q}'
        res = self.client.get(search_url_with_query_params)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'models/search.html')
