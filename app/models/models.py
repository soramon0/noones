import uuid

from django.db import models
from django.conf import settings


class Model(models.Model):
    SEXE_CHOICES = (
        ('f', 'Femme'),
        ('f', 'Homme'),
    )
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=500, blank=True)
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


class Mensuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    taille = models.IntegerField()
    taillenombrill = models.IntegerField()
    buste = models.IntegerField()
    epaules = models.IntegerField()
    hanches = models.IntegerField()
    poids = models.IntegerField()
    pointure = models.IntegerField()
    cheveux = models.CharField(max_length=100)
    yeux = models.CharField(max_length=100)
    permitted = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class History(models.Model):
    Q4_CHOICES = choices = (
        ('y', 'Oui'),
        ('n', 'Non'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    q1 = models.CharField(max_length=500)
    q2 = models.CharField(max_length=500)
    q3 = models.CharField(max_length=500)
    q4 = models.CharField(max_length=1, choices=Q4_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
