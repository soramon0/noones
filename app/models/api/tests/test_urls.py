import uuid

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from models.api import views


class TestAPIUrls(SimpleTestCase):
    def test_me_url_resolves(self):
        url = reverse('models:me')
        self.assertEquals(resolve(url).func, views.me)

    def test_list_models_url_resolves(self):
        url = reverse('models:list_models')
        self.assertEquals(resolve(url).func.view_class, views.ListModels)

    def test_update_model_url_resolves(self):
        url = reverse('models:update_model', args=(uuid.uuid4(),))
        self.assertEquals(resolve(url).func.view_class, views.UpdateModel)

    def test_search_models_url_resolves(self):
        url = reverse('models:search_models')
        self.assertEquals(resolve(url).func.view_class, views.SearchModels)

    def test_contact_model_url_resolves(self):
        url = reverse('models:contact_model')
        self.assertEquals(resolve(url).func, views.contact_model)

    def test_list_profile_pictures_url_resolves(self):
        url = reverse('models:list_profile_pictures')
        self.assertEquals(resolve(url).func.view_class,
                          views.ListPorfilePictures)

    def test_delete_profile_picture_url_resolves(self):
        url = reverse('models:delete_profile_picture', args=(1,))
        self.assertEquals(resolve(url).func.view_class,
                          views.ProfilePictureAPIView)

    def test_mark_profile_picture_url_resolves(self):
        url = reverse('models:mark_profile_picture', args=(1,))
        self.assertEquals(resolve(url).func, views.mark_as_profile_picture)

    def test_list_cover_pictures_url_resolves(self):
        url = reverse('models:list_cover_pictures')
        self.assertEquals(resolve(url).func.view_class,
                          views.ListCoverPictures)

    def test_delete_cover_picture_url_resolves(self):
        url = reverse('models:delete_cover_picture', args=(1,))
        self.assertEquals(resolve(url).func.view_class,
                          views.CoverPictureAPIView)

    def test_mark_cover_picture_url_resolves(self):
        url = reverse('models:mark_cover_picture', args=(1,))
        self.assertEquals(resolve(url).func, views.mark_as_cover_picture)
