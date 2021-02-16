# Generated by Django 3.1.2 on 2021-02-16 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('gender', models.CharField(choices=[('f', 'Female'), ('m', 'Male')], default='m', max_length=1, verbose_name='gender')),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
                ('bio', models.CharField(blank=True, max_length=500, verbose_name='biography')),
                ('birth_date', models.DateField(verbose_name='birth date')),
                ('facebook', models.URLField()),
                ('instagram', models.URLField()),
                ('phone', models.CharField(max_length=100, verbose_name='phone')),
                ('address', models.CharField(max_length=100, verbose_name='address')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
                ('country', models.CharField(max_length=100, verbose_name='country')),
                ('zipcode', models.CharField(max_length=50, verbose_name='zipcode')),
                ('nin', models.CharField(max_length=100, verbose_name='nin')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='ProfilePicture',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('inUse', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile Picture',
                'verbose_name_plural': 'Profile Pictures',
            },
        ),
        migrations.CreateModel(
            name='Mensuration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('height', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='height')),
                ('waist', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='waist')),
                ('bust', models.IntegerField(verbose_name='bust')),
                ('shoulders', models.IntegerField(verbose_name='shoulders')),
                ('hips', models.IntegerField(verbose_name='hips')),
                ('weight', models.IntegerField(verbose_name='weight')),
                ('shoe_size', models.IntegerField(verbose_name='shoe size')),
                ('hair', models.CharField(max_length=100, verbose_name='hair')),
                ('eyes', models.CharField(max_length=100, verbose_name='eyes')),
                ('permitted', models.BooleanField(default=False, verbose_name='permitted')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mensuration',
                'verbose_name_plural': 'Mensuration',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('q1', models.CharField(help_text='Who are you?', max_length=500)),
                ('q2', models.CharField(help_text='What do you know about fashion?', max_length=500)),
                ('q3', models.CharField(help_text='Why do we need to approve your registration?', max_length=500)),
                ('q4', models.CharField(choices=[('y', 'Oui'), ('n', 'Non')], default=True, max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'History',
                'verbose_name_plural': 'Histories',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('inUse', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Gallery',
                'verbose_name_plural': 'Galleries',
            },
        ),
        migrations.CreateModel(
            name='CoverPicture',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('inUse', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cover Picture',
                'verbose_name_plural': 'Cover Pictures',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_full_name', models.CharField(max_length=100, verbose_name='model full name')),
                ('model_email', models.EmailField(max_length=255, verbose_name='model email')),
                ('full_name', models.CharField(max_length=100, verbose_name='full name')),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(max_length=100, verbose_name='phone')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
    ]
