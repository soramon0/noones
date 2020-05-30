from rest_framework import serializers

from clones.models import MeasuresClone

class MeasuresCloneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasuresClone
        fields = ['id', 'measure', 'taille', 'taillenombrill', 'buste', 'epaules',
                  'hanches', 'poids', 'pointure', 'cheveux', 'yeux']
        read_only_fields = ['id']