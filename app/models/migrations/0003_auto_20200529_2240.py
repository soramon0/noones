# Generated by Django 3.0.3 on 2020-05-29 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20200220_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensuration',
            name='taille',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='mensuration',
            name='taillenombrill',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
