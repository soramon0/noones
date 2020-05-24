import os

from rest_framework import serializers

from models.models import Model, Mensuration, Photo
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


class ProfilePictureSerializer(serializers.ModelSerializer):
    profilePicture = serializers.ImageField()

    class Meta:
        model = Model
        fields = ['id', 'profilePicture']
        read_only_fields = ['id']

class CoverPictureSerializer(serializers.ModelSerializer):
    coverPicture = serializers.ImageField()

    class Meta:
        model = Model
        fields = ['id', 'coverPicture']
        read_only_fields = ['id']

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

    def delete_old_image(image):
        # if we have an old image; delete it
        if image and os.path.isfile(image.path):
            # Get full path to old image
            os.remove(image.path)
    

    
