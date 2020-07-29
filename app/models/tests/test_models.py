from django.test import TestCase
from django.contrib.auth import get_user_model

from . import factories
from models import models

User = get_user_model()


class TestModels(TestCase):
    def test_user_creation(self):
        user = factories.UserFactory()
        self.assertIsInstance(user, User)
        self.assertEqual(user.__str__(), user.email)

    def test_model_creation(self):
        model = factories.ModelFactory()
        self.assertIsInstance(model, models.Model)
        self.assertEqual(model.__str__(), model.user.email)

    def test_history_creation(self):
        history = factories.HistoryFacotry()
        self.assertIsInstance(history, models.History)
        self.assertEqual(history.__str__(), history.user.email)

    def test_measures_creation(self):
        measures = factories.MeasuresFactory()
        self.assertIsInstance(measures, models.Mensuration)
        self.assertEqual(measures.__str__(), measures.user.email)

    def test_contact_creation(self):
        contact = factories.ContactFactory()
        self.assertIsInstance(contact, models.Contact)
        self.assertEqual(contact.__str__(), contact.model_full_name)

    def test_profile_picture_creation(self):
        profile = factories.ProfilePictureFactory()
        self.assertIsInstance(profile, models.ProfilePicture)
        self.assertEqual(profile.__str__(), profile.image.url)
