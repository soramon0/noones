import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


GENDER_CHOICES = (
    ("f", _("Female")),
    ("m", _("Male")),
)


class AbstractMensuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # taille
    height = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("height")
    )
    # taillenombrill for male
    waist = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("waist"))
    # buste for female
    bust = models.IntegerField(verbose_name=_("bust"))
    # epaules
    shoulders = models.IntegerField(verbose_name=_("shoulders"))
    # hanches
    hips = models.IntegerField(verbose_name=_("hips"))
    # poids
    weight = models.IntegerField(verbose_name=_("weight"))
    # pointure
    shoe_size = models.IntegerField(verbose_name=_("shoe size"))
    # cheveux
    hair = models.CharField(max_length=100, verbose_name=_("hair"))
    # yeux
    eyes = models.CharField(max_length=100, verbose_name=_("eyes"))

    class Meta:
        abstract = True


class Mensuration(AbstractMensuration):
    permitted = models.BooleanField(default=False, verbose_name=_("permitted"))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Mensuration")
        verbose_name_plural = _("Mensuration")

    def __str__(self):
        return self.user.email


class History(models.Model):
    Q4_CHOICES = choices = (
        ("y", _("Yes")),
        ("n", _("No")),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Qui étés vous?:
    q1 = models.CharField(max_length=500, help_text=_("Who are you?"))
    # Que connaissez-vous à propos de la MODE?
    q2 = models.CharField(
        max_length=500, help_text=_("What do you know about fashion?")
    )
    # Pourquoi devons-nous approuver votre inscription?
    q3 = models.CharField(
        max_length=500, help_text=_("Why do we need to approve your registration?")
    )
    q4 = models.CharField(max_length=1, choices=Q4_CHOICES, blank=False, default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("History")
        verbose_name_plural = _("Histories")

    def __str__(self):
        return self.user.email


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=False,
        default="m",
        verbose_name=_("gender"),
    )
    first_name = models.CharField(max_length=100, verbose_name=_("first name"))
    last_name = models.CharField(max_length=100, verbose_name=_("last name"))
    bio = models.CharField(max_length=500, blank=True, verbose_name=_("biography"))
    birth_date = models.DateField(verbose_name=_("birth date"))
    facebook = models.URLField()
    instagram = models.URLField()
    phone = models.CharField(max_length=100, verbose_name=_("phone"))
    address = models.CharField(max_length=100, verbose_name=_("address"))
    city = models.CharField(max_length=100, verbose_name=_("city"))
    country = models.CharField(max_length=100, verbose_name=_("country"))
    zipcode = models.CharField(max_length=50, verbose_name=_("zipcode"))
    nin = models.CharField(max_length=100, verbose_name=_("nin"))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.user.email


class ProfilePicture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="photos/%Y/%m/%d")
    inUse = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Profile Picture")
        verbose_name_plural = _("Profile Pictures")

    def __str__(self):
        return self.image.url


class CoverPicture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="photos/%Y/%m/%d")
    inUse = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Cover Picture")
        verbose_name_plural = _("Cover Pictures")

    def __str__(self):
        return self.image.url


class Gallery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="photos/%Y/%m/%d")
    inUse = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galleries")

    def __str__(self):
        return self.image.url


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    model_full_name = models.CharField(
        max_length=100, verbose_name=_("model full name")
    )
    model_email = models.EmailField(max_length=255, verbose_name=_("model email"))
    full_name = models.CharField(max_length=100, verbose_name=_("full name"))
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=100, verbose_name=_("phone"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return self.model_full_name
