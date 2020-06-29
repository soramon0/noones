# Generated by Django 3.0.7 on 2020-06-21 22:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilePictureUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('accept', models.BooleanField(blank=True, null=True)),
                ('decline', models.BooleanField(blank=True, null=True)),
                ('message', models.TextField(blank=True, default='', max_length=500)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Model')),
            ],
            options={
                'verbose_name_plural': 'Profile Picture Updates',
            },
        ),
        migrations.CreateModel(
            name='PhotosUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('accept', models.BooleanField(blank=True, null=True)),
                ('decline', models.BooleanField(blank=True, null=True)),
                ('message', models.TextField(blank=True, default='', max_length=500)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Model')),
                ('related_photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='models.Photo')),
            ],
            options={
                'verbose_name_plural': 'Gallery Updates',
            },
        ),
        migrations.CreateModel(
            name='MeasuresUpdate',
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
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('accept', models.BooleanField(blank=True, null=True)),
                ('decline', models.BooleanField(blank=True, null=True)),
                ('message', models.TextField(blank=True, default='', max_length=500)),
                ('measure', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='models.Mensuration')),
            ],
            options={
                'verbose_name_plural': 'Measure Updates',
            },
        ),
    ]