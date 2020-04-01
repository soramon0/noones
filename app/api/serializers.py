from rest_framework import serializers

from models.models import Model, Mensuration, History
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'sexe', 'first_name', 'last_name', 'bio', 'birth_date', 'user', 'profilePicture', 'coverPicture',
                  'facebook', 'instagram', 'phone', 'addresse', 'city', 'country', 'zipcode', 'cin']


class MeasuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensuration
        fields = ['id', 'taille', 'taillenombrill', 'buste', 'epaules',
                  'hanches', 'poids', 'pointure', 'cheveux', 'yeux']
