# Generated by Django 3.0.3 on 2020-02-06 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20200206_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_id', models.UUIDField()),
                ('model_nom', models.CharField(max_length=100)),
                ('model_email', models.EmailField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(max_length=100)),
            ],
        ),
    ]
