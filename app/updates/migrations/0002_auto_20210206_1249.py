# Generated by Django 3.1.2 on 2021-02-06 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileupdate',
            name='changed_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='profileupdate',
            name='dirty',
            field=models.BooleanField(default=False),
        ),
    ]
