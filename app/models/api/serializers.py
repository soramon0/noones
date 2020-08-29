import os

from rest_framework import serializers

from models.models import (
    Profile,
    Mensuration,
    Gallery,
    ProfilePicture,
    CoverPicture,
    GENDER_CHOICES,
)
from models.forms import HAIR_CHOICES

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'gender', 'first_name', 'last_name', 'bio', 'birth_date',
                  'facebook', 'instagram', 'phone', 'address', 'city', 'country', 'zipcode', 'nin')
        read_only_fields = ('user', 'id')


class MinimalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'city', 'country')
        read_only_fields = ('id',)


class ModelContactSerializer(serializers.Serializer):
    model_id = serializers.CharField(max_length=100)
    model_full_name = serializers.CharField(min_length=3, max_length=100)
    full_name = serializers.CharField(min_length=6, max_length=100,)
    email = serializers.EmailField(max_length=255)
    phone = serializers.CharField(min_length=6, max_length=100)


class ProfilePictureWithModelSerializer(serializers.ModelSerializer):
    profile = MinimalModelSerializer()

    class Meta:
        model = ProfilePicture
        fields = ('id', 'image', 'profile')
        read_only_fields = ('id',)


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ('id', 'image', 'inUse')
        read_only_fields = ('id', 'inUse')


class CoverPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverPicture
        fields = ('id', 'image', 'inUse')
        read_only_fields = ('id', 'inUse')


class MeasuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensuration
        fields = ('id', 'user', 'height', 'waist', 'bust', 'shoulders',
                  'hips', 'weight', 'shoe_size', 'hair', 'eyes')
        read_only_fields = ('user', 'id')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('id', 'image', 'profile')
        read_only_fields = ('id',)


class SearchSerilaizer(serializers.Serializer):
    country = serializers.ChoiceField(choices=(
        ('maroc', 'Maroc'),
        ('france', 'France'),
    ))
    city = serializers.ChoiceField(choices=(
        ('marrakech', 'Marrakech'),
        ('agadir', 'Agadir'),
    ))
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    hair = serializers.ChoiceField(choices=HAIR_CHOICES)
    eyes = serializers.ChoiceField(choices=HAIR_CHOICES)
    height = serializers.ChoiceField(choices=(
        ('1.40-1.60', '1.40-1.60'),
        ('1.60-1.80', '1.60-1.80'),
        ('1.80-2.00', '1.80-2.00'),
    ))
