from django.core.management.base import BaseCommand
from core.models import User
from django_seed import Seed

from models.models import Model, Mensuration, History

import random
import decimal


class Command(BaseCommand):
    help = 'Seeds the database'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        # TODO(karim): add more fields
        colors = ['brown', 'yellow']
        countries = ['maroc']
        cities = ['marrakech', 'agadir', 'fes', 'rabat']

        seeder.add_entity(User, 1, {
            'password': lambda x: '123456'
        })
        seeder.add_entity(History, 1)
        seeder.add_entity(Mensuration, 1, {
            'taille':           lambda x: random.uniform(1.4, 2.0),
            'taillenombrill':   lambda x: random.uniform(1.4, 2.0),
            'buste':            lambda x: random.randint(1, 50),
            'epaules':          lambda x: random.randint(1, 50),
            'hanches':          lambda x: random.randint(1, 50),
            'poids':            lambda x: random.randint(1, 50),
            'pointure':         lambda x: random.randint(1, 50),
            'permitted':        lambda x: True,
            'cheveux':          lambda x: colors[random.randint(0, len(colors) - 1)],
            'yeux':             lambda x: colors[random.randint(0, len(colors) - 1)],
        })
        seeder.add_entity(Model, 1, {
            'cin':             lambda x: random.randint(10000, 99999),
            'handle':          lambda x: seeder.faker.name().replace(' ', '-'),
            'country':         lambda x: countries[random.randint(0, len(countries) - 1)],
            'city':            lambda x: cities[random.randint(0, len(cities) - 1)],
            'profilePicture':  None,
            'coverPicture':    None,
        })

        seeder.execute()
        self.stdout.write('Insertion done')