# Generated by Django 3.0.2 on 2020-01-30 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_header_images'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Images',
            new_name='Image',
        ),
    ]
