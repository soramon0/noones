from rest_framework import serializers

from updates.models import MeasuresUpdate, PhotosUpdate


class MeasuresUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasuresUpdate
        fields = ['id', 'measure', 'taille', 'taillenombrill', 'buste', 'epaules',
                  'hanches', 'poids', 'pointure', 'cheveux', 'yeux', 'accept', 'decline', 'message']
        read_only_fields = ['id', 'accept', 'decline', 'message']


class PhotosUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotosUpdate
        fields = ['id', 'image', 'model']
        read_only_fields = ['id']
