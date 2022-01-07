import random

import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from django.contrib.auth import get_user_model

from models import models

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('ascii_safe_email')
    password = 'superultimatesecretpassword'


class MeasuresFactory(DjangoModelFactory):
    class Meta:
        model = models.Mensuration

    height = 1.60
    waist = 1.60
    bust = 16
    shoulders = 16
    hips = 16
    weight = 16
    shoe_size = 16
    hair = 'brown'
    eyes = 'brown'
    user = factory.SubFactory(UserFactory)


class HistoryFacotry(DjangoModelFactory):
    class Meta:
        model = models.History

    q1 = factory.Faker('paragraph')
    q2 = factory.Faker('paragraph')
    q3 = factory.Faker('paragraph')
    q4 = factory.LazyFunction(lambda: random.choice(('y', 'n')))
    user = factory.SubFactory(UserFactory)


class ModelFactory(DjangoModelFactory):
    class Meta:
        model = models.Profile

    gender = factory.LazyFunction(lambda: random.choice(('f', 'h')))
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    birth_date = factory.Faker('date_of_birth')
    facebook = factory.Faker('url')
    instagram = factory.Faker('url')
    phone = factory.Faker('phone_number')
    address = factory.Faker('address')
    city = factory.Faker('city')
    country = factory.Faker('country')
    zipcode = factory.Faker('zipcode')
    nin = factory.Faker('postcode')

    user = factory.SubFactory(UserFactory)


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = models.Contact

    user = factory.SubFactory(UserFactory)
    model_full_name = 'Jake Roger'
    model_email = factory.lazy_attribute(lambda a: a.user.email)
    full_name = factory.Faker('name')
    email = factory.Faker('ascii_safe_email')
    phone = factory.Faker('phone_number')


class ProfilePictureFactory(DjangoModelFactory):
    class Meta:
        model = models.ProfilePicture

    profile = factory.SubFactory(ModelFactory)
    user = factory.SubFactory(UserFactory)
    image = factory.django.ImageField(filename='image.jpg')
