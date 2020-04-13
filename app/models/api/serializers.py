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
    
class ProfilePictureSerializer(serializers.ModelSerializer):
    profilePicture = serializers.ImageField()
    class Meta:
        model = Model
        fields = ['id', 'profilePicture']

class CoverPictureSerializer(serializers.ModelSerializer):
    coverPicture = serializers.ImageField()
    class Meta:
        model = Model
        fields = ['id', 'coverPicture']


class MeasuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensuration
        fields = ['id', 'user', 'taille', 'taillenombrill', 'buste', 'epaules',
                  'hanches', 'poids', 'pointure', 'cheveux', 'yeux']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'model']
