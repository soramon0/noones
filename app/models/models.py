import uuid

from django.db import models
from django.conf import settings


class Model(models.Model):
    SEXE_CHOICES = (
        ('F', 'Femme'),
        ('H', 'Homme'),
    )
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    handle = models.SlugField(max_length=100, unique=True)
    birth_date = models.DateField()
    facebook = models.URLField()
    instagram = models.URLField()
    phone = models.CharField(max_length=100)
    addresse = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=50)
    cin = models.CharField(max_length=100)
    profilePicture = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    coverPicture = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class Mensuratoin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    taille = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class History(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    q1 = models.TextField()
    q2 = models.TextField()
    q3 = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
