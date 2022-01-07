from rest_framework import serializers


class OutputCountrySerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()


class OutputCitySerializer(serializers.Serializer):
    name = serializers.CharField()
