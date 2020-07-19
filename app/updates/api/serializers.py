from django.utils import timezone
from rest_framework import serializers

from updates.models import (
    ModelUpdate,
    MeasuresUpdate,
    PhotosUpdate,
    ProfilePictureUpdate,
    CoverPictureUpdate
)


class ModelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelUpdate
        fields = ('id', 'model', 'bio', 'accept', 'decline', 'message')
        read_only_fields = ('id', 'accept', 'decline', 'message')

    def update(self, instance, validated_data):
        if instance.decline:
            # if the instance has decline set to True
            # it means that the admin declined the update
            # and we should lift up the 24h update restriction
            # by setting decline to None and removing the previous
            # message the next time a user makes a new update request
            instance.decline = None
            instance.created_at = timezone.now()
            instance.message = ""
        return super().update(instance, validated_data)


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
            instance.created_at = timezone.now()
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
            instance.created_at = timezone.now()
            instance.message = ""
        return super().update(instance, validated_data)


class PhotosUpdateResterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotosUpdate
        fields = ('id', 'image', 'model', 'accept',
                  'decline', 'message', 'related_photo', 'created_at')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        # This serializer is only used to update a gallery image
        # and when we update it we always want to reset these fields
        # NOTE(karim): never use this serializer to create updates
        instance.created_at = timezone.now()
        instance.accept = None
        instance.decline = None
        instance.message = ''
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
            instance.created_at = timezone.now()
            instance.message = ""
        return super().update(instance, validated_data)


class CoverPictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverPictureUpdate
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
            instance.created_at = timezone.now()
            instance.message = ""
        return super().update(instance, validated_data)
