import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from models.tests import factories


class TestViews(TestCase):
    def setUp(self):
        self.search_url = reverse('search')
        self.user = factories.UserFactory(is_public=True, is_active=True)
        self.model = factories.ModelFactory(user=self.user)
        self.history = factories.HistoryFacotry(user=self.user)
        self.measures = factories.MeasuresFactory(user=self.user)
        self.model_details_url = reverse('model', args=(self.model.id,))

    def test_listing_models_view_has_required_context_fields(self):
        res = self.client.get(reverse('models'))
        context = res.context

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'models/index.html')
        self.assertIn('data', context)
        self.assertIn('form', context)

    def test_listing_models_only_shows_public_accounts(self):
        obj = factories.ProfilePictureFactory(
            user=self.user,
            profile=self.model,
            inUse=True
        )

        private_user = factories.UserFactory()
        factories.ProfilePictureFactory(
            user=private_user,
            profile=factories.ModelFactory(user=private_user),
            inUse=True
        )

        res = self.client.get(reverse('models'))
        context = res.context
        public_user = context['data'][0].user

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'models/index.html')
        self.assertEqual(len(context['data']), 1)
        self.assertEqual(obj.user.email, public_user.email)

    def test_listing_models_can_return_zero_accounts(self):
        res = self.client.get(reverse('models'))
        context = res.context

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'models/index.html')
        self.assertEqual(len(context['data']), 0)

    def test_listing_models_returns_accounts(self):
        factories.ProfilePictureFactory(
            user=self.user,
            profile=self.model,
            inUse=True
        )
        user = factories.UserFactory(is_public=True, is_active=True)
        factories.ProfilePictureFactory(
            user=user,
            profile=factories.ModelFactory(user=user),
            inUse=True
        )

        res = self.client.get(reverse('models'))
        context = res.context

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'models/index.html')
        self.assertEqual(len(context['data']), 2)

    def test_model_view_has_required_context_fields(self):
        res = self.client.get(self.model_details_url)
        context = res.context

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'models/model.html')
        self.assertIn('form', context)
        self.assertIn('model', context)
        self.assertIn('measures', context)
        self.assertIn('photos', context)
        self.assertIn('profile', context)
        self.assertIn('cover', context)

    def test_model_does_not_exist(self):
        res = self.client.get(reverse('model', args=(uuid.uuid4(),)))

        self.assertEquals(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_view_model_with_no_pictures(self):
        res = self.client.get(self.model_details_url)
        context = res.context

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'models/model.html')
        self.assertEqual(len(context['photos']), 0)
        self.assertIsNone(context['profile'])
        self.assertIsNone(context['cover'])

    def test_model_with_unused_profile_picture(self):
        factories.ProfilePictureFactory(
            user=self.user,
            profile=self.model,
            inUse=False
        )

        res = self.client.get(self.model_details_url)
        context = res.context

        self.assertIsNone(context['profile'])

    def test_model_with_used_profile_picture(self):
        obj = factories.ProfilePictureFactory(
            user=self.user,
            profile=self.model,
            inUse=True
        )

        res = self.client.get(self.model_details_url)
        context = res.context

        self.assertIsNotNone(context['profile'])
        # pylint: disable=no-member
        self.assertEqual(obj.image.url, context['profile'])

    def test_search_models_with_bad_query_params_returns_400(self):
        res = self.client.get(self.search_url)

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(res, 'models/search.html')
