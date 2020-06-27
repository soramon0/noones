import datetime as dt


from rest_framework import serializers

from updates.models import (
    MeasuresUpdate,
    PhotosUpdate,
    ProfilePictureUpdate
)


class MeasuresUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasuresUpdate
        fields = ('id', 'measure', 'taille', 'taillenombrill', 'buste', 'epaules',
                  'hanches', 'poids', 'pointure', 'cheveux', 'yeux', 'accept', 'decline', 'message')
        read_only_fields = ('id', 'accept', 'decline', 'message')

    def update(self, instance, validated_data):
        if instance.decline:
            # if the instance has decline set to True
            # it means that the admin declined the update
            # and we should lift up the 24h update restriction
            # by setting decline to None and removing the previous
            # message the next time a user makes a new update request
            instance.decline = None
            instance.timestamp = dt.datetime.now(dt.timezone.utc)
            instance.message = ""
        return super().update(instance, validated_data)


class PhotosUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotosUpdate
        fields = ('id', 'image', 'model', 'accept',
                  'decline', 'message', 'related_photo')
        read_only_fields = ('id', 'accept', 'decline', 'message')

    def update(self, instance, validated_data):
        if instance.decline:
            # if the instance has decline set to True
            # it means that the admin declined the update
            # and we should lift up the 24h update restriction
            # by setting decline to None and removing the previous
            # message the next time a user makes a new update request
            instance.decline = None
            instance.timestamp = dt.datetime.now(dt.timezone.utc)
            instance.message = ""
        return super().update(instance, validated_data)


class ProfilePictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePictureUpdate
        fields = ('id', 'image', 'model', 'accept', 'decline', 'message')
        read_only_fields = ('id', 'accept', 'decline', 'message')

    def update(self, instance, validated_data):
        if instance.decline:
            # if the instance has decline set to True
            # it means that the admin declined the update
            # and we should lift up the 24h update restriction
            # by setting decline to None and removing the previous
            # message the next time a user makes a new update request
            instance.decline = None
            instance.timestamp = dt.datetime.now(dt.timezone.utc)
            instance.message = ""
        return super().update(instance, validated_data)
