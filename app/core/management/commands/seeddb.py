import random
import decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.conf import settings
from core.models import User

from models.models import Profile, Mensuration, History


if settings.DEBUG:
    from django_seed import Seed

    class Command(BaseCommand):
        help = 'Seeds the database'

        def handle(self, *args, **kwargs):
            seeder = Seed.seeder()

            # TODO(karim): add more fields
            colors = ['brown', 'yellow']
            countries = ['maroc']
            cities = ['marrakech', 'agadir', 'fes', 'rabat']
            password = make_password("userpassword")

            seeder.add_entity(User, 1, {
                'password': lambda x: password
            })
            seeder.add_entity(History, 1, {
                'q4': lambda x: 'y',
            })
            seeder.add_entity(Mensuration, 1, {
                'height': lambda x: random.uniform(1.4, 2.0),
                'waist': lambda x: random.uniform(1.4, 2.0),
                'bust': lambda x: random.randint(1, 50),
                'shoulders': lambda x: random.randint(1, 50),
                'hips': lambda x: random.randint(1, 50),
                'weight': lambda x: random.randint(1, 50),
                'shoe_size': lambda x: random.randint(1, 50),
                'permitted': lambda x: True,
                'hair': lambda x: colors[random.randint(0, len(colors) - 1)],
                'eyes': lambda x: colors[random.randint(0, len(colors) - 1)],
            })
            seeder.add_entity(Profile, 1, {
                'nin': lambda x: random.randint(10000, 99999),
                'country': lambda x: countries[random.randint(0, len(countries) - 1)],
                'city': lambda x: cities[random.randint(0, len(cities) - 1)],
            })

            seeder.execute()
            self.stdout.write('Insertion done')
