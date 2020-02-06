import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Carousel(models.Model):
    image = models.ImageField(upload_to='photos/site/%Y/%m/%d')
    title = models.CharField(max_length=100)
    inUse = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Header(models.Model):
    image = models.ImageField(upload_to='photos/site/%Y/%m/%d')
    inUse = models.BooleanField(default=False)

    def __str__(self):
        return self.image.url
