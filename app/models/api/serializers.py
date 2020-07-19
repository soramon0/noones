import os

from rest_framework import serializers

from models.models import (
    Model,
    Mensuration,
    Photo,
    ProfilePicture,
    CoverPicture,
)
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'user', 'sexe', 'first_name', 'last_name', 'bio', 'birth_date',
                  'facebook', 'instagram', 'phone', 'addresse', 'city', 'country', 'zipcode', 'cin']
        read_only_fields = ['user', 'id']


class MinimalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'first_name', 'last_name', 'city', 'country']
        read_only_fields = ['id']


class ModelContactSerializer(serializers.Serializer):
    model_id = serializers.CharField(max_length=100)
    model_full_name = serializers.CharField(min_length=3, max_length=100)
    full_name = serializers.CharField(min_length=6, max_length=100,)
    email = serializers.EmailField(max_length=255)
    phone = serializers.CharField(min_length=6, max_length=100)


class ProfilePictureWithModelSerializer(serializers.ModelSerializer):
    model = MinimalModelSerializer()

    class Meta:
        model = ProfilePicture
        fields = ['id', 'image', 'model']
        read_only_fields = ['id']


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ['id', 'image', 'inUse']
        read_only_fields = ['id', 'inUse']


class CoverPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverPicture
        fields = ['id', 'image', 'inUse']
        read_only_fields = ['id', 'inUse']


class MeasuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensuration
        fields = ['id', 'user', 'taille', 'taillenombrill', 'buste', 'epaules',
                  'hanches', 'poids', 'pointure', 'cheveux', 'yeux']
        read_only_fields = ['user', 'id']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'model']
        read_only_fields = ['id']


class SearchSerilaizer(serializers.Serializer):
    pays = serializers.ChoiceField(choices=(
        ('maroc', 'Maroc'),
        ('france', 'France'),
    ))
    ville = serializers.ChoiceField(choices=(
        ('marrakech', 'Marrakech'),
        ('agadir', 'Agadir'),
    ))
    sexe = serializers.ChoiceField(choices=(
        ('f', 'Femme'),
        ('h', 'Homme'),))
    cheveux = serializers.ChoiceField(choices=(
        ('brown', 'Brown'),
        ('yellow', 'Yellow'),
    ))
    yeux = serializers.ChoiceField(choices=(
        ('yellow', 'Yellow'),
        ('brown', 'Brown'),
    ))
    taille = serializers.ChoiceField(choices=(
        ('1.40-1.60', '1.40-1.60'),
        ('1.60-1.80', '1.60-1.80'),
        ('1.80-2.00', '1.80-2.00'),
    ))
