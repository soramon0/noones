from django.core.management.base import BaseCommand
from core.models import User
from django_seed import Seed

from models.models import Model, Mensuration, History

import random
import decimal


class Command(BaseCommand):
    help = 'Seeds the database'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()
        total = kwargs['total']
        colors = ['brown', 'yellow']
        photo = 'https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
        cover = 'https://images.unsplash.com/photo-1581577281464-9b8f1a71714d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'

        seeder.add_entity(User, total, {
            'password': lambda x: '123456'
        })
        seeder.add_entity(History, total)
        seeder.add_entity(Mensuration, total, {
            'taille':           lambda x: decimal.Decimal(random.randrange(1, 3)),
            'taillenombrill':   lambda x:  decimal.Decimal(random.randrange(1, 3)),
            'buste':            lambda x: random.randint(1, 50),
            'epaules':          lambda x: random.randint(1, 50),
            'hanches':          lambda x: random.randint(1, 50),
            'poids':            lambda x: random.randint(1, 50),
            'pointure':         lambda x: random.randint(1, 50),
            'permitted':        lambda x: True,
            'cheveux':          lambda x: colors[random.randint(0, len(colors) - 1)],
            'yeux':             lambda x: colors[random.randint(0, len(colors) - 1)],
        })
        seeder.add_entity(Model, total, {
            'cin':             lambda x: random.randint(10000, 99999),
            'handle':          lambda x: seeder.faker.name().replace(' ', '-'),
            'profilePicture':  photo,
            'coverPicture':    cover,
        })   
        seeder.execute()
        self.stdout.write('Insertion done')