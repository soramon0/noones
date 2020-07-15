import uuid

from django.db import models
from django.conf import settings


class AbstractMensuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    taille = models.DecimalField(max_digits=5, decimal_places=2)
    taillenombrill = models.DecimalField(max_digits=5, decimal_places=2)
    buste = models.IntegerField()
    epaules = models.IntegerField()
    hanches = models.IntegerField()
    poids = models.IntegerField()
    pointure = models.IntegerField()
    cheveux = models.CharField(max_length=100)
    yeux = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Mensuration(AbstractMensuration):
    permitted = models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


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
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Model(models.Model):
    SEXE_CHOICES = (
        ('f', 'Femme'),
        ('h', 'Homme'),
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
    is_public = models.BooleanField(default=False)
    highlight = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    measures = models.OneToOneField(
        Mensuration,
        on_delete=models.CASCADE,
    )
    history = models.OneToOneField(
        History,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.email


class ProfilePicture(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    inUse = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    model = models.ForeignKey(Model,
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url


class CoverPicture(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    inUse = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    model = models.ForeignKey(Model,
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    inUse = models.BooleanField(default=False)
    model = models.ForeignKey(Model,
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url


class Contact(models.Model):
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
    )
    model_full_name = models.CharField(max_length=100)
    model_email = models.EmailField(max_length=255)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.model_full_name
