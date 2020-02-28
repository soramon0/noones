from rest_framework import serializers, viewsets

from models.models import Model

class MyModel(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)

# Serializers define the API representation.
class MyModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model
        fields = ['url', 'id']

# ViewSets define the view behavior.
class ModelsViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = MyModelSerializer