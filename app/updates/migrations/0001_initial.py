# Generated by Django 3.1.2 on 2021-02-16 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileUpdate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bio', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('changed_at', models.DateTimeField(auto_now=True)),
                ('dirty', models.BooleanField(default=False)),
                ('accept', models.BooleanField(blank=True, null=True)),
                ('decline', models.BooleanField(blank=True, null=True)),
                ('message', models.TextField(blank=True, default='', max_length=500)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='models.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Model Updates',
            },
        ),
        migrations.CreateModel(
            name='ProfilePictureUpdate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('changed_at', models.DateTimeField(auto_now=True)),
                ('dirty', models.BooleanField(default=False)),
                ('accept', models.BooleanField(blank=True, null=True)),
                ('decline', models.BooleanField(blank=True, null=True)),
                ('message', models.TextField(blank=True, default='', max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profile Picture Updates',
            },
        ),
        migrations.CreateModel(
            name='MeasuresUpdate',
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
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('changed_at', models.DateTimeField(auto_now=True)),
                ('dirty', models.BooleanField(default=False)),
                ('accept', models.BooleanField(blank=True, null=True)),
                ('decline', models.BooleanField(blank=True, null=True)),
                ('message', models.TextField(blank=True, default='', max_length=500)),
                ('measures', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='models.mensuration')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Measure Updates',
            },
        ),
        migrations.CreateModel(
            name='GalleryUpdate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('changed_at', models.DateTimeField(auto_now=True)),
                ('dirty', models.BooleanField(default=False)),
                ('accept', models.BooleanField(blank=True, null=True)),
                ('decline', models.BooleanField(blank=True, null=True)),
                ('message', models.TextField(blank=True, default='', max_length=500)),
                ('related_photo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.gallery')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Gallery Updates',
            },
        ),
        migrations.CreateModel(
            name='CoverPictureUpdate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('changed_at', models.DateTimeField(auto_now=True)),
                ('dirty', models.BooleanField(default=False)),
                ('accept', models.BooleanField(blank=True, null=True)),
                ('decline', models.BooleanField(blank=True, null=True)),
                ('message', models.TextField(blank=True, default='', max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Cover Picture Updates',
            },
        ),
    ]
