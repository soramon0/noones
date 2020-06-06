from rest_framework import serializers

from clones.models import MeasuresClone, PhotoClone


class MeasuresCloneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasuresClone
        fields = ['id', 'measure', 'taille', 'taillenombrill', 'buste', 'epaules',
                  'hanches', 'poids', 'pointure', 'cheveux', 'yeux']
        read_only_fields = ['id']


class PhotosCloneSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoClone
        fields = ['id', 'image', 'original']
        read_only_fields = ['id']
