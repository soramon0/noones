# Generated by Django 3.0.3 on 2020-05-29 22:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('models', '0003_auto_20200529_2240'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasuresClone',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('taille', models.DecimalField(decimal_places=2, max_digits=5)),
                ('taillenombrill', models.DecimalField(decimal_places=2, max_digits=5)),
                ('buste', models.IntegerField()),
                ('epaules', models.IntegerField()),
                ('hanches', models.IntegerField()),
                ('poids', models.IntegerField()),
                ('pointure', models.IntegerField()),
                ('cheveux', models.CharField(max_length=100)),
                ('yeux', models.CharField(max_length=100)),
                ('measure', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='models.Mensuration')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
