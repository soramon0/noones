import sqlite3
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Country, City


class Command(BaseCommand):
    # Django command load countries and their cities
    def handle(self, *args, **options):
        # Setup sqlite connection
        db_file = os.path.join(settings.BASE_DIR, 'countries.db')
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        country_count = Country.objects.count()
        if country_count == 0:
            countries = c.execute("SELECT * FROM countries").fetchall()
            Country.objects.bulk_create([
                Country(name=country[0], code=country[1]) for country in countries
            ])
            print('Done seeding countries')
        else:
            print('countries are already seeded.')

        city_count = City.objects.count()
        if city_count == 0:
            countries = Country.objects.only('code').all()
            for country in countries:
                cities = c.execute(
                    "SELECT name FROM cities WHERE code = ?", (country.code,)).fetchall()

                City.objects.bulk_create([
                    City(name=city[0], country=country) for city in cities
                ])
            print('Done seeding cities')
        else:
            print('cities are already seeded.')

        conn.close()
