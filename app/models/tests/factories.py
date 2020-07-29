import random

import factory
from django.utils import timezone
from django.contrib.auth import get_user_model

from models import models

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('ascii_safe_email')
    password = 'superultimatesecretpassword'


class MeasuresFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Mensuration

    taille = 1.60
    taillenombrill = 1.60
    buste = 16
    epaules = 16
    hanches = 16
    poids = 16
    pointure = 16
    cheveux = 'brown'
    yeux = 'brown'
    user = factory.SubFactory(UserFactory)


class HistoryFacotry(factory.django.DjangoModelFactory):
    class Meta:
        model = models.History

    q1 = factory.Faker('paragraph')
    q2 = factory.Faker('paragraph')
    q3 = factory.Faker('paragraph')
    q4 = factory.LazyFunction(lambda: random.choice(('y', 'n')))
    user = factory.SubFactory(UserFactory)


class ModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Model

    sexe = factory.LazyFunction(lambda: random.choice(('f', 'h')))
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    handle = factory.Faker('slug')
    birth_date = factory.Faker('date_of_birth')
    facebook = factory.Faker('url')
    instagram = factory.Faker('url')
    phone = factory.Faker('phone_number')
    addresse = factory.Faker('address')
    city = factory.Faker('city')
    country = factory.Faker('country')
    zipcode = factory.Faker('zipcode')
    cin = factory.Faker('postcode')

    user = factory.SubFactory(UserFactory)
    measures = factory.SubFactory(MeasuresFactory)
    history = factory.SubFactory(HistoryFacotry)


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Contact

    model = factory.SubFactory(ModelFactory)
    model_full_name = factory.lazy_attribute(
        lambda a: f'{a.model.first_name} {a.model.last_name}')
    model_email = factory.lazy_attribute(lambda a: a.model.user.email)
    full_name = factory.Faker('name')
    email = factory.Faker('ascii_safe_email')
    phone = factory.Faker('phone_number')


class ProfilePictureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProfilePicture

    model = factory.SubFactory(ModelFactory)
    image = factory.django.ImageField()
    inUse = True
